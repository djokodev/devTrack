from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared', 'created_time')

admin.site.register(User, UserAdmin) 
