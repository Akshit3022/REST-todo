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
    def get(self, request):
        # Rendering the HTML template for GET requests
        return render(request, 'register.html')
    def post(self, request):

        userName = request.data.get('userName')
        userEmail = request.data.get('userEmail')
        userPassword = make_password(request.data.get('userPassword'))

        # url = requests.get('').json()

        if not userName or not userEmail or not userPassword:
            return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(userName=userName).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(userEmail=userEmail).exists():
            return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create(userName=userName, userEmail=userEmail, userPassword=userPassword)
        user.save()
        return redirect('login')

        # serializer = CustomUserSerializer(data=request.data)
        # if serializer.is_valid():
        #     password = make_password(serializer.validated_data['userPassword'])
        #     serializer.validated_data['userPassword'] = password
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return render(request, 'register.html') 


# class RegisterView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = make_password(request.data.get('password'))

#         if not username or not email or not password:
#             return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(username=username).exists():
#             return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.create(username=username, email=email, password=password)
#         if user:
#             return render(request, 'register.html')
#             # return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class RestrictedView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, format=None):
#         userName = request.data.get('userName')
#         userPassword = request.data.get('userPassword')

#         user = authenticate(username=userName, password=userPassword)
#         print("USER", user)
    
#         return JsonResponse({"response": "You are Allowed here"})


class LoginView(APIView):
    # def post(self, request):
    #     username = request.data.get('username')
    #     password = request.data.get('password')
    #     print("userPassword", password)
    #     user = authenticate(username=username, password=password)
    #     print("USER", user)
    #     if user is not None:
    #         refresh = RefreshToken.for_user(user)
    #         return JsonResponse({
    #             'refresh': str(refresh),
    #             'access': str(refresh.access_token)
    #         })
    #     else:
    #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # try:
        #     loginUser = CustomUser.objects.get(userEmail=userEmail)
        # except Exception as e:
        #     loginUser = None

        # if CustomUser.objects.filter(userEmail=userEmail).exists() and check_password(userPassword, loginUser.userPassword):
        #     request.session['email'] = userEmail
        #     return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        # else:
        #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):

        userEmail = request.data.get('userEmail')
        userPassword = request.data.get('userPassword')

        try:
            loginUser = CustomUser.objects.get(userEmail=userEmail)
        except Exception as e:
            loginUser = None

        # user = request.user
        # print("user", user)

        # print("check_password", check_password(userPassword, loginUser.userPassword))
        if loginUser is not None and check_password(userPassword, loginUser.userPassword):
            print("-------------------------------")
            request.session['email'] = userEmail
            return redirect('home')
        elif userEmail=='admin@gamil.com':
            request.session['email'] = userEmail
            return redirect('adminDash')
        else:
            request.session['email'] = userEmail
            return redirect('home')
            return render(request,'login.html')



class CustomUserCRUD(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request):
        allUser = CustomUser.objects.all()
        return render(request, 'adminDash.html', {'allUser':allUser})

# class TaskListCreateAPIView(APIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     # permission_classes = [IsAuthenticated]

#     def get(self, request):
#         logedUserTask = Task.objects.filter(user_id__userEmail=request.session['email'])
#         return render(request, 'home.html', {'logedUserTask':logedUserTask})

#     def post(self, request):
#         taskDate = datetime.datetime.now()
#         taskName = request.data.get('taskName')
#         taskDescription = request.data.get('taskDescription')
#         loggedUser = request.session['email']
#         user_instance = CustomUser.objects.get(userEmail=loggedUser)

#         task = Task(user_id=user_instance, taskDate=taskDate, taskName=taskName, taskDescription=taskDescription)
#         task.save()
#         return redirect ('home')


class LogOutAPIView(APIView):
    def get(self, request):
        del request.session['email']
        return redirect('login')

# class TaskDestroyAPIView(APIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     # permission_classes = [IsAuthenticated]

#     def post(self, request, id):
#         Task.objects.filter(userEmail=request.session['email'])
#         return render(request, 'home.html')
    
#     def patch(self, request, id):

#         task = Task.objects.get(id=id)
#         task.taskStatus = True

#         status = "Completed"
#         return render(request, 'home.html', {'status': status})

#     def delete(self, request, id):

#         task = Task.objects.get(id=id)
#         task.delete()
#         return redirect('home')


class TaskAPIView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request):
        # Retrieve tasks for the logged-in user
        logedUserTask = Task.objects.filter(user_id__userEmail=request.session.get('email'))
        return render(request, 'home.html', {'logedUserTask': logedUserTask})

    def post(self, request):
        # Create a new task
        taskDate = datetime.datetime.now()
        taskName = request.data.get('taskName')
        taskDescription = request.data.get('taskDescription')
        loggedUser = request.session.get('email')
        user_instance = CustomUser.objects.get(userEmail=loggedUser)

        task = Task(user_id=user_instance, taskDate=taskDate, taskName=taskName, taskDescription=taskDescription)
        task.save()
        return redirect('home')

    # def patch(self, request, id):
    #     # Update task status to completed
    #     task = Task.objects.get(id=id)
    #     task.taskStatus = True
    #     task.save()
    #     status = "Completed"
    #     return render(request, 'home.html', {'status': status})

    # def delete(self, request, id):
    #     # Delete task
    #     task = Task.objects.get(id=id)
    #     task.delete()
    #     return redirect('home')
class TaskDetails(APIView):
    def get(self, request, id):
        tasks = Task.objects.filter(user_id__user_id=id)
        return render(request, 'displayTask.html', {'tasks': tasks})    

class TaskCompleteAPIView(APIView):
    def post(self, request, id):
        # Update task status to completed
        task = Task.objects.get(task_id=id)
        task.taskStatus = True
        task.save()
        return redirect('home')
    
class TaskDeleteAPIView(APIView):
    def post(self, request, id):
        # Delete task
        task = Task.objects.get(task_id=id)
        task.delete()
        return redirect('home')