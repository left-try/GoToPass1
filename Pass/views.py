import pyqrcode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
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

def admink(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'admin.html')
        elif request.method == 'POST':
            if request.POST['submit'] == 'Выдать GoToPass':

                nso = request.POST['FirstLastname'].split('\n')
                for student_nso in nso:
                    exempl = student_nso.split(' ')
                    pers = Person()
                    pers.name = exempl[1]
                    pers.surname = exempl[0]
                    pers.otchestvo = exempl[2]
                    pers.pass_gen = secrets.token_hex(16)
                    pers.save()
                    qr_key = pyqrcode.create(pers, error='L', version=27, mode='binary')

                    response = HttpResponse(content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename="gotopass.pdf"'

                    # Create the PDF object, using the response object as its "file."
                    p = canvas.Canvas(response)

                    # Draw things on the PDF. Here's where the PDF generation happens.
                    # See the ReportLab documentation for the full list of functionality.
                    p.drawString(100, 100, qr_key)


                    # Close the PDF object cleanly, and we're done.
                    p.showPage()
                    p.save()
                    return response
            return redirect('/')



    else:
        return redirect('/login')



def APISETPASS(request):
    password = request.GET.get('pass', '')
    person = Person.objects.filter(pass_gen = password)

    return JsonResponse()

def APISET(request):
    tg_id = request.GET.get('tg', '')
    password = request.GET.get('pass', '')
    person = Person.objects.filter(pass_gen = password)
    if tg_id == '' or password == '':
        return HttpResponse("incorrect request", status=422)
    else:
        if password == person.pass_gen:
            person.tg_id = tg_id
        else:
            return HttpResponse('Неправильный pass')


def APIAll (request):

    return JsonResponse([], safe=False)