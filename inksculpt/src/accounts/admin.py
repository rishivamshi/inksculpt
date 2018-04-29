from django.contrib import admin

# Register your models here.

from .models import UserProfile


admin.site.register(UserProfile) #1


'''
#1 - adding the user profile from the models.py


'''