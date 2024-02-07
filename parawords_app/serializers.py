from rest_framework import serializers      
from .models import RegisterUser,Paragraph,Word
import re
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password


class CustomUserSerializer(serializers.ModelSerializer):
    """ A serializer for serializing and deserializing RegisterUser objects. """

    email = serializers.CharField(required=True,validators=[UniqueValidator(queryset=RegisterUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = RegisterUser
        fields ='__all__'

    def validate(self, attrs):
        """Performs basic validation on the serializer data."""
        return attrs    
    
    def create(self, validated_data):
        """Creates a new RegisterUser object from the validated data."""
        try:
            user_obj=RegisterUser.objects.create(name=validated_data["name"],email=validated_data["email"],dob=validated_data["dob"])
            user_obj.set_password(validated_data["password"])
        except Exception as e :
            raise serializers.ValidationError({'error':"Error while creating new user."})

        user_obj.save()
        return user_obj
    
class AuthUserSerializer(serializers.Serializer):

    """ Serializer for authenticating users using email and password credentials. """

    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self,data):
        """ Validation of email and password """
        try:
            user_obj=RegisterUser.objects.get(email=data["email"])
            
            if not check_password(data['password'],user_obj.password): 
                raise serializers.ValidationError({'error':"Invalid credentials."})
        except Exception as e :
            raise serializers.ValidationError({'error':e})
           
        return data
class ParagraphSerializer(serializers.ModelSerializer):
    """Serializer for creating paragraph and words objects"""
    class Meta:
        model = Paragraph
        fields =["paragraph"]

    def create(self, validated_data):
        """ creating paragraph and words objects ."""
        request_data=self.context["request"]       # collecting data in request from context 
        user_id=request_data.user.id               # collecting user id fetch from JWT and passsed in context                         
        try:        
            user_obj=RegisterUser.objects.get(id=user_id)   

            # spliting paragraphs from text
            content=str(validated_data["paragraph"]).split('\n\n')

            for paragraph in content:
                #creating paragraph objects
                para_obj=Paragraph.objects.create(user=user_obj,paragraph=paragraph)

                # spliting words from the paragraph field in paragraph instance
                word_list=str(para_obj.paragraph).split(' ')

                for word in set(word_list):     # set() is used for considering a single word in a paragraph (if same words present in a paragraph for multiple times ) 

                    # removing special characters found with words and convertind to lowercase
                    cleaned_word=re.sub(r'[^a-zA-Z0-9]', '', word).strip().lower()

                    #creating word instance
                    word_obj=Word.objects.create(user=user_obj,paragraph=para_obj,word=cleaned_word)

        except Exception as e:
                raise serializers.ValidationError({"error":"Error occured while saving the paragraphs."})
        return validated_data
