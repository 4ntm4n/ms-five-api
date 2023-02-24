from django.db import models
from profiles.models import Profile

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    group_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, related_name="members")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.name}'