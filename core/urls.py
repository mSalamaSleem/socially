from django.urls import path
from .views import *

urlpatterns = [
    path('', profile, name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
]
