#!/usr/bin/env python
from setuptools import setup

setup(
    name='django_draw_captcha',
    description='Captcha based on drawings by users.',
    version='1.0.5',
    packages=['draw_captcha'],
    author='Henrik Heino',
    author_email='henrik.heino@gmail.com',
    license='MIT License',
    url='https://github.com/henu/django_draw_captcha',
    package_data={'draw_captcha': ['templates/*']},
)

