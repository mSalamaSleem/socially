from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', profile, name='profile'),
    path('account_settings/', ProfileSettingUpdateView.as_view(), name='account_settings'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
