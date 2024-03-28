from django.urls import path
from .views import *

urlpatterns = [
    # path('api/restricted/', RestrictedView.as_view(), name='restricted'),
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', CustomUserCRUD.as_view(), name='user'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='home'),   
    path('tasks/<int:id>/', TaskDestroyAPIView.as_view(), name='task-detail'),
    path('logout/', LogOutAPIView.as_view(), name='logout'), 
]
