from django.urls import path
from .views import *

urlpatterns = [
    path('restricted/', RestrictedView.as_view(), name='restricted'),
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', CustomUserCRUD.as_view(), name='user-list'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task-operation'),
]
