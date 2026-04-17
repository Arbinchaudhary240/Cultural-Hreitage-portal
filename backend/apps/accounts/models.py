import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.full_name
    
class Contribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contributer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions')
    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(upload_to='contributions/', blank=True, null=True)
    audio = models.FileField(upload_to='contributions/', blank=True, null=True)
    vedio = models.FileField(upload_to='contributions/', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title