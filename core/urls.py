from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsListView.as_view(), name='profile'),
    path('user/<str:username>', FriendProfileView.as_view(), name='friend-profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('account_settings/', ProfileSettingUpdateView.as_view(), name='account_settings'),
    path('posts/new/', PostCreationView.as_view(), name='new_post'),

    # path('search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
