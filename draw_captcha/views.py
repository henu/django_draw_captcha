# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from .models import Task
from .utils import generate_new_task

def get_details(request):

    details = {}

    # If user has no task, create one
    task_uuid = request.session.get('draw_captcha_task_uuid')
    if not task_uuid:
        task = generate_new_task()
        request.session['draw_captcha_task_uuid'] = task.uuid
    else:
        try:
            task = Task.objects.get(uuid=task_uuid)
        except Task.DoesNotExist:
            task = generate_new_task()
            request.session['draw_captcha_task_uuid'] = task.uuid

    details['instructions'] = task.get_instructions()

    return JsonResponse(details)
