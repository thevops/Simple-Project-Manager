from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    # user = models.CharField(max_length=30, verbose_name="Nadawca")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Nadawca")
    message = models.TextField(verbose_name="treść")
    timestamp = models.DateTimeField(verbose_name="Data utworzenia", default=timezone.now)