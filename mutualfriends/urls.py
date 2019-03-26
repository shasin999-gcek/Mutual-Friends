from django.urls import path
from . import views

urlpatterns = [
  path('', views.index_view, name="index"),
  path('login/', views.login_view, name="login"),
  path('register/', views.register_view, name="register"),
  path('logout/', views.logout_view, name="logout"),
  path('myfriends/', views.myfriends_view, name="myfriends"),
  path('addfriends/', views.addfriends_view, name="addfriends"),
  path('friend/add/<user_id>', views.sent_friend_request_view, name="sentfriendrequest"),
  path('profile/<user_id>', views.profile_view, name="profile"),
  path('friendrequests/', views.friendrequests_view, name="friendrequests"),
  path('acceptfriend/<user_id>', views.accept_friend_view, name="acceptfriend"),
  path('rejectfriend/<user_id>', views.reject_friend_view, name="rejectfriend"),
]