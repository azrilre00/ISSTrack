from django.db import models
from rest_framework import serializers

# Create your models here.

class TimeISS(models.Model):
    datetimes = models.DateTimeField()
