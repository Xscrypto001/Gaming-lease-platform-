from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone




class User(AbstractUser):
    # Roles
    is_lender = models.BooleanField(default=False)
    is_borrower = models.BooleanField(default=False)

    # Contact & profile
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    gamer_tag = models.CharField(max_length=50, unique=True, null=True, blank=True)
    avatar_url = models.URLField(blank=True, null=True)

    # Location (from frontend mobile permission)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Wallet balance
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.username or self.gamer_tag


class UserDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id', 'ID Upload'),
        ('proof_address', 'Proof of Address'),
        ('proof_income', 'Proof of Income'),
        ('bank_statement', 'Bank Statement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='user_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField()
    
    class Meta:
        unique_together = ('user', 'document_type')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"
class GamingEquipment(models.Model):
    EQUIPMENT_TYPES = [
        ("PLAYSTATION", "PlayStation Console"),
        ("XBOX", "Xbox Console"),
        ("NINTENDO", "Nintendo Switch"),
        ("PC", "Gaming PC"),
        ("VR", "VR Headset"),
        ("ACCESSORY", "Accessory (controller, chair, etc.)"),
        ("OTHER", "Other"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="equipments")
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    brand = models.CharField(max_length=100, blank=True, null=True)  # e.g., Sony, Microsoft
    model = models.CharField(max_length=100, blank=True, null=True)  # e.g., PS5, Xbox Series X
    description = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=50, default="Good")  # e.g., New, Good, Used
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment_type} - {self.owner.username}"




class LoanRequest(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("FUNDED", "Funded"),
        ("ONGOING", "Ongoing"),
        ("REPAID", "Repaid"),
        ("DEFAULTED", "Defaulted"),
    ]

    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_requests")
    lender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="loans_given")
    equipment = models.ForeignKey(GamingEquipment, on_delete=models.SET_NULL, null=True, blank=True)

    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    duration_days = models.PositiveIntegerField()  # how long the loan lasts
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # %

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan {self.id} by {self.borrower.username}"




class Repayment(models.Model):
    loan = models.ForeignKey(LoanRequest, on_delete=models.CASCADE, related_name="repayments")
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Repayment for Loan {self.loan.id} - {self.amount_due}"




class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAWAL", "Withdrawal"),
        ("LOAN_FUND", "Loan Funding"),
        ("REPAYMENT", "Repayment"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    tx_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tx_type} - {self.amount}"
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Payment

@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "payments/payment_list.html", {"payments": payments})
'''



from django.db import models
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items_lent")
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="items_borrowed")
    is_borrowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
#    image = models.ImageField(upload_to="items/", blank=True, null=True)
    file = models.FileField(upload_to="items/files/", blank=True, null=True)  # any file

    time_from = models.TimeField(null=True)
    time_to = models.TimeField(null=True)
    
    # Price
    price = models.DecimalField(max_digits=20, decimal_places=2,null=True)
    def __str__(self):
        return f"{self.name} (Owner: {self.owner.username})"


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("failed", "Failed"),
        ],
        default="pending"
    )

    def __str__(self):
        return f"Payment {self.amount} by {self.user.username} for {self.item.name}"
