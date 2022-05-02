from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list_api'),
]
