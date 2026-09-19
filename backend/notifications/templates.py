"""Centralised, product-facing notification messages."""


def payment_confirmation(amount, balance=None):
    message = f"Nyumbani: Payment of KSh {amount} received successfully."
    if balance is not None:
        message += f" Remaining balance: KSh {balance}."
    return message


def payment_failed():
    return "Nyumbani: Your payment attempt failed. Please try again."


def new_inquiry(property_name, name):
    return f"Nyumbani: New inquiry for {property_name} from {name}."


def maintenance_alert(tenant_name, issue_type):
    return f"Nyumbani: New maintenance issue from {tenant_name}: {issue_type}."

