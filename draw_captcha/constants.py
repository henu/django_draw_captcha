# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _


ADJECTIVES = {
    'colorful': _('colorful'),
    'hairy': _('hairy'),
    'wet': _('wet'),
    'flying': _('flying'),
    'burning': _('burning'),
    'dirty': _('dirty'),
}

NOUNS = {
    'cat': _('cat'),
    'snake': _('snake'),
    'car': _('car'),
    'house': _('house'),
    'computer': _('computer'),
    'ship': _('ship'),
    'guitar': _('guitar'),
    'tree': _('tree'),
    'mobile_phone': _('mobile phone'),
    'triangle': _('triangle'),
    'bird': _('bird'),
    'fish': _('fish'),
    'mug': _('mug'),
    'clock': _('clock'),
    'flower': _('flower'),
    'lock': _('lock'),
    'bicycle': _('bicycle'),
    'chair': _('chair'),
    'backpack': _('backpack'),
    'umbrella': _('umbrella'),
    'shoe': _('shoe'),
    'hat': _('hat'),
    'spider': _('spider'),
}

BANNED_COMBINATIONS = [
    ('burning', 'cat'),
    ('burning', 'snake'),
    ('burning', 'bird'),
    ('burning', 'fish'),
    ('burning', 'flower'),
    ('burning', 'spider'),
]
