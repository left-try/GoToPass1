import qrcode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from Pass import models
from Pass.models import Person
import secrets
import pyqrcode
import io
import pdfkit
import pdfkit
from reportlab.pdfgen.canvas import Canvas

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# страница для логина
def login_page(request):
    if request.method == 'GET':
        # если юзер залогинен - редирект на основную стр
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

# TODO: сделать печать pdf для выбраных участников, а не для всех
def make_pdf(request):                     # генерация pdf
    if not request.user.is_authenticated:  # если не залогинен
        return redirect('/')
    students = Person.objects.all()

    p_pdf = Canvas("p_pdf.pdf", pagesize=A4)
    for student in students:
        pdfmetrics.registerFont(TTFont('FreeSans', 'calibrili.ttf'))
        # памятка
        p_pdf.setFont('FreeSans', 12)
        p_pdf.drawString(150, 800, student.name)
        p_pdf.drawString(190, 800, student.surname)
        p_pdf.drawString(20, 760, 'В GoTo Camp запрещается и приводит к отчислению:')
        p_pdf.drawString(20, 730, 'употребление алкоголя,')
        p_pdf.drawString(20, 700, 'курение,')
        p_pdf.drawString(20, 670, 'выход за территорию базы без сопровождения,')
        p_pdf.drawString(20, 640, 'создание угрозы жизни, здоровью и учебе других людей или самого ')
        p_pdf.drawString(20, 610, 'нарушителя (компьютерные игры, соцсети и т.п. во время занятий,')
        p_pdf.drawString(20, 580, 'выход из домов в ночное время и др.).')
        p_pdf.drawString(20, 550, '')
        p_pdf.drawString(20, 520, 'Отчисление происходит по решению директора. Если несовершеннолетнего ')
        p_pdf.drawString(20, 490, 'участника отчисляют из школы, родители или доверенные лица обязаны ')
        p_pdf.drawString(20, 460, 'забрать его самостоятельно в течение 2 дней.')
        p_pdf.drawString(20, 430, 'Вот ваш GoToPass:')

        # генерация qr кода с Pass-ом
        qr.add_data(student.pass_gen)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        p_pdf.drawInlineImage(img, 200, 250, 200, 200)
        p_pdf.drawString(200, 200, student.pass_gen)
        p_pdf.showPage()
        qr.clear()

    p_pdf.save()
    pdf = open('p_pdf.pdf', 'rb')
    return FileResponse(pdf)


def admink(request):  # страница для добавления участников лагеря

    if request.user.is_authenticated:
        if request.method == 'GET':
            students = Person.objects.all()
            return render(request, 'admin.html', {'students': students})
        elif request.method == 'POST':
            if request.POST['submit'] == 'Выдать GoToPass':
                # запись участников в бд

                nso = request.POST['FirstLastname'].split('\n')  # список из ФИО
                # запись всех данных в своё поле
                for student_nso in nso:
                    exempl = student_nso.split(' ')  # список [Фамилия, Имя, Отчество]

                    pers = Person()
                    pers.name = exempl[1]
                    pers.surname = exempl[0]
                    pers.patronymic = exempl[2]
                    pers.pass_gen = secrets.token_hex(16)  # запись и генерация Pass-токена
                    pers.save()
            return redirect('/')
    else:
        return redirect('/login')

# №№№№№№№№№№№№ API №№№№№№№№№№№№№
# документация по API - https://docs.google.com/document/d/1dd41TxSUM4Dg5NFpNAdrAFae-BUW2PjXVwL4YAGHRDU/edit?usp=sharing
# TODO: иправить костыли и баги, если они есть

def APIGETINFO(request):
    password = request.GET.get('pass', '')
    person_z = Person.objects.get(pass_gen=password)
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'patronymic': person_z.patronymic,
        'tg_id': person_z.tg_id,
        'vk_id': person_z.vk_id,
        'home_number': person_z.home_number,
        'cours': person_z.cours,
        'id': person_z.id,
        'pass': person_z.pass_gen,
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
    # костыль
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }

    return JsonResponse(person)


def APIAll(request):
    if request.GET.get('key', '') == 'c21e9d9f7c68192ef79c2a6dddcbb953':
        students = models.Person.objects.all()

        all = []
        for student in students:
            all.append({
                'name': student.name,
                'surname': student.surname,
                'patronymic': student.patronymic,
                'tg_id': student.tg_id,
                'vk_id': student.vk_id,
                'home_number': student.home_number,
                'cours': student.cours,
                'id': student.id,
                'pass': student.pass_gen,
            })

    return JsonResponse(all, safe=False)


def APISETVKID(request):
    vk_id = request.GET.get('vk', '')
    password = request.GET.get('pass', '')
    person_z = Person.objects.get(pass_gen=password)
    if vk_id == '' or password == '':
        return HttpResponse("incorrect request", status=422)
    else:
        if password == person_z.pass_gen:
            person_z.vk_id = vk_id
            person_z.save()

        else:
            return HttpResponse('Неправильный pass')
    # костыль
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }
    return JsonResponse(person)


def APISETHOME(request):
    password = request.GET.get('pass', '')
    home_numb = request.GET.get('home', '')
    person_z = Person.objects.get(pass_gen=password)
    if home_numb == '' or password == '':
        return HttpResponse("incorrect request", status=422)
    else:
        if password == person_z.pass_gen:
            person_z.home_number = home_numb
            person_z.save()

        else:
            return HttpResponse('Неправильный pass')
    # костыль
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }
    return JsonResponse(person)


def APISETCOURS(request):
    password = request.GET.get('pass', '')
    cours = request.GET.get('cours', '')
    person_z = Person.objects.get(pass_gen=password)
    if password == '':
        return HttpResponse("incorrect request", status=422)
    else:
        if password == person_z.pass_gen:
            person_z.cours = cours
            person_z.save()
    # костыль
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }
    return JsonResponse(person)

def APIINFOTGID(request):
    tg_id = request.GET.get('tg', '')

    if tg_id != '':
        person_z = Person.objects.get(tg_id=tg_id)
        person = {
            'name': person_z.name,
            'surname': person_z.surname,
            'patronymic': person_z.patronymic,
            'tg_id': person_z.tg_id,
            'vk_id': person_z.vk_id,
            'home_number': person_z.home_number,
            'cours': person_z.cours,
            'id': person_z.id,
            'pass': person_z.pass_gen,
        }

        return JsonResponse(person)
    elif tg_id == '':
        return HttpResponse("incorrect request", status=422)


def APIINFOVKID(request):
    vk_id = request.GET.get('vk', '')
    if vk_id != '':
        person_z = Person.objects.get(vk_id=vk_id)
        person = {
            'name': person_z.name,
            'surname': person_z.surname,
            'patronymic': person_z.patronymic,
            'tg_id': person_z.tg_id,
            'vk_id': person_z.vk_id,
            'home_number': person_z.home_number,
            'cours': person_z.cours,
            'id': person_z.id,
            'pass': person_z.pass_gen,
        }

        return JsonResponse(person)
    elif vk_id == '':
        return HttpResponse("incorrect request", status=422)
