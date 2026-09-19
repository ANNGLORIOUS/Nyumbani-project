from django.http import JsonResponse


def home(request):
    """The browser UI is the React app in ``frontend/``; Django serves its API."""
    return JsonResponse({
        "name": "Nyumbani API",
        "frontend": "Run the Vite app at http://127.0.0.1:5173/",
        "status": "ok",
    })


def api_status(request):
    return JsonResponse({
        "name": "Nyumbani Property Management API",
        "status": "ok",
        "endpoints": {
            "users": "/api/users/",
            "properties": "/api/properties/",
            "payments": "/api/payments/",
            "admin": "/admin/",
        },
    })
