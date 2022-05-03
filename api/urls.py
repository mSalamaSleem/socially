from django.urls import path
from .views import *

urlpatterns = [
    path('', FriendsPostsList.as_view(), name='friends_posts_list_api'),
    path('profile/posts/', UserPostsList.as_view(), name='user_posts_list_api'),
    path('profile/posts/<int:pk>', UserPostDetails.as_view(), name='user_posts_detail_api'),
    path('friends/', FriendsList.as_view(), name='friends_list_api'),
    path('friends/<str:username>', FriendPostsList.as_view(), name='friend_posts_list_api-profile'),
]
