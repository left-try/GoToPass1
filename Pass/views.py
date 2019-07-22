import io

import pyqrcode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import secrets

from reportlab.pdfgen import canvas

from Pass.models import Person


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            messages.error(request, 'Заполните все поля!')
            return redirect('/login')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильный логин или пароль!')
            return redirect('/login')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login')


def make_pdf(request):
    if not request.user.is_authenticated:
        return redirect('/')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="gotopass.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)


    students = Person.objects.all()
    # qr_key = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
    # qr_key.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
    # qr_key.show()
    offset = 1
    for student in students:
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(200, 500, student.pass_gen)

        # Close the PDF object cleanly, and we're done.
        p.showPage()

        offset += 20
        #print("doing")

    p.showPage()
    p.save()
    return response


def admink(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            students = Person.objects.all()
            return render(request, 'admin.html', {'students': students})
        elif request.method == 'POST':
            if request.POST['submit'] == 'Выдать GoToPass':
                # save to d
                nso = request.POST['FirstLastname'].split('\n')
                for student_nso in nso:
                    exempl = student_nso.split(' ')
                    pers = Person()
                    pers.name = exempl[1]
                    pers.surname = exempl[0]
                    pers.otchestvo = exempl[2]
                    pers.pass_gen = secrets.token_hex(16)
                    pers.save()
            return redirect('/')
    else:
        return redirect('/login')


def APISETPASS(request):
    stud = request.GET.get('pass', 0)
    pers = Person.objects.get(pass_gen=stud)
    pers.tg_id = request.GET.get('tg_id', 0)

    pers.save()

    return JsonResponse(pers, safe=False)


def APISET(request):
    return HttpResponse('ок')


def APIAll(request):
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
