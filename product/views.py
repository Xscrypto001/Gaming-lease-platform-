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
from .models import *



import os
import re
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.files.storage import default_storage
from django.db import models
from django.conf import settings
import uuid


def terms(request):
    
    return render(request, "product/terms.html")

'''
# Add this model to your models.py (alongside your custom User model)
class UserDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id', 'ID Upload'),
        ('proof_address', 'Proof of Address'),
        ('proof_income', 'Proof of Income'),
        ('bank_statement', 'Bank Statement'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='user_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    
    class Meta:
        unique_together = ('user', 'document_type')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"
'''

def signup_view(request):
    if request.method == "POST":
        # Get form data
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        terms_accepted = request.POST.get("terms_accepted")
        
        # Get file uploads
        id_upload = request.FILES.get('id_upload')
        proof_address = request.FILES.get('proof_address')
        proof_income = request.FILES.get('proof_income')
        bank_statement = request.FILES.get('bank_statement')
        
        # Validation
        errors = []
        
        # Basic validation
        if not username:
            errors.append("Username is required")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters long")
        
        if not email:
            errors.append("Email is required")
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Please enter a valid email address")
        
        # Password validation with regex
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not password:
            errors.append("Password is required")
        elif not re.match(password_regex, password):
            errors.append("Password must be at least 8 characters with uppercase, lowercase, number and special character")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if not terms_accepted:
            errors.append("You must agree to the Terms and Conditions")
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors.append("Username already taken")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered")
        
        # File validation
        required_files = {
            'ID Upload': id_upload,
            'Proof of Address': proof_address,
            'Proof of Income': proof_income,
            'Bank Statement': bank_statement
        }
        
        for field_name, file_obj in required_files.items():
            if not file_obj:
                errors.append(f"{field_name} is required")
            else:
                # Validate file type
                allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']
                file_extension = os.path.splitext(file_obj.name)[1].lower()
                if file_extension not in allowed_extensions:
                    errors.append(f"{field_name} must be PDF, JPG, JPEG, or PNG format")
                
                # Validate file size (max 10MB)
                max_size = 10 * 1024 * 1024  # 10MB
                if file_obj.size > max_size:
                    errors.append(f"{field_name} must be smaller than 10MB")
        
        # If there are validation errors, show them and return to form
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, "product/signup.html", {
                'username': username,
                'email': email,
            })
        
        try:
            # Create and save new user
            user = User(username=username, email=email)
            user.set_password(password)  # hash the password
            user.save()
            
            # Save documents
            document_mapping = {
                id_upload: 'id',
                proof_address: 'proof_address', 
                proof_income: 'proof_income',
                bank_statement: 'bank_statement'
            }
            
            saved_documents = []
            
            for file_obj, doc_type in document_mapping.items():
                if file_obj:
                    try:
                        # Generate unique filename to avoid conflicts
                        file_extension = os.path.splitext(file_obj.name)[1]
                        unique_filename = f"{user.id}_{doc_type}_{uuid.uuid4().hex[:8]}{file_extension}"
                        
                        # Create UserDocument instance
                        user_document = UserDocument.objects.create(
                            user=user,
                            document_type=doc_type,
                            file_name=file_obj.name,
                            file_size=file_obj.size
                        )
                        
                        # Save file to storage
                        file_path = f"user_documents/{user.id}/{unique_filename}"
                        saved_path = default_storage.save(file_path, file_obj)
                        user_document.file = saved_path
                        user_document.save()
                        
                        saved_documents.append(user_document)
                        
                    except Exception as file_error:
                        # If any file upload fails, clean up everything
                        user.delete()
                        for doc in saved_documents:
                            if doc.file:
                                default_storage.delete(doc.file.name)
                            doc.delete()
                        
                        messages.error(request, f"Error uploading files: {str(file_error)}")
                        return render(request, "product/signup.html", {
                            'username': username,
                            'email': email,
                        })
            
            # Success - log the user in automatically
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, f"Account created successfully! Welcome, {username}!")
                return redirect("dashboard")  # Change to your desired redirect page
            else:
                messages.success(request, "Signup successful. Please login.")
                return redirect("login")
                
        except Exception as e:
            messages.error(request, f"An error occurred during signup: {str(e)}")
            return render(request, "product/signup.html", {
                'username': username,
                'email': email,
            })

    return render(request, "product/signup.html")


# Additional utility functions you might need

def get_user_documents_view(request):
    """
    View to display user's uploaded documents (for profile/dashboard)
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        documents = UserDocument.objects.filter(user=request.user).order_by('-uploaded_at')
        return render(request, 'product/user_documents.html', {
            'documents': documents
        })
    except Exception as e:
        messages.error(request, f"Error loading documents: {str(e)}")
        return redirect('dashboard')


def delete_user_document_view(request, document_id):
    """
    Allow users to delete their own documents
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        document = UserDocument.objects.get(id=document_id, user=request.user)
        
        # Delete file from storage
        if document.file:
            default_storage.delete(document.file.name)
        
        # Delete database record
        document_type = document.get_document_type_display()
        document.delete()
        
        messages.success(request, f"{document_type} deleted successfully")
        
    except UserDocument.DoesNotExist:
        messages.error(request, "Document not found or you don't have permission to delete it")
    except Exception as e:
        messages.error(request, f"Error deleting document: {str(e)}")
    
    return redirect('user_documents')


# Don't forget to add these URLs to your urls.py:
"""
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('user-documents/', views.get_user_documents_view, name='user_documents'),
    path('delete-document/<int:document_id>/', views.delete_user_document_view, name='delete_document'),
    # ... your other URLs
]
"""

# Add these settings to your settings.py if not already present:
"""
import os

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10MB

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for file uploads
FILE_UPLOAD_PERMISSIONS = 0o644
"""




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



'''
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




def signup_view(request):
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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

@login_required
def profile_view(request):
    user = request.user  # current logged in user
    return render(request, "product/profile.html", {"profile": user})



@login_required
def my_items_view(request):
    my_items = Item.objects.filter(owner=request.user)
    return render(request, "product/my_items.html", {"my_items": my_items})

@login_required
def borrowed_items_view(request):
    borrowed_items = Item.objects.filter(borrower=request.user)
    return render(request, "product/borrowed_items.html", {"borrowed_items": borrowed_items})







from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Item

@login_required
def add_item(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        file = request.FILES.get("file")  # handle uploaded file/image
        if name:  # simple validation
            Item.objects.create(
                name=name,
                description=description,
                file = file,
                owner=request.user,
            )
            return redirect("my_items")  # redirect to /my-items after adding

    return render(request, "product/add_item.html")
