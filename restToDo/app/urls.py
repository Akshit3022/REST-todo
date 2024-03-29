from django.urls import path
from .views import *

urlpatterns = [
    path('api/restricted/', RestrictedView.as_view(), name='restricted'),
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', CustomUserCRUD.as_view(), name='adminDash'),
    path('task-details/<int:id>', TaskDetails.as_view(), name='task-details'),
    path('tasks/', TaskAPIView.as_view(), name='home'), 
    path('tasks/<int:id>/complete/', TaskCompleteAPIView.as_view(), name='complete-task'),
    path('tasks/<int:id>/delete/', TaskDeleteAPIView.as_view(), name='delete-task'),
    path('logout/', LogOutAPIView.as_view(), name='logout'), 
]
