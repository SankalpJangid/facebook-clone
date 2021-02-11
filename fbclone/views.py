from django.shortcuts import render,HttpResponse,redirect, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .models import ProfilePic, Posts, Friend, Relationship, blogComment, Message
from .forms import Profile_Update
from django.http import JsonResponse
import random

# Create your views here.
@login_required(login_url="login_user")
def home(request):
    alldata = ProfilePic.objects.all()
    all_users = []
    for data in alldata:
        all_users.append(data.user)
    
    if request.user not in all_users:
        profile = ProfilePic.objects.create(user=request.user)
    
    # profile_user = ProfilePic.objects.filter(user=request.user)
    # print(ProfilePic.objects.filter(user=request.user))
    # if request.user not in ProfilePic.objects.filter(user=request.user):
    # profile = ProfilePic.objects.create(user=request.user)
    friends, created = Relationship.objects.get_or_create(user=request.user)
    new_friends = friends.friend.all()
    #print(new_friends)

    user_specific_post = []
    for i in new_friends:
        user_specific_post.append(i.id)

    second_parameter = len(user_specific_post)
    random_generate_list = random.sample(user_specific_post,second_parameter)
    #print(random_generate_list)
    # print(len(user_specific_post[0]))
    # print(type(user_specific_post))
    # user_specific_post = Posts.objects.filter(post_user=11)
    # Relationship.objects.filter(User__firstname__in=user_specific_post)
    my_data = Posts.objects.filter(post_user__in=random_generate_list)
    my_data_profile_pic = ProfilePic.objects.filter(user__in=random_generate_list)
    #print(my_data)

    sankalp = []
    for i in my_data:
        sankalp.append(i)

    my_generated_post_list = random.sample(sankalp, len(sankalp))
    checkAnyMessage = []
    listOfReceiver = Message.objects.values_list('message_receiver', flat=True)
    for i in listOfReceiver:
        checkAnyMessage.append(User.objects.get(id=i))

    profile_pic = ProfilePic.objects.filter(user__in=user_specific_post)
    user_image = ProfilePic.objects.filter(user=request.user)
    print(my_generated_post_list)
    if request.user in checkAnyMessage:
        message_receiving = Message.objects.filter(message_receiver=request.user)
        notification_number = message_receiving.count()
        context = {'new_friends':new_friends, 'user_specific_post':user_specific_post, 'my_data':my_data, 'user_image':user_image, 'profile_pic':profile_pic, 'message_receiving':message_receiving, 'notification_number':notification_number, 'my_data_profile_pic':my_data_profile_pic, 'my_generated_post_list':my_generated_post_list}
        return render(request,"base.html", context)
    else:
        context = {'new_friends':new_friends, 'user_specific_post':user_specific_post, 'my_data':my_data, 'user_image':user_image, 'profile_pic':profile_pic, 'my_data_profile_pic':my_data_profile_pic, 'my_generated_post_list':my_generated_post_list}
        return render(request,"base.html", context)

def notification(request):
    checkAnyMessage = []
    listOfReceiver = Message.objects.values_list('message_receiver', flat=True)
    user_image = ProfilePic.objects.filter(user=request.user)
    for i in listOfReceiver:
        checkAnyMessage.append(User.objects.get(id=i))
    
    if request.user in checkAnyMessage:
        message_receiving = Message.objects.filter(message_receiver=request.user)
        notification_number = message_receiving.count()
        context = {'message_receiving':message_receiving, 'notification_number':notification_number, 'user_image':user_image}
        return render(request, "notification.html", context)
    
    else:
        return render(request, "notification.html", {'user_image':user_image})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginPassword']
    
        User = auth.authenticate(username=username,password=password)
        if User is not None:
            auth.login(request, User)
            return redirect("/")
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login_user')
          
    else:
     return render(request=request,
                   template_name = "login.html"
                      )

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,'email taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request,'email taken')
            return redirect('signup')
        elif len(password) < 8:
            messages.error(request, 'password must be 8 character long')
            return redirect('signup')   
        else:   
          user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
          user.save()
          return redirect('login_user')
    else:
        
     return render(request = request,
                  template_name = "signup.html"
                  )               

def logout(request):
    auth.logout(request)
    return redirect('/')  

def search(request):
    query = request.GET['search']
    profile = []
    if len(query) > 70:
        pass
    else:
        username = User.objects.filter(username__icontains=query)
        # profile = ProfilePic.objects.filter(user__icontains=query)
        # print(profile)
        print(username)
    for i in username:
        profile += ProfilePic.objects.filter(user=i)
    
    print(len(username))
    user_image = ProfilePic.objects.filter(user=request.user)
    context = {'username':username, 'profile':profile, 'user_image':user_image, 'query':query}
    return render(request, 'search.html',context)

def profile(request):
    alldata = ProfilePic.objects.filter(user=request.user)
    if request.method == "POST":
        post_title = request.POST.get('post_title')
        image = request.FILES['post_image']
        data = Posts.objects.create(post_title = post_title, post_image = image, post_user=request.user)
        data.save()
        return redirect('profile')

    friends, created = Relationship.objects.get_or_create(user=request.user)
    new_friends = friends.friend.all()
    print(new_friends)

    user_specific_post = []
    for i in new_friends:
        user_specific_post.append(i.id)


    profile_pic = ProfilePic.objects.filter(user__in=user_specific_post)
    post_data = Posts.objects.filter(post_user=request.user)
    user_image = ProfilePic.objects.filter(user=request.user)
    context = {'alldata':alldata,'post_data':post_data, 'new_friends':new_friends, 'user':request.user, 'user_image':user_image, 'profile_pic':profile_pic}
    return render(request,"profile_page.html", context)

def profile_update(request, id):
    if request.method == "POST":
        form = ProfilePic.objects.get(sno=id)
        form.img = request.FILES['myfile']
        form.save()
        return redirect('profile')
    else:
        return HttpResponse('404')

def update_cover(request, id):
    if request.method == "POST":
        form = ProfilePic.objects.get(sno=id)
        form.cover_image = request.FILES['cover_file']
        form.save()
        return redirect('profile')
    else:
        return HttpResponse('404')

def delete_post(request, id):
    data = Posts.objects.get(sno=id)
    data.delete()
    return redirect('profile')

# def afterSearch(request, id):
#     alldata = ProfilePic.objects.filter(user=id)
#     post_data = Posts.objects.filter(post_user=id)
#     print(alldata)
#     print(post_data)
#     friends, created = Relationship.objects.get_or_create(user=request.user)
#     new_friends = friends.friend.all()
#     context = {'alldata':alldata, 'post_data':post_data, 'new_friends':new_friends}
#     return render(request, "afterSearch.html", context)


#send ,accept, delete request

# def second_home(request):
#     alluser = User.objects.exclude(username=request.user)
#     request_check = Friend.objects.filter(receiver=request.user)
#     print(Friend.objects.all())
#     print(request_check)
#     friends, created = Relationship.objects.get_or_create(user=request.user)
#     friendssss = friends.friend.all()
#     print(friendssss)
#     context = {'alluser':alluser, 'request_check':request_check, 'friendssss':friendssss}
#     return render(request, "second_home.html", context)

def add_friend(request, id):
    receiver = User.objects.get(id=id)
    print(receiver)
    create_friend = Friend.objects.create(sender=request.user, receiver=receiver)
    print(create_friend)
    messages.success(request,"friend request successfully sent")
    return redirect(f"/afterSearch/{id}")

def accept_friend(request, id):
    user = request.user
    friends = User.objects.get(id=id)
    friend_request, created = Relationship.objects.get_or_create(user=user)
    friend_request.friend.add(friends)
    friend_request, created = Relationship.objects.get_or_create(user=friends)
    friend_request.friend.add(user)
    messages.success(request,"friend request successfully accepted")
    return redirect("friendRequest")




def blogPost(request,id):
    alldata = Posts.objects.filter(post_user=id)
    profile = ProfilePic.objects.filter(user=id)
    name = User.objects.get(id=id)
    friends, created = Relationship.objects.get_or_create(user=name)
    new_friends = friends.friend.all()
    check_friend = []
    for i in new_friends:
        check_friend.append(i)  

    user_specific_post = []
    for i in new_friends:
        user_specific_post.append(i.id)

    profile_pic = ProfilePic.objects.filter(user__in=user_specific_post) 

    receiver = User.objects.get(id=id)
    request_status = Friend.objects.filter(sender=request.user, receiver=receiver)
    check_friend_request = []
    for i in request_status:
        check_friend_request.append(str(i))

    print(check_friend_request)
   
    current_user = str(request.user)
    user_image = ProfilePic.objects.filter(user=request.user)

    checkAnyMessage = []
    listOfReceiver = Message.objects.values_list('message_receiver', flat=True)
    for i in listOfReceiver:
        checkAnyMessage.append(User.objects.get(id=i))
    
    if request.user in checkAnyMessage:
        message_receiving = Message.objects.filter(message_receiver=request.user)
        notification_number = message_receiving.count()
        context = {'alldata':alldata, 'user':request.user, 'profile':profile, 'new_friends':new_friends, 'check_friend':check_friend, 'profile_pic':profile_pic, 'request_status':request_status, 'check_friend_request':check_friend_request, 'current_user':current_user, 'user_image':user_image, 'notification_number':notification_number, 'id':id}
        return render(request, "afterSearch.html",context)

    else:
        context = {'alldata':alldata, 'user':request.user, 'profile':profile, 'new_friends':new_friends, 'check_friend':check_friend, 'profile_pic':profile_pic, 'request_status':request_status, 'check_friend_request':check_friend_request, 'current_user':current_user, 'user_image':user_image, 'id':id}
        return render(request, "afterSearch.html",context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comments")
        user = request.user
        postSno = request.POST.get('postSno')
        post = Posts.objects.get(sno=postSno)
        parentsno = request.POST.get('parentsno')
        if parentsno == "":
            commenting = blogComment(comment=comment,user=user,post=post)
            commenting.save()
            messages.success(request,"Your Comment Posted Successfully")
        else:
            parent = blogComment.objects.get(sno=parentsno)
            commenting = blogComment(comment=comment,user=user,post=post,parent=parent)
            commenting.save()
            messages.success(request,"Your Reply has been Posted Successfully")

    return redirect(f'comment/{post.sno}')


def comment(request, sno):
    post = Posts.objects.filter(sno=sno).first()
    print(post)
    comments = blogComment.objects.filter(post=post,parent=None)
    replies = blogComment.objects.filter(post=post).exclude(parent=None)
    replydict = {}
    for reply in replies:
        if reply.parent.sno not in replydict.keys():
            replydict[reply.parent.sno] = [reply]
        else:
            replydict[reply.parent.sno].append(reply)

    user_image = ProfilePic.objects.filter(user=request.user)
    checkAnyMessage = []
    listOfReceiver = Message.objects.values_list('message_receiver', flat=True)
    for i in listOfReceiver:
        checkAnyMessage.append(User.objects.get(id=i))
    
    if request.user in checkAnyMessage:
        message_receiving = Message.objects.filter(message_receiver=request.user)
        notification_number = message_receiving.count()
        context = {'comments':comments, 'replydict':replydict, 'user':request.user, 'post':post, 'user_image':user_image, 'notification_number':notification_number}
        return render(request, "comment.html", context)

    else:
        context = {'comments':comments, 'replydict':replydict, 'user':request.user, 'post':post, 'user_image':user_image}
        return render(request, "comment.html", context)


def friendRequest(request):
    request_check = Friend.objects.filter(receiver=request.user)
    friends, created = Relationship.objects.get_or_create(user=request.user)
    new_friends = friends.friend.all()
    check_friend = []
    for i in new_friends:
        check_friend.append(i)

    user_image = ProfilePic.objects.filter(user=request.user)
    context = {'request_check':request_check, 'check_friend':check_friend, 'user_image':user_image}
    return render(request, 'friendRequest.html',context)



def Remove_friend(request,id):
    user1 = request.user
    user2 = User.objects.get(id=id)
    friends, created = Relationship.objects.get_or_create(user=user1)
    friends.friend.remove(user2)
    friends, created = Relationship.objects.get_or_create(user=user2)
    friends.friend.remove(user1)
    friend = Friend.objects.filter(sender=user1, receiver=user2) or Friend.objects.filter(sender=user2, receiver=user1)
    friend.delete()
    return redirect('profile')


def cancel_friend(request,id):
    user1 = request.user
    user2 = User.objects.get(id=id)
    friend = Friend.objects.filter(sender=user1, receiver=user2) or Friend.objects.filter(sender=user2, receiver=user1)
    friend.delete()
    messages.success(request,"friend request Declined")
    return redirect('friendRequest')

def cancel_friend_request(request,id):
    user1 = request.user
    user2 = User.objects.get(id=id)
    friend = Friend.objects.filter(sender=user1, receiver=user2) or Friend.objects.filter(sender=user2, receiver=user1)
    friend.delete()
    messages.success(request,"friend request Canceled")
    return redirect(f"/afterSearch/{id}")


def chat(request,id): 
    print(User.objects.get(id=id))
    user1 = request.user
    user2 = User.objects.get(id=id)
    message_sending, created = Message.objects.get_or_create(message_sender=request.user, message_receiver=user2)
    message_receiving, created = Message.objects.get_or_create(message_sender=user2, message_receiver=request.user)
    profile_picture = ProfilePic.objects.get(user=user2)
    user_image = ProfilePic.objects.filter(user=request.user)
    friend = Friend.objects.filter(sender=user1, receiver=user2) or Friend.objects.filter(sender=user2, receiver=user1)
    print(friend)

    context = {'id':id, 'message_sending':message_sending, 'message_receiving':message_receiving, 'user2':user2, 'profile_picture':profile_picture, 'friend':friend, 'user_image':user_image}
    return render(request, "chat.html", context)


def message_system(request, id):
    if request.method == "POST":
        user2 = User.objects.get(id=id)
        message_sender = Message.objects.get(message_sender=request.user, message_receiver=user2)
        text_message = request.POST.get('message')
        message_sender.message_field = text_message
        message_sender.save()
        print(text_message)
        return redirect(f'/chat/{id}')


def messageDelete(request, id):
    checkAnyMessage = []
    listOfReceiver = Message.objects.values_list('message_sender', flat=True)
    for i in listOfReceiver:
        checkAnyMessage.append(User.objects.get(id=i))
    
    if request.user in checkAnyMessage:
        message_receiving = Message.objects.filter(message_receiver=request.user)
        user2 = User.objects.get(id=id)
        delete_sending = Message.objects.get(message_sender=request.user, message_receiver=user2)
        delete_receive = Message.objects.get(message_sender=user2, message_receiver=request.user)
        delete_sending.delete()
        delete_receive.delete()
        return redirect('/')
    
    else:
        return redirect('/')


def likes(request, sno, id):
    get_post = Posts.objects.get(sno=sno)
    get_post.post_likes.add(request.user)
    print(id)
    return redirect("/")

def self_like(request,sno):
    get_post = Posts.objects.get(sno=sno)
    get_post.post_likes.add(request.user)
    return HttpResponseRedirect(reverse('profile'))

def common_like(request, sno):
    get_post = Posts.objects.get(sno=sno)
    get_post.post_likes.add(request.user)
    data = {
        'likes':get_post.post_likes.all().count()
    }
    return redirect("/")