from django.contrib.auth.models import User
from django.db import models

class Person:
    name = models.TextField()
    surname = models.TextField()
    otchestvo = models.TextField()
