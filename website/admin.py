from django.contrib import admin
from .models import Task, UserProfile, StudySessionMessage

admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(StudySessionMessage)
