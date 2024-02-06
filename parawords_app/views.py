from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,AuthUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import RegisterUser

# Create your views here.

class register(APIView):
   
    def get(self, request, format=None):
        users_obj = RegisterUser.objects.all()
        print(users_obj)
        return Response({'status':200,'payload':CustomUserSerializer(users_obj,many=True).data})
    
    def post(self, request, format=None):
        serialized_data=CustomUserSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response({'status':403,'error':serialized_data.errors})

        serialized_data.save()
        return Response({'status':200,'payload':serialized_data.data,'message':'user added successfully'})

class authuser(APIView):

    def post(self, request, format=None):
        serialized_data=AuthUserSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response({'status':403,'error':serialized_data.errors})
        
        try:
            user_obj=RegisterUser.objects.get(email=serialized_data.data["email"])
        except Exception as e:
            return Response({'message':'Error occured while generating token.'})

        refresh = RefreshToken.for_user(user_obj)
        return Response({'status':200,'user_id': user_obj.id,'token':str(refresh.access_token),'message':'token generated successfully'})
    
class welcome(APIView):
    
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        return Response({'status':200,'message':'authenticated successfully'})
    
