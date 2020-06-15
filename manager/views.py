from django.shortcuts import render

# Create your views here.

import hashlib
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from manager.models import Manager_Acc, Manager_Code
from base.models import Pent_User, Test
from django.db.models import Q
from django.utils import timezone
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import textwrap
from fuzzywuzzy import process
import xlwt

def reg_index(request):
    return render(request, 'manager/m_register.html')


def manager_register(request):
    try:
        mcode = hashlib.md5((request.POST['mcode']).encode()).hexdigest()
        uname = request.POST["username"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        pwd = hashlib.md5((request.POST["pass"]).encode()).hexdigest()
    except:
        pass

    m_code = Manager_Code.objects.get(pk=1).code
    if mcode != m_code :
        return render(request, "manager/m_register.html", {
            'err_msg': "You cannot create a Manager Account without the correct manager code.",
        })
    if not uname.islower():
        return render(request, "manager/m_register.html", {
            'err_msg': "Username should not have any uppercase letters.",
        })
    if len(uname.split(" ")) > 1:
        return render(request, "manager/m_register.html", {
            'err_msg': "Username should be a single word.",
        })
    if uname[0].isdigit():
        return render(request, "manager/m_register.html", {
            'err_msg': "User name cannot start with a number.",
        })
    if fname[0].islower() or lname[0].islower():
        return render(request, "manager/m_register.html", {
            'err_msg': "First name or last name cannot start with a lowercase letter.",
        })
    if len(uname) < 5:
        return render(request, "manager/m_register.html", {
            'err_msg': "User name must have more than 4 characters.",
        })
    if len(request.POST['pass']) < 8:
        return render(request, "manager/m_register.html", {
            'err_msg': "Password should have at least 8 characters.",
        })
    if request.POST['pass'].isalpha():
        return render(request, "manager/m_register.html", {
            'err_msg': "Password should have at least 1 number.",
        })
    if request.POST['pass'] != request.POST['cpw']:
        return render(request, "manager/m_register.html", {
            'err_msg': "Passwords does not match.",
        })
    for manager in Manager_Acc.objects.all():
        if manager.username == uname:
            error_message = """Manager account : %s already exists. 
                                Try using different username.""" % uname
            return render(request, 'manager/m_register.html', {'err_msg': error_message})

    mgr = Manager_Acc.objects.create(username=uname, firstname=fname, lastname=lname, passwd=pwd)
    messages.add_message(request, messages.INFO, 'Manager Account Created.')

    # success_message = "Manager Account Created."
    # return render(request, 'manager/m_register.html', {'name': mgr.username,'password': mgr.passwd, 'success_msg':success_message})
    return HttpResponseRedirect('register')


def login_index(request):
    return render(request, 'manager/m_login.html')


def manager_login(request):
    try :
        if request.session['manager_id'] is not None:
            return render(request, "manager/manager_ui.html", {'m_fname': Manager_Acc.objects.get(id=request.session['manager_id']).username})
    except:
        pass

    try:
        uname = request.POST['username']
        pwd = hashlib.md5((request.POST["pass"]).encode()).hexdigest()
    except (KeyError, Manager_Acc.DoesNotExist):
        return render(request, "manager/m_login.html", {
            'err_msg_login': "login required",
        })

    if len(Manager_Acc.objects.all()) > 0:
        # flag variable for user name and and password
        fn, fp = 0, 0
        for manager in Manager_Acc.objects.all():
            if manager.username == uname:
                fn = 1
                if manager.passwd == pwd:
                    fp = 1

            if fp == 0:
                error_message = "Password Incorrect. Try again."
            elif fn == 0:
                error_message = "Username Incorrect. Try again."
            else :
                request.session['manager_id'] = manager.id
                request.session['manager_uname'] = manager.username
                return render(request, "manager/manager_ui.html", {'m_fname': manager.firstname})
    else:
        error_message = "Manager account does not exist."

    return render(request, "manager/m_login.html", {'err_msg_login': error_message })


def manager_logout(request):
    request.session['manager_id'] = None
    request.session['manager_uname'] = None
    return render(request, 'manager/m_login.html')


# Starting manager dashboard view views here.

def add_test(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass
    try:
        fname = request.POST['fname']
        phone = request.POST['phone']
        cphone = request.POST['cphone']
        place = request.POST['place']
    except:
        return render(request, 'manager/addnewtest.html', context)

    if fname[0].islower():
        return render(request, "manager/addnewtest.html", {
            'err_msg_addtest': "First name should have the first letter capitalised.",
        })
    if len(str(phone)) != 10:
        return render(request, "manager/addnewtest.html", {
            'err_msg_addtest': "Phone Number should be of length 10.",
        })
    if phone != cphone:
        return render(request, "manager/addnewtest.html", {
            'err_msg_addtest': "Phone Numbers does not match.",
        })

    place = (place.lower())[0].upper() + (place.lower())[1:]
    for pu in Pent_User.objects.all():
        if pu.phone == phone:
            pentuser = Pent_User.objects.get(phone=phone)
            pentuser.latesttestdate = timezone.now()
            pentuser.place = place
            pentuser.save()
            pentuser.test_set.create(user=pentuser)
            return render(request, 'manager/addnewtest.html', {
                'succ_msg': "Test details added successfully.",
                'm_id': request.session['manager_id'],
                'm_uname': request.session['manager_uname']
            })

    u1 = Pent_User.objects.create(first_name=fname, phone=phone, place=place)
    u1.test_set.create(user=u1)

    return render(request, 'manager/addnewtest.html', {
        'succ_msg': "Test details added successfully.",
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    })


def update_test(request, test_id):
    testupdate = Test.objects.get(pk=test_id)
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname'],
        'testob': testupdate
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    try:
        testupdate.colour = request.POST['colour']
        testupdate.smell = request.POST['smell']
        testupdate.ph = request.POST['ph']
        testupdate.tds = request.POST['tds']
        testupdate.iron = request.POST['iron']
        testupdate.hardness = request.POST['hardness']
        testupdate.remarks = request.POST['remarks']
        try:
            print(request.POST['completed'])
            testupdate.completed = True if request.POST['completed'] == 'on' else False
            if request.POST['completed'] == 'on':
                testupdate.completiondate = timezone.now()
        except:
            pass
        testupdate.save()
        context['succ_msg_update'] = "Test Details Added Successfully."
    except:
        pass
    return render(request, 'manager/updatetest.html', context)


def view_user_index(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    return render(request, 'manager/viewuser.html', context)


def search_name(q, limit=5):
    choices = []
    for u in Pent_User.objects.all():
        choices.append(u.first_name)
    results = process.extract(q, choices, limit=limit)
    return results


def view_user(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    try:
        search_p = request.POST['phone']
        search_n = request.POST['fname']

        search_ph = Pent_User.objects.filter(Q(phone__contains=search_p))
        if search_n:
            sn = search_name(search_n)
            sname = [x[0] for x in sn if x[1] > 71]
            if len(sname) > 0:
                sn = []
                for n in sname:
                    sn.append(Pent_User.objects.get(first_name=n))
                context['sn'] = sn
                context['succ_msg_viewuser'] = "Search results found."
                return render(request, 'manager/userlistsearch.html', context)
        if search_p:
            print("+")
            context['s_np'] = search_ph
            context['succ_msg_viewuser'] = "Search results found."
            return render(request, 'manager/userlistsearch.html', context)
        else:
            context['err_msg_viewuser'] = "No users found with specified details."
            return render(request, 'manager/viewuser.html', context)

    except:
        pass

    return render(request, 'manager/viewuser.html', context)


def view_user_bydate(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass
    context['user_obj'] = Pent_User.objects.filter(latesttestdate__lte=timezone.now()).order_by('-latesttestdate')

    if len(context['user_obj'])>0:
        context['succ_msg_viewuser'] = "Search results found."
        return render(request, 'manager/userlist.html', context)
    else:
        context['err_msg_viewuser'] = "No users found with specified details."
        return render(request, 'manager/viewuser.html', context)


def ban_user_index(request):
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    return render(request, 'manager/banuser.html', context)


def ban_user_by_search(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }

    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    try:
        search_p = request.POST['phone']
        search_n = request.POST['fname']
        search_ph = Pent_User.objects.filter(Q(phone__contains=search_p))
        if search_n:
            sn = search_name(search_n)
            sname = [x[0] for x in sn if x[1] > 71]
            if len(sname) > 0:
                sn = []
                for n in sname:
                    sn.append(Pent_User.objects.get(first_name=n))
                context['sn'] = sn
                context['succ_msg_viewuser'] = "Search results found."
                return render(request, 'manager/banuserbypn.html', context)
        if search_p:
            context['s_np'] = search_ph
            context['succ_msg_viewuser'] = "Search results found."
            return render(request, 'manager/banuserbypn.html', context)
        else:
            context['err_msg_viewuser'] = "No users found with specified details."
            return render(request, 'manager/banuser.html', context)

    except:
        pass

    return render(request, 'manager/viewuser.html', context)


def ban_user_by_date(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass
    context['user_obj'] = Pent_User.objects.filter(latesttestdate__lte=timezone.now()).order_by('-latesttestdate')[:15]
    # context['test_obj'] = Test.objects.all()
    if len(context['user_obj']) > 0:
        context['succ_msg_viewuser'] = "Search results found."
        return render(request, 'manager/banuserbyd.html', context)
    else:
        context['err_msg_viewuser'] = "No users found with specified details."
        return render(request, 'manager/banuser.html', context)


def ban_user(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    try:
        ban_id = int(request.GET['ban'])
        pu = Pent_User.objects.get(pk=ban_id)
        pu.ban = True
        context['succ_msg_viewuser'] = "User with id : "+str(ban_id)+" has been banned."
        pu.save()
    except:
        pass

    try:
        unban_id = int(request.GET['unban'])
        pu = Pent_User.objects.get(pk=unban_id)
        pu.ban = False
        context['succ_msg_viewuser'] = "User with id : " + str(unban_id) + " has been un-banned."
        pu.save()
    except:
        pass

    return render(request, 'manager/banuser.html', context)


def export_as_excel(n, t):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'inline; filename="Test_Data_('+str(timezone.now().day)+'-'+\
                                      str(timezone.now().month)+'-'+str(timezone.now().year)+').xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Tests')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    borders = xlwt.Borders()
    borders.left = 6
    borders.right = 6
    # borders.top = 6
    borders.bottom = 6
    font_style.borders = borders

    ws.row(0).height = 1000
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    font_style.alignment = alignment
    columns = ['Test Number', 'Test Name', 'Completion Date & Time', 'Colour', 'Smell', 'pH', 'TDS', 'Iron', 'Hardness', 'Test Submitted Date & Time', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER

    font_style = xlwt.easyxf('borders:left 6, right 6, top 3, bottom 3;')

    font_style.alignment = alignment

    rows = t.values_list('id', 'user', 'completiondate', 'colour', 'smell', 'ph', 'tds', 'iron', 'hardness', 'addeddate')
    for row in rows:
        row_num += 1
        ws.row(row_num).height = 400
        for col_num in range(len(row)):
            if col_num == 0:
                ws.col(col_num).width = 256 * (len(str(row[col_num])) + 20)
                ws.write(row_num, col_num, row_num, font_style)
            else:
                if isinstance(row[col_num], int):
                    ws.col(col_num).width = 256 * (len(str(row[col_num])) + 35)
                    ws.write(row_num, col_num, Pent_User.objects.get(pk=row[col_num]).first_name+"_"+Pent_User.objects.get(pk=row[col_num]).phone+"_"+Pent_User.objects.get(pk=row[col_num]).place, font_style)
                elif str(type(row[col_num])) == "<class 'datetime.datetime'>":
                    ws.col(col_num).width = 256 * (len(str(row[col_num])) + 10)
                    ws.write(row_num, col_num, str(row[col_num].day)+"/"+str(row[col_num].month)+"/"+
                                               str(row[col_num].year)+", "+str(row[col_num].hour)+":"+
                                                "0"+str(row[col_num].minute) if len(str(row[col_num].minute))<=1 else str(row[col_num].day)+"/"+str(row[col_num].month)+"/"+
                                               str(row[col_num].year)+", "+str(row[col_num].hour)+":"+str(row[col_num].minute), font_style)
                else:
                    ws.col(col_num).width = 256 * (len(str(row[col_num])) + 30)
                    ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def test_list(request):
    context = {
        'm_id': request.session['manager_id'],
        'm_uname': request.session['manager_uname']
    }
    try:
        if request.session['manager_id'] is None:
            return render(request, 'manager/m_login.html', {
                'err_msg_login': "You have to be logged in to do this."
            })
    except:
        pass

    tests_completed = Test.objects.filter(completed=True)
    context['t_comp'] = tests_completed
    if len(tests_completed)>0:
        return render(request, 'manager/testexport.html', context)
    else:
        context['err_msg'] = "No Tests that are having completed status."
        return render(request, 'manager/testexport.html', context)


def test_export(request):
    tests = int(request.GET['numoftests'])
    tests_completed = Test.objects.filter(completed=True)[:tests]
    try:
        if request.GET['export'] == "Export":
            return export_as_excel(tests, tests_completed)
    except:
        pass

    try:
        if request.GET['delete'] == "Delete":
            for tc in tests_completed:
                tc.delete()
            t_comp = Test.objects.filter(completed=True)
            return render(request, 'manager/testexport.html', {
                'succ_msg': "Tests Deleted Successfully.",
                't_comp': t_comp
            })
    except:
        pass

    t_comp = Test.objects.filter(completed=True)
    return render(request, 'manager/testexport.html', {
        'err_msg': "Some error has occured.",
        't_comp': t_comp
    })


def print_data(request, test_id):
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
    p.drawCentredString(300, 755, 'Near Passport Seva Kendra')
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
    p.setFont('Times-Roman', 14)
    p.drawCentredString(297, 640, 'Customer Name : '+testpdf.user.first_name)
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