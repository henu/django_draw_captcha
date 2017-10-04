# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.template import loader
from django.utils.safestring import mark_safe


class CaptchaWidget(forms.widgets.Widget):
    template_name = 'draw_captcha.html'

    def get_context(self, name, value, attrs=None):
        return {'name': name}

    def render(self, name, value, attrs=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)


class CaptchaField(forms.Field):

    def __init__(self, required=False, label=None, initial=None, help_text=None):
        super(CaptchaField, self).__init__(
            required=required,
            label=label,
            initial=None,
            widget=CaptchaWidget,
            help_text=help_text
        )

    def clean(self, value):
        return value
