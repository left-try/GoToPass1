from django.contrib.auth.models import User
from django.db import models

class Person(models.Model):
    name = models.TextField()
    surname = models.TextField()
    otchestvo = models.TextField()
    tg_id = models.TextField()
    pass_gen = models.TextField()
