from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import *
from rest_framework import generics 
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken



from .serializers import *
from .models import *


class TestApi(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response({
            "detail": "User is authenticated!"
        })


class SignUpView(generics.GenericAPIView):
    def post(self, request):
         
        serializer = UserSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful !"
            data['email'] = account.email
        
        else:
            data = serializer.errors
            
        return Response(data)


class LogOutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



