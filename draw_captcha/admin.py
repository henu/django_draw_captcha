from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'secret', 'created_at', 'task_type', 'adjective', 'noun']
