from django.db import models
from profiles.models import Profile
from groups.models import Group

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owning_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}, task for {self.owning_group}'

    class Meta:
        ordering = ['-created_at']
        unique_together = ('owning_group', 'title')
