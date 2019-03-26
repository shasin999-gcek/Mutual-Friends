from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Friend(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
  friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend")

  def __str__(self):
    return str('User ' + self.user.username + ' is Friend with ' + self.friend.username)


class FriendRequest(models.Model):
  from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
  to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")

  def __str__(self):
      return "User " + self.from_user.username + " Sent a friend request to " + self.to_user.username
  
