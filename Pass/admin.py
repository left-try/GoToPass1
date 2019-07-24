from django.contrib import admin

# Register your models here.
from .models import Person, Key

admin.site.register(Person)
admin.site.register(Key)
