from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_pic = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True, max_length=200, default='')


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.caption
