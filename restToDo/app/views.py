import datetime
# from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Task
from .serializers import CustomUserSerializer, TaskSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import requests

# admin
# RARE0000


class RegisterView(APIView):
    # def post(self, request):
    #     username = request.data.get('username')
    #     email = request.data.get('email')
    #     password = make_password(request.data.get('password'))

    #     if not username or not email or not password:
    #         return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

    #     if User.objects.filter(username=username).exists():
    #         return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    #     if User.objects.filter(email=email).exists():
    #         return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    #     user = User.objects.create(username=username, email=email, password=password)
        def post(self, request):

            userName = request.data.get('userName')
            userEmail = request.data.get('userEmail')
            userPassword = make_password(request.data.get('userPassword'))

            if not userName or not userEmail or not userPassword:
                return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(userName=userName).exists():
                return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(userEmail=userEmail).exists():
                return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

            user = CustomUser.objects.create(userName=userName, userEmail=userEmail, userPassword=userPassword)
            if user:
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RestrictedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        userName = request.data.get('userName')
        userPassword = request.data.get('userPassword')

        user = authenticate(username=userName, password=userPassword)
        print("USER", user)
    
        return JsonResponse({"response": "You are Allowed here"})


class LoginView(APIView):
    def post(self, request):
        userName = request.data.get('userName')
        userPassword = request.data.get('userPassword')
        request.session['username'] = userName
        print("userPassword", userPassword)
        user = authenticate(username=userName, password=userPassword)
        print("USER", user)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomUserCRUD(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        taskDate = datetime.datetime.now()
        taskName = request.data.get('taskName')
        taskDescription = request.data.get('taskDescription')
        loggedUser = request.session['username']
        user_instance = CustomUser.objects.get(userName=loggedUser)

        try:
            task = Task(user_id=user_instance, taskDate=taskDate, taskName=taskName, taskDescription=taskDescription)
            task.save()
            return Response({'message': 'Task created successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error",e)
            return Response({'error': 'Task creation failed'}, status=status.HTTP_400_BAD_REQUEST)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [IsAuthenticated]


    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response({'message': 'Task deleted successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error",e)
            return Response({'error': 'Task deletion failed'}, status=status.HTTP_400_BAD_REQUEST)
