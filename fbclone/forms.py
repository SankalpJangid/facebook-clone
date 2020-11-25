from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django import forms

class Profile_Update(ModelForm):
    class Meta:
        model = ProfilePic
        fields = '__all__'
        exclude = ['user']