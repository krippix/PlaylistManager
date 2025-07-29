from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SpotifyCredentials(models.Model):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    token_info = models.JSONField()
