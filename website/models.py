from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    class responsible with the details about a task from to-do list
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        # setting a priority to the tasks that are not completed yet
        # the tasks that are marked as completed will be shown in the bottom section of the tasks list
        ordering = ['is_complete']
