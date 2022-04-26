from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('profile', PostsListView.as_view(), name='profile'),
    path('user/<str:username>', FriendProfileView.as_view(), name='friend-profile'),
    path('posts/new/', PostCreationView.as_view(), name='new_post'),
    path('search/', SearchResult.as_view(), name='search'),
    path('follow/<int:pk>', follow_user, name='follow'),
    path('unfollow/<int:pk>', unfollow_user, name='unfollow'),

]
