from django.contrib import admin
from django.urls import path

from Pass.views import APISetPass, APIAll, APISET

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get', APISetPass),
    path('api/all', APIAll),
    path('api/set', APISET)
]