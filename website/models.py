from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage
from django.core.validators import FileExtensionValidator
from django.db.models import F


class UserProfile(models.Model):
    """
    class responsible with the additional information for a User model 
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, blank=True, related_name='user_profile')
    country = models.CharField(max_length=60, null=True, blank=True)
    description = models.CharField(max_length=600, null=True, blank=True)
    profile_picture = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to='profile_pictures/',
        null=True, blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])


class Task(models.Model):
    """
    class responsible with the details about a task from to-do list
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    create = models.DateTimeField(
        auto_now_add=True, null=False, blank=True)
    deadline = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        # setting a priority to the tasks that are not completed yet
        # the tasks that are marked as completed will be shown in the bottom section of the tasks list
        ordering = ['is_complete', F('deadline').asc(nulls_last=True)]


class StudySessionMessage(models.Model):
    """
    class responsible with the details about a message from a study session room
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True
    )
    group_name = models.CharField(max_length=30, null=False, blank=True)
    message_content = models.TextField(null=False, blank=True)
    create = models.DateTimeField(
        auto_now_add=True, null=False, blank=True
    )

    def __str__(self):
        return self.message_content

    class Meta:
        ordering = ['create']


class FriendRequest(models.Model):
    """
    class responsible with the details about a friend request
    """
    class RequestStatus(models.TextChoices):
        PENDING = "pending",
        ACCEPTED = "accepted",
        REJECTED = "rejected"

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True, related_name="request_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True, related_name="request_receiver")
    status = models.CharField(
        max_length=8,
        null=False, blank=True,
        choices=RequestStatus,
        default=RequestStatus.PENDING
    )
    create = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    def __str__(self):
        return f"Request sent by {self.sender} to {self.receiver} has the status: {self.status}"


class Friendship(models.Model):
    """
    class responsible with the details about a friendship between two users
    the friendship is bidirectional
    """

    user_1 = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True, related_name="friendship_user_1"
    )
    user_2 = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True, related_name="friendship_user_2"
    )
    create = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    def __str__(self):
        return f"{self.user_1.username} is friend with {self.user_2.username}"


class FlashcardsFolder(models.Model):
    """
    class responsible with the details about a flashcards folder
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True)
    name = models.CharField(max_length=128, null=False, blank=False)
    flashcards_number = models.PositiveIntegerField(
        default=0, null=False, blank=True)
    create = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    """
    class responsible with the details about a flashcard
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=True
    )
    folder = models.ForeignKey(
        FlashcardsFolder, on_delete=models.CASCADE, null=False, blank=False
    )
    front_side_text = models.TextField(null=False, blank=False)
    back_side_text = models.TextField(null=False, blank=False)
    create = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    def __str__(self):
        return self.front_side_text
