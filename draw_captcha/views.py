# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import IntegrityError
from django.db.models import F
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

import base64
import colorsys
from io import BytesIO
from PIL import Image
import random

from .models import Task, Picture
from .utils import generate_new_task, random_string


@require_GET
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
    details['secret'] = task.secret

    details['pictures'] = []
    for picture in task.valid_pictures.all():
        details['pictures'].append([picture.id, picture.img.url])
    for picture in task.invalid_pictures.all():
        details['pictures'].append([picture.id, picture.img.url])
    random.shuffle(details['pictures'])

    if details['draw']:
        random.seed(task.uuid)
        details['colors'] = ['#222']
        hue = random.uniform(0, 1)
        saturation = random.uniform(0.8, 1)
        lightness = random.uniform(0.8, 1)
        COLORS = 9
        for i in range(COLORS):
            hue = (hue + 1 / COLORS) % 1
            red, green, blue = colorsys.hsv_to_rgb(hue, saturation, lightness)
            color = '#{:02x}{:02x}{:02x}'.format(
                max(0, min(255, int(red * 255))),
                max(0, min(255, int(green * 255))),
                max(0, min(255, int(blue * 255))),
            )
            details['colors'].append(color)

    return JsonResponse(details)


@csrf_exempt
@require_POST
def upload_drawing(request):

    # Make sure user has proper task open
    try:
        task = Task.objects.get(uuid=request.session.get('draw_captcha_task_uuid'))
    except Task.DoesNotExist:
        return HttpResponseForbidden()
    if task.task_type != 'draw':
        return HttpResponseForbidden()

    # Read image data
    drawing = request.POST.get('drawing')
    if not drawing:
        return HttpResponseBadRequest()
    try:
        drawing = base64.decodestring(str.encode(drawing.split(',', 1)[1]))
    except:
        return HttpResponseBadRequest()

    # Open image and scale it down
    try:
        img = Image.open(BytesIO(drawing))
    except IOError:
        return HttpResponseBadRequest()
    if (img.size != (400, 400)):
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


@csrf_exempt
@require_POST
def complete_task(request):

    # Make sure user has proper task open
    try:
        task = Task.objects.get(uuid=request.session.get('draw_captcha_task_uuid'))
    except Task.DoesNotExist:
        return HttpResponseForbidden()
    if task.task_type == 'draw':
        return HttpResponseForbidden()

    # Read and validate arguments
    pictures_ids_raw = filter(None, request.POST.get('pictures_ids', '').split(','))
    pictures_ids = []
    for picture_id_raw in pictures_ids_raw:
        try:
            picture_id = int(picture_id_raw)
        except ValueError:
            return HttpResponseBadRequest()
        pictures_ids.append(picture_id)
    pictures_ids = set(pictures_ids)

    # Divide pictures into different categories
    valid_identifications = []
    not_identified = []
    fail_identifications = []
    for picture_id in pictures_ids:
        if task.valid_pictures.filter(id=picture_id).exists():
            valid_identifications.append(picture_id)
        elif task.invalid_pictures.filter(id=picture_id).exists():
            fail_identifications.append(picture_id)
        else:
            return HttpResponseBadRequest()
    for valid_picture in task.valid_pictures.all():
        if valid_picture.id not in pictures_ids:
            not_identified.append(valid_picture.id)

    # Calculate number of errors
    errors = task.valid_pictures.count() - len(valid_identifications)

    # If the error is small enough, then update picture statistics.
    # But only if task is never solved before.
    if errors <= 3 and not task.secret:
        Picture.objects.filter(id__in=valid_identifications).update(valid_identifications=F('valid_identifications') + 1)
        Picture.objects.filter(id__in=fail_identifications + not_identified).update(failed_identifications=F('failed_identifications') + 1)

    # Check if task is accepted
    if errors <= 1:
        # Mark task as resolved
        while True:
            try:
                task.secret = random_string(16)
                task.save(update_fields=['secret'])
                break
            except IntegrityError:
                pass
        # Inform user
        return JsonResponse({'secret': task.secret})
    else:
        # Task failed. Remove it and inform user
        task.delete()
        return JsonResponse({'secret': None})
