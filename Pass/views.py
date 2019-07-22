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
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(200, 500, student.pass_gen)
        p.drawString(200, 500, ' GoTo Camp запрещается и приводит к отчислению:')
        p.drawString(200, 500, 'употребление алкоголя, ')
        p.drawString(200, 500, 'курение')
        p.drawString(200, 500, 'выход за территорию базы без сопровождения,')
        p.drawString(200, 500, 'создание угрозы жизни, здоровью и учебе других людей или самого ')
        p.drawString(200, 500, 'нарушителя (компьютерные игры, соцсети и т.п. во время занятий, ')
        p.drawString(200, 500, 'выход из домов в ночное время и др.).')
        p.drawString(200, 500, '')
        p.drawString(200, 500, 'Отчисление происходит по решению директора. Если несовершеннолетнего')
        p.drawString(200, 500, 'участника отчисляют из школы, родители или доверенные лица обязаны ')
        p.drawString(200, 500, 'забрать его самостоятельно в течение 2 дней. ')
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
    password = request.GET.get('pass', '')
    person_z = Person.objects.get(pass_gen=password)
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }

    return JsonResponse(person)

def APISET(request):
    tg_id = request.GET.get('tg', '')
    password = request.GET.get('pass', '')
    person_z = Person.objects.get(pass_gen=password)
    if tg_id == '' or password == '':
        return HttpResponse("incorrect request", status=422)
    else:
        if password == person_z.pass_gen:
            person_z.tg_id = tg_id
            person_z.save()

        else:
            return HttpResponse('Неправильный pass')
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }

    return JsonResponse(person)



def APIAll (request):


    return JsonResponse([], safe=False)
