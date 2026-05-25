from django.db import models
import uuid
from apps.contribution.models import Contribution

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    
class HeritageItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    official_name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    contribution = models.OneToOneField(
        Contribution,
        on_delete=models.CASCADE,
        limit_choices_to={"status" : "approved"}
        )
    metadata = models.JSONField(default=dict, blank=True)
    
    community_tags = models.ManyToManyField(
        'sanskriti.EthnicityProfile',
        related_name='heritage_items',
        blank=True,
        help_text="Tag which religions, castes, or subcastes this heritage item belongs to."
    )