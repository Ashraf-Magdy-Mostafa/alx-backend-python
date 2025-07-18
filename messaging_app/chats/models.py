import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max=255)
    last_name = models.CharField(max=255)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
