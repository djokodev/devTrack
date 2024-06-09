from django.shortcuts import render
from rest_framework import generics, permissions, serializers
from .serializers import IssueSerializer
from .models import Issue
from project.models import Contributor

