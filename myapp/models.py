# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    weather = models.BooleanField(default=True)
    date_time = models.BooleanField(default=True)
    quote = models.BooleanField(default=False)
    user_text = models.TextField(default="")
    location = models.TextField(default="Visakhapatnam, Andhra Pradesh, India")
    timezone = models.TextField(default="5.30")
    alarm = models.TimeField(null=True, blank=True)
