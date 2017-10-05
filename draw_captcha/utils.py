import random
import string

from django.db import IntegrityError

from .models import Task, Picture
from .constants import ADJECTIVES, NOUNS

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def generate_new_task():
    # Select type
    task_type = random.randint(0, 1)
    adjective = None
    noun = None
    if task_type == 0:
        task_type = 'find_adjectives'
        adjective = random.choice(ADJECTIVES.keys())
        valid_pictures = list(Picture.objects.filter(adjective=adjective).order_by('?')[:8])
        invalid_pictures = list(Picture.objects.exclude(adjective=adjective).order_by('?')[:8])
    elif task_type == 1:
        task_type = 'find_nouns'
        noun = random.choice(NOUNS.keys())
        valid_pictures = list(Picture.objects.filter(noun=noun).order_by('?')[:8])
        invalid_pictures = list(Picture.objects.exclude(noun=noun).order_by('?')[:8])

    # If there is not enough pictures, then ask user to draw some
    if len(valid_pictures) < 8:
        task_type = 'draw'
        if noun is None:
            noun = random.choice(NOUNS.keys())
        if adjective is None:
            adjective = random.choice(ADJECTIVES.keys())
    elif len(invalid_pictures) < 8:
        task_type = 'draw'
        if noun is None:
            noun = random.choice(NOUNS.keys())
        else:
            noun = random.choice([noun2 for noun2 in NOUNS.keys() if noun2 != noun])
        if adjective is None:
            adjective = random.choice(ADJECTIVES.keys())
        else:
            adjective = random.choice([adjective2 for adjective2 in ADJECTIVES.keys() if adjective2 != adjective])

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
