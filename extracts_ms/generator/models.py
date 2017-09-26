# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class File(models.Model):
    user_id = models.IntegerField()
    days = models.IntegerField()
