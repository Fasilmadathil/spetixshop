from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from datetime import timedelta


# class person(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField(null=True)
#     place = models.CharField(max_length=50)


class User(AbstractUser):
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expire_time = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Add a unique related_name
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='custom_user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Add a unique related_name
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='custom_user_permission',
    )

    def set_otp(self, otp, expire_duration=5):
        self.otp = otp
        self.otp_expire_time = timezone.now() + timedelta(minutes=expire_duration)
        self.save()

    def verify_otp(self, otp):
        if self.otp == otp and self.otp_expire_time > timezone.now():
            self.is_verified = True
            self.otp = None
            self.otp_expire_time = None
            self.save()
            return True
        return False

    def block_user(self):
        self.is_blocked = True
        self.save()

    def unblock_user(self):
        self.is_blocked = False
        self.save()

    def __str__(self):
        return self.username


class Product(models.Model):
    # Define fields for the product
    name = models.CharField(max_length=200)  # Name of the product
    image = models.CharField(max_length=100)  # link of the image
    description = models.TextField(blank=True)  # Description of the product
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # Price of the product
    stock = models.PositiveIntegerField(
        default=0)  # Number of products in stock
    # Store the rating of the product
    rating = models.DecimalField(max_digits=2, decimal_places=2)
    # Timestamp when the product was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when the product was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
