
from django.contrib import admin
from django.urls import path

from Pass.views import APIGETINFO, APIAll, APISET, login_page, logout_page, admink, make_pdf, APISETVKID, APISETHOME

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get', APIGETINFO),
    path('api/all', APIAll),
    path('api/set', APISET),
    path('api/setvk', APISETVKID),
    path('api/sethome', APISETHOME),

    path('login', login_page),
    path('pdf', make_pdf),
    path('logout', logout_page),
    path('', admink)
]
