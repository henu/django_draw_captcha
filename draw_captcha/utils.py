import random
import string

from django.db import IntegrityError
from django.db.models import F

from .models import Task, Picture
from .constants import ADJECTIVES, NOUNS, BANNED_COMBINATIONS

VALID_PICTURES_COUNT = 6
INVALID_PICTURES_COUNT = 16 - VALID_PICTURES_COUNT


def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def clean_bad_pictures():
    bad_pictures = Picture.objects.filter(
        failed_identifications__gt=5,
        valid_identifications__lt=F('failed_identifications') * 5,
    )
    bad_pictures.delete()


def generate_new_task():
    # Before anything else, clean crappy drawings
    clean_bad_pictures()

    # In some cases, the user needs to draw a picture.
    # Use loop, because some combinations are not allowed.
    while True:
        # By default, a picture finding task is created
        selection = random.randint(0, len(ADJECTIVES) + len(NOUNS) - 1)
        adjective = None
        noun = None
        if selection < len(ADJECTIVES):
            task_type = 'find_adjectives'
            adjective = random.choice(list(ADJECTIVES.keys()))
            valid_pictures = list(Picture.objects.filter(adjective=adjective).order_by('?')[:VALID_PICTURES_COUNT])
            invalid_pictures = list(Picture.objects.exclude(adjective=adjective).order_by('?')[:INVALID_PICTURES_COUNT])
        else:
            task_type = 'find_nouns'
            noun = random.choice(list(NOUNS.keys()))
            valid_pictures = list(Picture.objects.filter(noun=noun).order_by('?')[:VALID_PICTURES_COUNT])
            invalid_pictures = list(Picture.objects.exclude(noun=noun).order_by('?')[:INVALID_PICTURES_COUNT])

        # If there is not enough pictures, then ask user to draw some
        if len(valid_pictures) < VALID_PICTURES_COUNT:
            task_type = 'draw'
            if noun is None:
                noun = random.choice(list(NOUNS.keys()))
            if adjective is None:
                adjective = random.choice(list(ADJECTIVES.keys()))
        elif len(invalid_pictures) < INVALID_PICTURES_COUNT:
            task_type = 'draw'
            if noun is None:
                noun = random.choice(list(NOUNS.keys()))
            else:
                noun = random.choice([noun2 for noun2 in NOUNS.keys() if noun2 != noun])
            if adjective is None:
                adjective = random.choice(list(ADJECTIVES.keys()))
            else:
                adjective = random.choice([adjective2 for adjective2 in ADJECTIVES.keys() if adjective2 != adjective])

        # Ten percent of users need to draw something anyway
        if task_type != 'draw' and random.randint(0, 9) == 0:
            task_type = 'draw'
            noun = random.choice(list(NOUNS.keys()))
            adjective = random.choice(list(ADJECTIVES.keys()))

        # If drawing task was created, then make sure the combination is permitted
        if task_type == 'draw' and (adjective, noun) in BANNED_COMBINATIONS:
            continue

        break

    # Actual creation
    while True:
        try:
            task = Task.objects.create(
                uuid=random_string(16),
                task_type=task_type,
                adjective=adjective,
                noun=noun,
            )
            break
        except IntegrityError:
            pass

    # If not a drawing task, then add images
    if task_type != 'draw':
        for pic in valid_pictures:
            task.valid_pictures.add(pic)
        for pic in invalid_pictures:
            task.invalid_pictures.add(pic)

    return task
