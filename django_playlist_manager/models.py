from django.conf import settings
from django.db import models


class SpotifyCredentials(models.Model):
    django_user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE)
    token_info = models.JSONField()
