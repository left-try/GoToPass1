import qrcode as qrcode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from reportlab.pdfgen import canvas
from Pass import models
from Pass.models import Person, Key
import secrets
import pyqrcode
import io

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

key = Key()
if key == '':
    key.key = secrets.token_hex(16)


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

    for student in students:
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(150, 600, student.name)
        p.drawString(200, 600, student.surname)
        qr.make(fit=True)
        img = qr.make_image()
        arr = io.BytesIO()
        img.save(arr, format='PNG')
        #qr_key = pyqrcode.create('0987654321', error='L', version=27, mode='binary')
        #qr_key.png('gotopass.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])
        #qr_key.show()
        p.drawString(200, 500, qr_key)
        # Close the PDF object cleanly, and we're done.
        p.showPage()

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


def APIGETINFO(request):
    password = request.GET.get('pass', '')
    person_z = Person.objects.get(pass_gen=password)
    person = {
        'name': person_z.name,
        'surname': person_z.surname,
        'patronymic': person_z.otshestvo,
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

def APIAll (request):

    if request.GET.get('key', '') == key.key:
        students = models.Person.all().count()


        all = []
        i = 0
        for student in students:
            all[i] = {
                'name': student.name,
                'surname': student.surname,
                'patronymic': student.otshestvo,
                'tg_id': student.tg_id,
                'pass': student.pass_gen
            }


    return JsonResponse(all, safe=False)


def APISETVKID(request):
    vk_id = request.GET.get('vk', '')
    password = request.GET.get('pass', '')
    person_z = Person.objects.get(pass_gen=password)
    if vk_id == '' or password == '':
        return HttpResponse("incorrect request", status=422)
    else:
        if password ==person_z.pass_gen:
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



