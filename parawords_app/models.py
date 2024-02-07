from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
"""
    1. AbstractBaseUser:

    Abstract base class for creating custom user models in Django.
    Provides essential user fields like username, password, email, and active status.
    Includes password hashing, permission management, and authentication support.
    Customizable through overriding methods and adding custom fields.

    2. PermissionsMixin:

    Mixin used to add permission management functionalities to models.
    Enables checking if a user has specific permissions or permissions in an app.
    Used in conjunction with AbstractBaseUser for user permission control.

    3. BaseUserManager:

    Base manager for user models, handling user creation and password hashing.
    Provides methods for creating new users with password security.
    Used internally by AbstractBaseUser for user management tasks.
"""
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user manager for creating users and superusers.

    Enforces email as the required field and sets default active status.
    Raises errors for missing email or incorrect superuser configuration.
    """

    def create_user(self,email,password, **extra_fields):
        """creating user"""
        if not email:
            raise ValueError("The Email is required.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        """creating super user"""
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(mobile, password, **extra_fields)
    
class RegisterUser(AbstractBaseUser,PermissionsMixin):
    """A custom user model for managing registered users.

        This model inherits from `AbstractBaseUser` and `PermissionsMixin` to provide
        standard user authentication and permission management functionalities. It also
        adds custom fields and overrides some methods for specific purposes.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  #Set to `email` for authentication using email address.
    REQUIRED_FIELDS = ['name','dob','passoword']  #fields required for user creation.

    # instance of  `CustomUserManager` for user creation
    objects = CustomUserManager()

    def __str__(self):
        """Returns the user's email as the string representation."""
        return self.email
class Paragraph(models.Model):
    """
    A model representing individual paragraphs added by registered users.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    paragraph=models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Word(models.Model):
    """
    A model representing individual present in each paragraphs added by registered users.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph,on_delete=models.CASCADE)
    word=models.CharField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)    