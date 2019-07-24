import qrcode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from reportlab.lib.pagesizes import A4, A3, A1, A5
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
#key = Key()
#if key == '':
 #  key.key = secrets.token_hex(16)


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
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf";'

    #p_pdf = canvas.Canvas(response)
    students = Person.objects.all()

    p_pdf = Canvas("p_pdf.pdf", pagesize=A4)
    for student in students:
        pdfmetrics.registerFont(TTFont('FreeSans', 'calibrili.ttf'))
        p_pdf.setFont('FreeSans', 12)
        p_pdf.drawString(150, 700, student.name)
        p_pdf.drawString(200, 700, student.surname)
        p_pdf.drawString(200, 500, student.pass_gen)
        qr.add_data('student.pass_gen')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        #p_pdf.drawImage(img, 200, 800,  mask='auto')
        #qr_key = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
        #qr_key.png('gotopass.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
        #qr_key.show()
        #p_pdf.drawString(200, 500 , qr_key)
        p_pdf.showPage()
    p_pdf.save()
    response = HttpResponse(content=p_pdf)
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = 'attachment; filename="gotopass.pdf"'
    return response
    #return FileResponse(as_attachment=False, filename='p_pdf.pdf')


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
                    pers.patronymic = exempl[2]
                    pers.pass_gen = secrets.token_hex(16)
                    pers.save()
            return redirect('/')
    else:
        return redirect('/login')


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


def APIAll(request):
    if request.GET.get('key', '') == 'c21e9d9f7c68192ef79c2a6dddcbb953':
        students = models.Person.objects.all()

        all = []
        i = 0
        for student in students:
            all.append({
                'name': student.name,
                'surname': student.surname,
                'patronymic': student.otshestvo,
                'tg_id': student.tg_id,
                'pass': student.pass_gen
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

    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'tg_id': person_z.tg_id,
        'pass': person_z.pass_gen
    }
    return JsonResponse(person)
