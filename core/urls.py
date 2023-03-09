"""
Here we have all the API Urls
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', Signup, name="signup"),
] 
