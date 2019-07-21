from django.http import JsonResponse
from django.shortcuts import render

def APISetPass(request):
    a = {
        'name': 'Вася',
        'surname': 'Пупкин',
        'password': 123456,
        'tg': 1238860
    }
    return JsonResponse(a)


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
