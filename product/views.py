from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User

from django.contrib.auth import authenticate, login

from django.contrib import messages
# import User
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:  # simple validation
            Item.objects.create(
                name=name,
                description=description,
                owner=request.user,
            )
            return redirect("my_items")  # redirect to /my-items after adding

    return render(request, "add_item.html")




def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        # Create and save new user
        user = User(username=username, email=email)
        user.set_password(password)  # hash the password
        user.save()

        messages.success(request, "Signup successful. Please login.")
        return redirect("login")

    return render(request, "product/signup.html")




'''def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup")

        user = User(username=username, email=email)
        login(request, user)
        user.set_password(password)
        user.save()
        messages.success(request, "Signup successful. Please login.")
        return redirect("login")

    return render(request, "product/signup.html")

'''

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # authenticate user
        if user is not None:
            login(request, user)  # log the user in and start a session
            return redirect("dashboard")  # redirect to dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "product/login.html")



'''
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





from django.shortcuts import render, get_object_or_404
from .models import Item
from django.conf import settings

def landing_page(request):
    items = Item.objects.all()
    return render(request, "product/landing.html", {"items": items})

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, "product/item_detail.html", {
        "item": item,
        "PAYSTACK_PUBLIC_KEY": settings.PAYSTACK_PUBLIC_KEY
    })







from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile, Item

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, "product/profile.html", {"profile": profile})

@login_required
def my_items_view(request):
    my_items = Item.objects.filter(owner=request.user)
    return render(request, "product/my_items.html", {"my_items": my_items})

@login_required
def borrowed_items_view(request):
    borrowed_items = Item.objects.filter(borrower=request.user)
    return render(request, "product/borrowed_items.html", {"borrowed_items": borrowed_items})
