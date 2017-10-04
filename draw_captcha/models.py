# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .constants import ADJECTIVES, NOUNS


class Task(models.Model):
    uuid = models.CharField(max_length=16, primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True)
    secret = models.CharField(max_length=16)

    task_type = models.CharField(max_length=16)
    adjective = models.CharField(max_length=16, null=True, blank=True)
    noun = models.CharField(max_length=16, null=True, blank=True)

    def get_instructions(self):
        if self.task_type == 'find_adjectives':
            return _('Click all {adjective} objects!').format(adjective=ADJECTIVES[self.adjective])
        if self.task_type == 'find_nouns':
            return _('Click all images where is {noun}!').format(noun=NOUNS[self.noun])
        return None

    def __unicode__(self):
        return self.uuid