from django.shortcuts import render
from django.http import JsonResponse

def initiate_payment(request):
    # This will later call M-Pesa API
    return JsonResponse({'status': 'success', 'message': 'Payment initiated'})
