from django.db import models
from profiles.models import Profile
from groups.models import Group
# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owning_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}, task for {self.owning_group}'

    class Meta:
        ordering = ['-created_at']
        # maybe add a unique together field with task creator and owning_group?

    