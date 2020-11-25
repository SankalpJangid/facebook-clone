from django.contrib import admin
from .models import ProfilePic, Posts, Friend, Relationship, blogComment, Message

# Register your models here.
admin.site.register((ProfilePic, Posts, Friend, Relationship, blogComment, Message))