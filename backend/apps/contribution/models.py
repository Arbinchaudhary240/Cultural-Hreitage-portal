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
    description = models.TextField(1000)

    image = models.ImageField(upload_to='contributions/', blank=True, null=True)
    audio = models.FileField(upload_to='contributions/', blank=True, null=True)
    video = models.FileField(upload_to='contributions/', blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True)
    # is_verified = models.BooleanField(default=False)
    PENDING = 'P'
    APPROVED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.title