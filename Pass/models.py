from django.contrib.auth.models import User
from django.db import models

class Person(models.Model):
    name = models.TextField()
    surname = models.TextField()
    patronymic = models.TextField()
    tg_id = models.TextField()
    vk_id = models.TextField()
    cours = models.TextField()
    pass_gen = models.TextField()
    home_number = models.TextField()

class Key(models.Model):
    key = models.TextField()
