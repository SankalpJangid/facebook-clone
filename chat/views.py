from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from fbclone.models import ProfilePic, Posts, Friend, Relationship, blogComment, Message
import json

# Create your views here.
def index(request):
    return render(request, 'chat/index.html')

def room(request, room_name):
    friend = Friend.objects.get(chat=room_name)
    print(friend.sender)
    print(friend.receiver)
    if request.user == friend.sender:
        other_name = friend.receiver
        other = ProfilePic.objects.get(user=friend.receiver)
    else:
        other_name = friend.sender
        other = ProfilePic.objects.get(user=friend.sender)

    pic = ProfilePic.objects.get(user=request.user)
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'room': room_name,
        'pic':pic,
        'other':other,
        'other_name':other_name,
    })
