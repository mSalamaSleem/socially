from operator import mod
from django.db import models
from socially import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    name = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=40, null=False, blank=False)
    ismember = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} subscribe successfully"
