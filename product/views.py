from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        messages.success(request, "Signup successful. Please login.")
        return redirect("login")

    return render(request, "product/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                request.session["user_id"] = user.id  # Simple session auth
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "product/login.html")

'''
def dashboard_view(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    return render(request, "dashboard.html", {"user": user})
'''



def logout_view(request):
    request.session.flush()
    return redirect("login")



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Item, Payment, Profile
import json

@login_required
def dashboard(request):
    lent_items = Item.objects.filter(owner=request.user)
    borrowed_items = Item.objects.filter(borrower=request.user)
    payments = Payment.objects.filter(user=request.user)

    return render(request, "product/dashboard.html", {
        "lent_items": lent_items,
        "borrowed_items": borrowed_items,
        "payments": payments,
    })

@login_required
def update_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        profile = request.user.profile
        profile.latitude = data.get("latitude")
        profile.longitude = data.get("longitude")
        profile.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)
