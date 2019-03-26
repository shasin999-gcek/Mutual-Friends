from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Friend, FriendRequest
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse

# Create your views here.

def index_view(request):
  return render(request, 'index.html')

  
def login_view(request):
  if request.method == 'GET':
    return render(request, 'login.html')
  else:
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect(myfriends_view)
    else:
      return HttpResponse('login failed') 


def register_view(request):
  if request.method == 'GET':
    return render(request, 'register.html')
  else:
    firstname = request.POST['firstname']
    lastname = request.POST['lastname'] 
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create_user(username, email, password)
    user.first_name = firstname
    user.last_name = lastname
    user.save()

    return redirect(login_view)


def logout_view(request):
  if request.method == 'GET':
    logout(request)
    return redirect(login_view)  


def myfriends_view(request):
  if request.user.is_authenticated:
    friends = Friend.objects.filter(friend=request.user)
    return render(request, 'myfriends.html', {"friends" : friends})
  return redirect(login_view)  

def addfriends_view(request):
  if request.user.is_authenticated:
    # we need to exclude friends
    exclude_list = list(Friend.objects.filter(friend=request.user).values_list('user_id', flat=True))

    # exclude sent requests
    exclude_list.extend(list(FriendRequest.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)))

    #exclude received requests
    exclude_list.extend(list(FriendRequest.objects.filter(to_user=request.user).values_list('from_user_id', flat=True)))

    #exclude current login user
    exclude_list.append(request.user.id)

    addfriends = User.objects.exclude(id__in=exclude_list)
    return render(request, 'addfriends.html', {"addfriends": addfriends})
  return redirect(login_view)


def sent_friend_request_view(request, user_id):
  if request.user.is_authenticated:
    to_user = User.objects.get(pk=user_id)
    FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect(addfriends_view)
  return redirect(login_view)  


def profile_view(request, user_id):
  if request.user.is_authenticated:
    userInfo = User.objects.get(pk=user_id)
    userFriends = list(Friend.objects.filter(friend=userInfo))
    auth_user_friends = list(Friend.objects.filter(friend=request.user))
    mutualfriends = []

    # find mutual friends
    for f1 in auth_user_friends:
      for f2 in userFriends:
        if f1.user.id == f2.user.id:
          mutualfriends.append(f1.user)

    data = { 
      "profileInfo": userInfo,
      "friends": userFriends,
      "mutualfriends": mutualfriends
    }

    return render(request, 'profile.html', data)
        
  return redirect(login_view)  

def friendrequests_view(request):
  if request.user.is_authenticated:
    sented = FriendRequest.objects.filter(from_user=request.user)
    received = FriendRequest.objects.filter(to_user=request.user)
    data = { "sented": sented, "received": received }
    return render(request, "friendrequests.html", data)
  return redirect(login_view)  

def accept_friend_view(request, user_id):
  if request.user.is_authenticated:
    friend = User.objects.get(pk=user_id)

    # adding friends
    Friend.objects.create(user=request.user, friend=friend)
    Friend.objects.create(user=friend, friend=request.user)

    # delete friend request
    FriendRequest.objects.filter(from_user=friend, to_user=request.user).delete() 
    return redirect(friendrequests_view)  
  return redirect(login_view)    
  

def reject_friend_view(request, user_id):
  if request.user.is_authenticated:
    user = User.objects.get(pk=user_id)

    # delete friend request
    FriendRequest.objects.filter(from_user=user, to_user=request.user).delete() 
    return redirect(friendrequests_view)  
  return redirect(login_view)     
