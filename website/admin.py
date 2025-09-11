from django.contrib import admin
from .models import Task, UserProfile, StudySessionMessage, FriendRequest, Friendship, FlashcardsFolder, Flashcard

admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(StudySessionMessage)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(FlashcardsFolder)
admin.site.register(Flashcard)
