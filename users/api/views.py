from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from users.api.serializers import RegistrationSerializer, UserSerializer, UserListSerializer
from users import models

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):    
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def post(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            print(serializer.data)
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'response': "Registration Successful",
                'token': token.key,
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
                }, status.HTTP_201_CREATED)
        print("Registration errors: ", serializer.errors)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print("Logged in!!")
        print(user.is_staff)
        return Response({
            'response': "Login Successfull",
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_staff': user.is_staff
        })
            
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.user.auth_token.delete()
        return Response('Logged out successfully', status=status.HTTP_200_OK)

