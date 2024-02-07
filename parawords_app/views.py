from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,AuthUserSerializer,ParagraphSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken 
from .models import RegisterUser,Paragraph,Word
from django.shortcuts import redirect

# Create your views here.

def redirect_to_register(request):
    """
    Redirects users to the registration page whenever they access the root URL.
    """
    return redirect('/register')
class register(APIView):
    """API endpoint for registering new users"""  
    # def get(self, request, format=None):
    #     users_obj = RegisterUser.objects.all()
    #     return Response({'status':200,'payload':CustomUserSerializer(users_obj,many=True).data})
    
    def post(self, request, format=None):
        serialized_data=CustomUserSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response({'status':403,'error':serialized_data.errors})

        serialized_data.save()
        return Response({'status':200,'payload':serialized_data.data,'message':'user added successfully'})

class authuser(APIView):
    """API endpoint for authenticating registered users and generating auth jwt token"""
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
    
class paragraph(APIView):
    """API endpoint for adding new content leading to creating paragraph and words class instance"""
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        
        serialized_data=ParagraphSerializer(data=request.data,context = {'request':request})
        if not serialized_data.is_valid():
            return Response({'status':403,'error':serialized_data.errors})
        
        serialized_data.save()
        return Response({'status':200,'user_id':request.user.id,'payload':serialized_data.data,'message':'paragraphs added successfully'})

class word(APIView):
    """API endpoint for finding words from added paragraph by registered user""" 
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        word=request.data["word"]
        try:
           
            word_obj=Word.objects.filter(user=request.user.id,word=word).order_by('created_at')
            
            if word_obj is None:
                raise ValueError({"error":"No paragraphs found which contain '"+word+"'"})
            else:

                para_id=word_obj.values_list('paragraph',flat=True)
                para_obj=Paragraph.objects.filter(user=request.user.id,id__in=para_id).values('paragraph')
                para_found=para_obj.values_list('paragraph',flat=True)

        except Exception as e:
            return Response({'message':'Error occured while fetching paragraphs.'})
        
        return Response({'paragraphs':para_found})
            
    