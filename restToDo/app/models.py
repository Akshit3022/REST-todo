from django.db import models

# Create your models here.

class CustomUser(models.Model):
    user_id = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    userEmail = models.EmailField()
    userPassword = models.CharField(max_length=100)

class Task(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    taskDate = models.DateField()
    taskName = models.CharField(max_length=300)
    taskDescription = models.TextField()
    taskStatus = models.BooleanField(default=False)