# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

import os

from .constants import ADJECTIVES, NOUNS


class Picture(models.Model):
    img = models.ImageField(upload_to='draw_captcha/')
    created_at = models.DateTimeField(auto_now_add=True)

    adjective = models.CharField(max_length=16)
    noun = models.CharField(max_length=16)

    # These keep track how many times picture has been identified.
    # These are updated only when user seems to be a human.
    valid_identifications = models.PositiveIntegerField(default=0)
    failed_identifications = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return _('{adjective} {noun}').format(adjective=ADJECTIVES[self.adjective], noun=NOUNS[self.noun])


@receiver(models.signals.post_delete, sender=Picture)
def picture_file_delete(sender, instance, **kwargs):
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


class Task(models.Model):
    uuid = models.CharField(max_length=16, primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # This is set if task is completed
    secret = models.CharField(max_length=16, unique=True, blank=True, null=True, default=None)

    task_type = models.CharField(max_length=16)
    adjective = models.CharField(max_length=16, null=True, blank=True)
    noun = models.CharField(max_length=16, null=True, blank=True)

    valid_pictures = models.ManyToManyField(Picture, related_name='valid_in_tasks')
    invalid_pictures = models.ManyToManyField(Picture, related_name='invalid_in_tasks')

    def get_instructions(self):
        if self.task_type == 'draw':
            return _('Draw {adjective} {noun}!').format(adjective=ADJECTIVES[self.adjective], noun=NOUNS[self.noun])
        if self.task_type == 'find_adjectives':
            return _('Click all {adjective} objects!').format(adjective=ADJECTIVES[self.adjective])
        if self.task_type == 'find_nouns':
            return _('Click all images where is {noun}!').format(noun=NOUNS[self.noun])
        return None

    def __unicode__(self):
        return self.uuid