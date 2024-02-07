from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError("The Email is required.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(mobile, password, **extra_fields)
    
class RegisterUser(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name','dob','passoword']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
class Paragraph(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    paragraph=models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Word(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    paragraph = models.ForeignKey(Paragraph,on_delete=models.CASCADE)
    word=models.CharField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)    