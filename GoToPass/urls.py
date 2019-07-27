
from django.contrib import admin
from django.urls import path

from Pass.views import APIGETINFO, APIAll, APISET, login_page, logout_page, admink, make_pdf, APISETVKID, APISETHOME, APIINFOTGID, APIINFOVKID, APISETCOURS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get', APIGETINFO),
    path('api/get/tg', APIINFOVKID),
    path('api/get/vk', APIINFOTGID),
    path('api/get/all', APIAll),

    path('api/set/tg', APISET),
    path('api/set/vk', APISETVKID),
    path('api/set/home', APISETHOME),
    path('api/set/cours', APISETCOURS),

    path('login', login_page),
    path('pdf', make_pdf),
    path('logout', logout_page),
    path('', admink)
]
