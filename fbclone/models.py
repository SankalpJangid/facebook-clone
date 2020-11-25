from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class ProfilePic(models.Model):
      sno = models.AutoField(primary_key=True)
      img = models.ImageField(default="user_image.jpg", null=True, blank=True)
      cover_image = models.ImageField(default="default_LY4bxuY.jpg", null=True, blank=True, upload_to='cover_image')
      user = models.ForeignKey(User, on_delete=models.CASCADE)

      def __str__(self):
          return str(self.sno)
      

class Posts(models.Model):
    sno = models.AutoField(primary_key=True)
    post_title = models.TextField()
    post_image = models.ImageField(null=True, blank=True, upload_to='post_image')
    post_user = models.ForeignKey(User ,on_delete=models.CASCADE)
    post_likes = models.ManyToManyField(User, related_name="post_likes")
    
    def __str__(self):
        return self.post_title
    
class Friend(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    
    def __str__(self):
        return str(self.sender)
    

class Relationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    friend = models.ManyToManyField(User)


class blogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:12] + "...." +  " by " + self.user.username


class Message(models.Model):
    sno = models.AutoField(primary_key=True)
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_sender")
    message_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_receiver")
    message_field = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.message_sender) + " to " + str(self.message_receiver)
    

    