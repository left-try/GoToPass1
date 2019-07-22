from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            return HttpResponse("Заполните все поля")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Логин неверен")



def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login')


def APISETPASS(request):
    a = {
        'name': 'Вася',
        'surname': 'Пупкин',
        'password': 123456,
        'tg': 1238860
    }
    return JsonResponse(a)

def APISET(request):
    return HttpResponse('ок')


def APIAll (request):
    a = {
        'name': 'Вася',
        'surname': 'Пупкин',
        'password': 123456,
        'tg': 1238860
    }

    b = {
        'name': 'Петя',
        'surname': 'Пупкин',
        'password': 123456,
        'tg': 1238860
    }
    return JsonResponse([a, b], safe=False)