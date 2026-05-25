from django.db import models
from django.utils.text import slugify

class EthnicityProfile(models.Model):
    """
    A unified hierarchical model designed to classify Religion, Caste, and Subcaste
    efficiently within a single table using parent-child nodes.
    """
    NODE_TYPES = (
        ('religion', 'Religion'),
        ('caste', 'Caste/Ethnic Group'),
        ('subcaste', 'Subcaste/Clan/Thang'),
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    node_type = models.CharField(max_length=15, choices=NODE_TYPES)
    
    # The magical self-referencing link that builds the tree structure
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='children',
        help_text="For a Caste, select its dominant Religion. For a Subcaste, select its Caste."
    )
    
    historical_background = models.TextField(blank=True, help_text="Brief origin story of this demographic node.")

    class Meta:
        verbose_name = "Demographic Profile"
        verbose_name_plural = "Demographic Profiles"
        ordering = ['node_type', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"