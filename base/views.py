# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from base.models import Pent_User,Test
import hashlib
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView
import re
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import textwrap
from random import randint


class HomePageView(TemplateView):
    template_name = 'index.html'


def reg_index(request):
    return render(request, 'register.html')


def register(request):
    try:
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        pwd = hashlib.md5((request.POST["pass"]).encode()).hexdigest()
        phone = request.POST["phone"]
        addr = request.POST["address"]
    except:
        pass

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if match is None:
        return render(request, "register.html", {
            'err_msg': "Email is invalid.",
        })
    if len(email.split(" ")) > 1:
        return render(request, "register.html", {
            'err_msg': "Email cannot have whitespaces.",
        })

    if fname[0].islower() or lname[0].islower():
        return render(request, "register.html", {
            'err_msg': "First name or last name cannot start with a lowercase letter.",
        })

    if len(request.POST['pass']) < 8:
        return render(request, "register.html", {
            'err_msg': "Password should have at least 8 characters.",
        })
    if request.POST['pass'].isalpha():
        return render(request, "register.html", {
            'err_msg': "Password should have at least 1 number.",
        })
    if request.POST['pass'] != request.POST['cpw']:
        return render(request, "register.html", {
            'err_msg': "Passwords does not match.",
        })
    if len(phone)<10:
        return render(request, "register.html", {
            'err_msg': "Invalid Mobile Number.",
        })
    for user in Pent_User.objects.all():
        if user.email == email:
            error_message = """User account with email: %s already exists. 
                                Try using different email.""" % user.email
            return render(request, 'register.html', {'err_msg': error_message})

    sc = ''.join(["{}".format(randint(0, 9)) for num in range(0, 8)])
    securitycode = hashlib.md5((sc).encode()).hexdigest()
    try:
        pu = Pent_User.objects.get(phone=phone)
        pu.first_name = fname
        pu.last_name = lname
        pu.email = email
        pu.phone = phone
        if addr == "":
            pu.addr = "NA"
        else:
            pu.addr = addr
        pu.passwd = pwd
        pu.securitycode = securitycode
        pu.save()
    except:
        Pent_User.objects.create(first_name=fname, last_name=lname, email=email, phone=phone, addr=addr, passwd=pwd, securitycode=securitycode)

    messages.add_message(request, messages.INFO, 'User Account Created. Your Security Code is '+sc
                         + '. Keep it saved as this is the only way you can reset your password if forgotten.')
    return HttpResponseRedirect('register')


def login_index(request):
    return render(request, 'login.html')


def login(request):
    try:
        if request.session['user_id'] is not None:
            return render(request, "user_ui.html", {'fname': Pent_User.objects.get(id=request.session['user_id']).first_name})
    except:
        pass

    try:
        email = request.POST['email']
        pwd = hashlib.md5((request.POST["pass"]).encode()).hexdigest()
    except (KeyError, Pent_User.DoesNotExist):
        return render(request, "login.html", {
            'err_msg_login': "login required",
        })

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if match is None:
        return render(request, "login.html", {
            'err_msg_login': "Email is invalid.",
        })

    if len(Pent_User.objects.all()) > 0:
        # flag variable for user name and and password
        fn, fp = 0, 0
        for user in Pent_User.objects.all():
            if user.email == email:
                pu = Pent_User.objects.get(email=email)
                if pu.ban == True:
                    return render(request, "login.html", {
                        'err_msg_login': "User banned by Administrator. Contact Owner.",
                    })
                fn = 1
                if user.passwd == pwd:
                    fp = 1

            if fn == 0:
                error_message = "Email Incorrect. Try again."
            elif fp == 0:
                error_message = "Password Incorrect. Try again."
            else :
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                return render(request, "user_ui.html", {'fname': user.first_name})
    else:
        error_message = "User does not exist."

    return render(request, "login.html", {'err_msg_login': error_message })


def logout(request):
    request.session['user_id'] = None
    request.session['email'] = None
    return render(request, 'login.html')


def password_reset(request):
    try:
        email = request.POST['email']
        sc = request.POST['securitycode']
        pwd = request.POST['pass']
        cpw = request.POST['cpw']
    except:
        return render(request, 'reset_pass.html')

    for user in Pent_User.objects.all():
        if user.email == email:
            pu = Pent_User.objects.get(email=email)
            if pu.securitycode == hashlib.md5(sc.encode()).hexdigest():
                if pwd != cpw:
                    return render(request, "reset_pass.html", {
                        'err_msg_reset': "Passwords do not match.",
                    })
                elif len(pwd) < 8:
                    return render(request, "reset_pass.html", {
                        'err_msg_reset': "Password should have at least 8 characters.",
                    })
                elif pwd.isalpha():
                    return render(request, "reset_pass.html", {
                        'err_msg_reset': "Password should have at least 1 number.",
                    })
                else:
                    pu.passwd = hashlib.md5(pwd.encode()).hexdigest()
                    pu.save()
                    return render(request, "reset_pass.html", {
                        'succ_msg_reset': "Password reset successfully.",
                    })
            else:
                return render(request, "reset_pass.html", {
                    'err_msg_reset': "WRONG SECURITY CODE!",
                })

    return render(request, "reset_pass.html", {
        'err_msg_reset': "Email does not exist.",
        })


def all_my_tests(request):
    context = {
        'user_id': request.session['user_id'],
        'email': request.session['email'],
    }

    try:
        if request.session['user_id'] is None:
            return render(request, 'login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    tests = Pent_User.objects.get(pk=request.session['user_id']).test_set.filter(addeddate__lte=timezone.now()).order_by('-addeddate')
    if len(tests)>0:
        context['succ_msg_mytest'] = "Found "+str(len(tests))+" submitted tests."
        context['tests'] = tests
    else:
        context['err_msg_mytest'] = "No tests found."

    return render(request, 'mytests.html', context)


def view_test(request, test_id):
    test = Test.objects.get(pk=test_id)
    context = {
        'user_id': request.session['user_id'],
        'email': request.session['email'],
        'testob': test
    }

    try:
        if request.session['user_id'] is None:
            return render(request, 'login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    return render(request, 'printtest.html', context)


def enquiry(request):
    context = {
        'user_id': request.session['user_id'],
        'email': request.session['email'],
    }

    try:
        if request.session['user_id'] is None:
            return render(request, 'login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    return render(request, 'enquiry.html', context)


def print_data_unofficial(request, test_id):
    def drawmyruler(pdf):
        pdf.drawString(100, 810, 'x100')
        pdf.drawString(200, 810, 'x200')
        pdf.drawString(300, 810, 'x300')
        pdf.drawString(400, 810, 'x400')
        pdf.drawString(500, 810, 'x500')

        pdf.drawString(10, 100, 'y100')
        pdf.drawString(10, 200, 'y200')
        pdf.drawString(10, 300, 'y300')
        pdf.drawString(10, 400, 'y400')
        pdf.drawString(10, 500, 'y500')
        pdf.drawString(10, 600, 'y600')
        pdf.drawString(10, 700, 'y700')
        pdf.drawString(10, 800, 'y800')

    testpdf = Test.objects.get(pk=test_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="test_'+testpdf.user.first_name+'_'+testpdf.user.phone+'.pdf"'

    documentTitle = testpdf.user.first_name+"_"+testpdf.user.phone
    title = 'Pentagon Water Consultants'
    subtitle = 'Water Test Results'
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    # drawmyruler(p)

    # Start writing the PDF here
    p.setFont('Times-Bold', 32)
    p.setFillColor(HexColor('#135375'))
    p.drawCentredString(300, 780, title)
    p.setFont('Times-Roman', 12)
    p.setFillColorRGB(0, 0, 0)
    p.drawCentredString(300, 755, 'Near Passport Sevakendra')
    p.drawCentredString(300, 740, 'Payyanur . 670307 . Kerala')
    p.setFont('Times-Italic', 10)
    p.drawCentredString(90, 710, 'pentagonwaters@gmail.com')
    p.setFont('Times-Italic', 9)
    p.drawCentredString(530, 709, '+91 8086654684')
    # Borders
    p.line(20, 820, 20, 20)  # left border
    p.line(20, 820, 575, 820)  # top border
    p.line(575, 820, 575, 20)  # right border
    p.line(575, 20, 20, 20)  # bottom border

    # Underlines
    p.line(20, 720, 575, 720)  # above email and phone

    # Box Report Borders
    p.line(20, 570, 575, 570)
    p.line(20, 545, 575, 545)
    p.line(20, 520, 575, 520)
    p.line(20, 495, 575, 495)
    p.line(20, 470, 575, 470)
    p.line(20, 445, 575, 445)
    p.line(20, 418, 575, 418)
    # Box Report
    p.setFont('Times-Bold', 18)
    p.drawCentredString(297, 670, 'Indicative Report of Water Quality')

    p.setFont('Times-Roman', 9)
    p.drawCentredString(458, 670, '(Unverified)')
    p.setFont('Times-Roman', 14)
    p.drawCentredString(297, 640, 'Customer Name : '+testpdf.user.first_name+' '+testpdf.user.last_name)
    p.drawCentredString(297, 620, 'Customer Mobile : ' + testpdf.user.phone)

    p.drawString(50, 550, '1. Colour')
    p.drawCentredString(220, 550, ' : ')
    p.drawString(230, 550, testpdf.colour)

    p.drawString(50, 525, '2. Smell')
    p.drawCentredString(220, 525, ' : ')
    p.drawString(230, 525, testpdf.smell)

    p.drawString(50, 500, '3. pH')  # + ' (Acceptable limit : 6.5 - 8.5)')
    p.drawString(230, 500, str(testpdf.ph))
    p.setFont('Times-Roman', 8)
    p.drawString(460, 500, '..Acceptable limit : 6.5 - 8.5')
    p.setFont('Times-Roman', 14)
    p.drawCentredString(220, 500, ' : ')

    p.drawString(50, 475, '4. TDS (mg/l)')  # + str(testpdf.tds) + ' (Acceptable limit : 500)')
    p.drawString(230, 475, str(testpdf.tds))
    p.setFont('Times-Roman', 8)
    p.drawString(460, 475, '..Acceptable limit : 500')
    p.setFont('Times-Roman', 14)
    p.drawCentredString(220, 475, ' : ')

    p.drawString(50, 450, '5. Iron (mg/l)')  # + str(testpdf.iron) + ' (Acceptable limit : 0.3)')
    p.drawString(230, 450, str(testpdf.iron))
    p.setFont('Times-Roman', 8)
    p.drawString(460, 450, '..Acceptable limit : 0.3')
    p.setFont('Times-Roman', 14)
    p.drawCentredString(220, 450, ' : ')

    p.drawString(50, 425, '6. Total Hardness (mg/l)')  # + str(testpdf.hardness) + ' (Acceptable limit : 200)')
    p.drawString(230, 425, str(testpdf.hardness))
    p.setFont('Times-Roman', 8)
    p.drawString(460, 425, '..Acceptable limit : 200')
    p.setFont('Times-Roman', 14)
    p.drawCentredString(220, 425, ' : ')

    # Remarks
    p.setFont('Times-Bold', 14)
    p.drawString(50, 300, 'Remarks :')
    remarks_lines = textwrap.wrap(testpdf.remarks, 83)
    vh = 270
    p.setFont('Times-Roman', 14)
    for line in remarks_lines:
        p.drawString(50, vh, line)
        vh -= 25

    # PS
    p.setFillColor(HexColor('#135375'))
    p.drawString(50, 53, 'PS : The report is based on field kits and are indicative values for further detail analysis.')
    p.setFont('Times-Roman', 10)
    p.setFillColor(HexColor('#000000'))
    p.drawString(200, 35, 'Date & Time     : ')
    p.setFillColor(HexColor('#135375'))
    p.drawString(280, 35, str(timezone.now()))
    # End writing

    p.setTitle(documentTitle)
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response