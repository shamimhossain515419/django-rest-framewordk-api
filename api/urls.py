from home.views import index 
from home.views import person 

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('index/', index),
    path('person/', person),  # Ensure the trailing slash is here
]