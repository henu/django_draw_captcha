from django.contrib import admin

from .models import Task, Picture


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'secret', 'created_at', 'task_type', 'adjective', 'noun', 'valid_pictures', 'invalid_pictures']


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ['img', 'created_at', 'adjective', 'noun', 'valid_identifications', 'failed_identifications']
