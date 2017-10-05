from django.contrib import admin

from .models import Task, Picture


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'secret', 'created_at', 'task_type', 'adjective', 'noun', 'valid_pictures', 'invalid_pictures']

    list_display =  ['__unicode__', 'secret', 'created_at', 'task_type', 'adjective', 'noun']


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    readonly_fields = ['img', 'created_at', 'adjective', 'noun', 'valid_identifications', 'failed_identifications']

    list_display =  ['__unicode__', 'created_at', 'adjective', 'noun', 'valid_identifications', 'failed_identifications']
