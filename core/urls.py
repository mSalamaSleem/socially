from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', profile, name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('account_settings/', ProfileSettingUpdateView.as_view(), name='account_settings'),
    path('posts/new/', PostCreationView.as_view(), name='new_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
