from django.contrib import admin
from .models import Issue

class IsssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Issue, IsssueAdmin)