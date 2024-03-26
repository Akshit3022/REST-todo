import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Task
from .serializers import CustomUserSerializer, TaskSerializer
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password


class CustomUserRegisterAPIView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(serializer.validated_data['userPassword'])
            serializer.validated_data['userPassword'] = password
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomUserLoginAPIView(APIView):
    def post(self, request):
        userEmail = request.data.get('userEmail')
        userPassword = request.data.get('userPassword')

        try:
            loginUser = CustomUser.objects.get(userEmail=userEmail)
        except Exception as e:
            loginUser = None

        if CustomUser.objects.filter(userEmail=userEmail).exists() and check_password(userPassword, loginUser.userPassword):
            request.session['email'] = userEmail
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CustomUserRetrieveUpdateDestroyAPIView(generics.ListCreateAPIView):
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
        loggedUser = request.session['email']
        user_instance = CustomUser.objects.get(userEmail=loggedUser)

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

    def post(self, request):
        Task.objects.filter(userEmail=request.session['email'])

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response({'message': 'Task deleted successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("error",e)
            return Response({'error': 'Task deletion failed'}, status=status.HTTP_400_BAD_REQUEST)
