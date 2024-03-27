from django.urls import path
from .views import *

urlpatterns = [
    path('api/restricted/', RestrictedView.as_view(), name='restricted'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('users/', CustomUserRetrieveUpdateDestroyAPIView.as_view(), name='user-list'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-detail'),
]
