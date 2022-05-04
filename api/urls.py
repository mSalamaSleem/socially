from django.urls import path

from .views import *

urlpatterns = [
    # Posts
    path('', FriendsPostsList.as_view(), name='friends_posts_list_api'),
    path('profile/posts', UserPostsList.as_view(), name='user_posts_list_api'),
    path('profile/posts/<int:pk>', UserPostDetails.as_view(), name='user_posts_detail_api'),
    path('friends', FriendsList.as_view(), name='friends_list_api'),
    path('friends/<str:username>', FriendPostsList.as_view(), name='friend_posts_list_api_profile'),
    path('search/<str:key_to_search>', SearchResultsList.as_view(), name='search_api'),
    path('follow/<int:pk>', Follow.as_view(), name='follow_api'),
    path('unfollow/<int:pk>', UnFollow.as_view(), name='unfollow_api'),

    # Auth
    path('signup', signup),
    path('login', login),
]

