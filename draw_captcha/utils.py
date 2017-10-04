import random
import string

from django.db import IntegrityError

from .models import Task
from .constants import ADJECTIVES, NOUNS

def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def generate_new_task():
    secret = random_string(16)

    # Select type
    task_type = random.randint(0, 1)
    adjective = None
    noun = None
    if task_type == 0:
        task_type = 'find_adjectives'
        adjective = random.choice(ADJECTIVES.keys())
    elif task_type == 1:
        task_type = 'find_nouns'
        noun = random.choice(NOUNS.keys())

    # Actual creation
    while True:
        try:
            task = Task.objects.create(
                uuid=random_string(16),
                secret=secret,
                task_type=task_type,
                adjective=adjective,
                noun=noun,
            )
            break
        except IntegrityError:
            pass

    return task
