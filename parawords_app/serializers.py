from rest_framework import serializers
from .models import RegisterUser,Paragraph,Word
import re
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.CharField(required=True,validators=[UniqueValidator(queryset=RegisterUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = RegisterUser
        fields ='__all__'

    def validate(self, attrs):
        return attrs    
    
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
class ParagraphSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paragraph
        fields =["paragraph"]

    def create(self, validated_data):

        request_data=self.context["request"]
        user_id=request_data.user.id
        gen_para_obj=[]
        try:        
            user_obj=RegisterUser.objects.get(id=user_id)
            content=str(validated_data["paragraph"]).split('\n\n')

            for paragraph in content:

                para_obj=Paragraph.objects.create(user=user_obj,paragraph=paragraph)
                gen_para_obj.append(para_obj)
                

                word_list=str(para_obj.paragraph).split(' ')

                for word in set(word_list):
                    cleaned_word=re.sub(r'[^a-zA-Z0-9]', '', word).strip().lower()
                    word_obj=Word.objects.create(user=user_obj,paragraph=para_obj,word=cleaned_word)
                    
            
        except Exception as e:
                raise serializers.ValidationError({"error":"Error occured while saving the paragraphs."})
        

        return validated_data
