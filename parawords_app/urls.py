from django.urls import path
from .views import register,authuser,paragraph,word
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   

urlpatterns = [
    # path('',views.welcome),
    path('register',register.as_view()),
    path('authuser',authuser.as_view()),
    path('paragraph',paragraph.as_view()),
    path('word',word.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]