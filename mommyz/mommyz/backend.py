from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from one.models import User
from django.core.exceptions import ValidationError

# User = get_user_model()


class CustomUserBackend(ModelBackend):
    """
    Custom authentication backend that supports custom User model authentication
    with additional checks for is_verified and is_blocked status.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Use email or username based on your custom model's configuration
            # Adjust to email if that's your login field
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        # Verify password
        if user.check_password(password):
            # Additional checks for custom fields
            if user.is_blocked:
                raise ValidationError("User account is blocked.")
            # if not user.is_verified:
            #     raise ValidationError("User account is not verified.")
            return user

        return None
