from django.contrib import admin

#imported model to register
from .models import RegisterUser
# Register your models here.
admin.site.register(RegisterUser)
