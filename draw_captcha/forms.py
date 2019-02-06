# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.template import loader
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from .models import Task


class CaptchaWidget(forms.widgets.Widget):
    template_name = 'draw_captcha.html'

    def get_context(self, name, value, attrs=None):
        return {'name': name}

    def render(self, name, value, attrs=None, renderer=None):
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
        if not Task.objects.filter(secret=value).exists():
            raise forms.ValidationError(_('Captcha was not completed!'))
        return value
