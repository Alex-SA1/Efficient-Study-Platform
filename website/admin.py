from django.contrib import admin
from .models import Task, UserProfile, StudySessionMessage, FriendRequest

admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(StudySessionMessage)
admin.site.register(FriendRequest)
