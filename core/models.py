from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_pic = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True, max_length=200, default='')

    def get_num_posts(self):
        return Post.objects.filter(user=self).count()

    def is_following(self, followed):
        return Friend.objects.filter(follower=self, followed=followed).count()


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.caption


class Friend(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followings')
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return f"{self.follower} following {self.followed}"
