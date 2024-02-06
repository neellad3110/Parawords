from rest_framework import serializers
from .models import RegisterUser
import re
from django.contrib.auth.hashers import make_password,check_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields ='__all__'

 
    def validate(self,data):
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,}$"

        if not re.match(password_regex,data["password"]):
            raise serializers.ValidationError({'error':"Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."})
                 
        return data
    
    def create(self, validated_data):

        try:
            user_obj=RegisterUser.objects.create(name=validated_data["name"],email=validated_data["email"],dob=validated_data["dob"])
            user_obj.set_password(validated_data["password"])
        except Exception as e :
            raise serializers.ValidationError({'error':"Error while creating new user."})

        user_obj.save()
        return user_obj
    
class AuthUserSerializer(serializers.Serializer):

    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self,data):
        
        try:
            user_obj=RegisterUser.objects.get(email=data["email"])
            
            if not check_password(data['password'],user_obj.password): 
                raise serializers.ValidationError({'error':"Invalid credentials."})

        except Exception as e :
            raise serializers.ValidationError({'error':e})
           
        return data
    