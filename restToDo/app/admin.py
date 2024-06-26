from django.contrib import admin
from . models import *

# Register your models here.
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ["userName", "userEmail", "userPassword"]
admin.site.register(CustomUser, CustomUserModelAdmin)

class TaskModelAdmin(admin.ModelAdmin):
    list_display = ["task_id", "taskDate", "taskName", "taskDescription", "taskStatus"]
admin.site.register(Task, TaskModelAdmin)