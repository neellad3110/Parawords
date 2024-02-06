from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from uuid import uuid4

# Create your models here.
class RegisterUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name', 'dob','email','password']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

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