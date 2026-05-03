import uuid
from django.db import models
from django.conf import settings

class Contribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    contributer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    image = models.ImageField(upload_to='contributions/', blank=True, null=True)
    audio = models.FileField(upload_to='contributions/', blank=True, null=True)
    vedio = models.FileField(upload_to='contributions/', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.title