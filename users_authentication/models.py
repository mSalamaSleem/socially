from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import *


class User(AbstractUser):
    profile_pic = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True, max_length=200, default='')

    def get_num_posts(self):
        return Post.objects.filter(user=self).count()

    def is_following(self, followed):
        return Friend.objects.filter(follower=self, followed=followed).count()
