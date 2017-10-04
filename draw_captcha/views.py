# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from io import BytesIO
from PIL import Image

from .models import Task, Picture
from .utils import generate_new_task, random_string

def get_task(request):

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
    details['draw'] = task.task_type == 'draw'

    return JsonResponse(details)


@csrf_exempt
def upload_drawing(request):

    # Make sure user has proper task open
    try:
        task = Task.objects.get(uuid=request.session.get('draw_captcha_task_uuid'))
    except Task.DoesNotExist:
        return HttpResponseForbidden()
    if task.task_type != 'draw':
        return HttpResponseForbidden()

    file = request.FILES.get('drawing')
    if not file:
        return HttpResponseBadRequest()

    # Open image and scale it down
    try:
        img = Image.open(BytesIO(file.read()))
    except IOError:
        return HttpResponseBadRequest()
    img.thumbnail([100, 100], Image.ANTIALIAS)

    # Convert back to Django image
    img_d_buf = BytesIO()
    img.save(img_d_buf, 'PNG')
    img_d = ContentFile(img_d_buf.getvalue())
    img_filename = '{}.png'.format(random_string(32))
    img_d = InMemoryUploadedFile(img_d, None, img_filename, 'image/png', img_d.tell, None)

    Picture.objects.create(img=img_d, adjective=task.adjective, noun=task.noun)

    # Task is now completed, so remove it
    task.delete()

    return JsonResponse({})
