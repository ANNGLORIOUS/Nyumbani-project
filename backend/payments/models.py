from django.conf import settings
from django.db import models
from properties.models import Property
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Payment(models.Model):
    STATUS = [('pending','pending'), ('confirmed','confirmed'), ('failed','failed')]

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, related_name='payments')
    rent_record = models.ForeignKey('RentRecord', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def confirm(self, confirmed_at=None):
        """Confirm once and reconcile its linked rent obligation."""
        if self.status == 'confirmed':
            return False
        self.status = 'confirmed'
        self.confirmed_at = confirmed_at or timezone.now()
        self.save(update_fields=('status', 'confirmed_at'))
        if self.rent_record_id:
            self.rent_record.recalculate()
        return True


class Lease(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leases')
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='leases')
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    due_day = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not 1 <= self.due_day <= 28:
            raise ValidationError({'due_day': 'Due day must be between 1 and 28.'})
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot precede the start date.'})


class RentRecord(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'), ('due', 'Due'), ('partially_paid', 'Partially paid'),
        ('paid', 'Paid'), ('overdue', 'Overdue'),
    ]
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='rent_records')
    period = models.DateField(help_text='First day of the rent month.')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=('lease', 'period'), name='unique_lease_rent_period')]
        ordering = ('-due_date',)

    @property
    def balance(self):
        return max(self.amount_due - self.amount_paid, 0)

    def recalculate(self, today=None):
        from django.db.models import Sum
        from django.utils import timezone
        self.amount_paid = self.payments.filter(status='confirmed').aggregate(total=Sum('amount'))['total'] or 0
        today = today or timezone.localdate()
        if self.amount_paid >= self.amount_due:
            self.status = 'paid'
        elif self.amount_paid > 0:
            self.status = 'partially_paid'
        elif today > self.due_date:
            self.status = 'overdue'
        elif today >= self.period:
            self.status = 'due'
        else:
            self.status = 'upcoming'
        self.save(update_fields=('amount_paid', 'status'))
