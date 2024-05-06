import smtplib

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core import mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Max
from django.db.models.fields import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from reportlab.lib.styles import getSampleStyleSheet

from myapp.models import *


def login(request):
    return render(request,"loginindex.html")




def login_post(request):
    uname = request.POST['username']
    password = request.POST['password']
    cls = Login.objects.filter(username=uname, password=password)

    if cls.exists():
        clss = Login.objects.get(username=uname, password=password)

        if clss.username != uname or clss.password != password:
            return HttpResponse(
                '''<Script>alert("Invalid user and password!");window.location="/myapp/login/"</Script>''')

        request.session['lid'] = clss.id

        if clss.type == 'admin':
            # ob1 = auth.authenticate(username='admin@gmail.com', password='admin')
            # if ob1 is not None:
            #     auth.login(request, ob1)
            return HttpResponse('''<script>alert("Login Successful");window.location="/myapp/admin_home/"</script>''')
        elif clss.type == 'HOD':
            ob2 = auth.authenticate(username=uname, password=password)
            if ob2 is not None:
                auth.login(request, ob2)
            return HttpResponse('''<script>alert("Login Successful");window.location="/myapp/hod_home"</script>''')
        elif clss.type == 'Tutor':
            ob3 = auth.authenticate(username=uname, password=password)
            if ob3 is not None:
                auth.login(request, ob3)
            return HttpResponse('''<script>alert("Login Successful");window.location="/myapp/staff_home"</script>''')
        else:
            return HttpResponse('''<script>alert("User not found");window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid Username/Password.");window.location="/myapp/login/"</script>''')


def reg(request):
    email  = request.POST['textfield8']
    print(email)
    data = {
        'is_taken': str(Login.objects.filter(username__iexact=email).exists())
    }
    # if data['is_taken']:
    #     data['is_taken']="True"
    print(data['is_taken'], 'dataaaa')
    return JsonResponse({"status":str(data['is_taken']),"data":data})


def logout(request):
    request.session['lid']=''
    return render(request, "loginindex.html")

def admin_home(request):
    return render(request, "admin/admin_home_index.html")

def admindashboard(request):
    return render(request, "admin/admin_home_index1.html")

def view_dept(request):
    if request.session['lid']=='':
        return redirect('/myapp/login/')
    else:
        a=Department.objects.all()
        return render(request, "admin/department.html", {'data':a})

def view_dept_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        name = request.POST['search']
        if name:
            a = Department.objects.filter(dept_name__icontains=name)
        else:
            a = Department.objects.all()
        return render(request, "admin/department.html", {'data':a})

def add_dept(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        return render(request, "admin/add_department.html/")

def add_dept_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        dept_name = request.POST['textfield']
        desc = request.POST['desc']
        a = Department()
        a.dept_name = dept_name
        a.description = desc
        a.save()
        return HttpResponse('''<script>alert("Department Added");window.location="/myapp/add_dept/#about"</script>''')

def edit_dept(request,id):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        a=Department.objects.get(id=id)
        return render(request, "admin/edit_department.html",{'data':a})

def edit_dept_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        dept_name = request.POST['textfield']
        desc = request.POST['desc']
        id = request.POST['id']
        a = Department.objects.get(id=id)
        a.dept_name = dept_name
        a.description = desc
        a.save()
        return HttpResponse('''<script>alert("Department Edited");window.location="/myapp/view_dept/#about"</script>''')

def delete_dept(request,id):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        a = Department.objects.get(id=id).delete()
        return HttpResponse('''<script>alert("Department Deleted");window.location="/myapp/view_dept/#about"</script>''')

def view_course(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        a = Course.objects.all()
        b = Department.objects.all()
        return render(request, "admin/courses.html", {'data':a,'dep':b})

def view_course_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        d=Department.objects.all()
        dep = request.POST['department']
        name = request.POST['search']
        if name:
            a = Course.objects.filter(course_name__icontains=name)
            return render(request, "admin/courses.html", {'data': a, 'dep': d})
        elif dep:
            a = Course.objects.filter(DEPARTMENT_id=dep)
            return render(request, "admin/courses.html", {'data': a, 'dep': d})
        else:
            a = Course.objects.all()
            return render(request, "admin/courses.html", {'data':a,'dep':d})

def add_course(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        s=Department.objects.all()
        return render(request, "admin/add_course.html", {'dep':s})

def add_course_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        course_name = request.POST['textfield']
        department = request.POST['select']
        duration = request.POST['textfield2']
        a = Course()
        a.course_name = course_name
        a.DEPARTMENT_id = department
        a.duration = duration
        a.save()
        return HttpResponse('''<script>alert("Course Added");window.location="/myapp/view_course/"</script>''')

def edit_course(request,id):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        s=Department.objects.all()
        a=Course.objects.get(id=id)
        return render(request, "admin/edit_course.html/", {'data':a,'dep':s})

def edit_course_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        course_name = request.POST['textfield']
        department = request.POST['select']
        duration = request.POST['textfield2']
        id=request.POST['id']
        a=Course.objects.get(id=id)
        a.course_name=course_name
        a.department=department
        a.duration=duration
        a.save()
        return HttpResponse('''<script>alert("Course Edited");window.location="/myapp/view_course/#about"</script>''')

def delete_course(request,id):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        a = Course.objects.get(id=id).delete()
        return HttpResponse('''<script>alert("Course Deleted");window.location="/myapp/view_course/#about"</script>''')

def view_subject(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        b=Subject.objects.all()
        return render(request, "admin/subjects.html", {'data':b})

def view_subject_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        name = request.POST['search']
        if name:
            a = Subject.objects.filter(subject_name__icontains=name)
        else:
            a = Subject.objects.all()
        return render(request, "admin/subjects.html", {'data': a})




def add_subject(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        a = Course.objects.all()
        b=Staff.objects.all()
        return render(request,"admin/subject_add.html",{'cdata':a,'sdata':b})

def add_subject_post(request):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        subject_name=request.POST['textfield']
        semester=request.POST['textfield2']
        course=request.POST['select']
        staff=request.POST['select2']
        c=Subject()
        c.subject_name=subject_name
        c.sem=semester
        c.COURSE_id=course
        c.STAFF_id=staff
        c.save()
        return HttpResponse('''<script>alert("Subject Added");window.location="/myapp/view_subject/#about"</script>''')

def edit_subject(request,id):
    if request.session['lid'] == '':
        return redirect('/myapp/login/')
    else:
        a = Course.objects.all()
        b = Staff.objects.all()
        c=Subject.objects.get(id=id)
        return render(request,"admin/edit_subject.html",{'data1':a,'data2':b,'data3':c})

def edit_subject_post(request):
    subject_name = request.POST['textfield']
    semester = request.POST['textfield2']
    course = request.POST['select']
    staff = request.POST['select2']
    id=request.POST['id']
    c = Subject.objects.get(id=id)
    c.subject_name = subject_name
    c.semester = semester
    c.COURSE_id = course
    c.STAFF_id= staff
    c.save()
    return HttpResponse('''<script>alert("Subject Edited");window.location="/myapp/view_subject/#about"</script>''')

def delete_subject(request,id):
    a = Subject.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Subject Deleted");window.location="/myapp/view_subject/#about"</script>''')



def view_staff(request):
    s=Staff.objects.all()
    d=Department.objects.all()
    return render(request, "admin/staff.html", {'data':s,'dep':d})

def view_staff_post(request):
    d = Department.objects.all()
    dep=request.POST['department']
    name = request.POST['search']
    if name:
        a = Staff.objects.filter(staff_name__startswith=name)
    elif dep:
        a=Staff.objects.filter(DEPARTMENT_id=dep)
    elif name and dep:
        a = Staff.objects.filter(staff_name__startswith=name,DEPARTMENT_id=dep)
    else:
        a = Staff.objects.all()
    return render(request, "admin/staff.html", {'data': a,'dep':d})

def add_staff(request):
    d=Department.objects.all()
    return render(request, "admin/add_staff.html", {'data':d})

def add_staff_post(request):
    staff_name = request.POST['textfield']
    photo = request.FILES['photo']
    dob=request.POST['textfield2']
    gender=request.POST['r1']
    department=request.POST['select1']
    designation=request.POST['select2']
    house=request.POST['textfield3']
    location=request.POST['textfield4']
    pin=request.POST['textfield6']
    phone=request.POST['textfield7']
    email=request.POST['textfield8']
    staff_education=request.POST['textfield10']
    staff_experience=request.POST['textfield11']

    try:
        existing_staff = Staff.objects.get(staff_email=email)
        return HttpResponse(
            '<script>alert("Staff with this email already exists!"); window.location="/myapp/add_staff/#about";</script>')
    except ObjectDoesNotExist:
        pass


    from datetime import datetime
    d=datetime.now().strftime('%Y%m%d_%H%M%S')+".jpg"
    f=FileSystemStorage()
    f.save(d,photo)
    path=f.url(d)

    l=Login()
    l.username=email
    l.password=dob
    l.type=designation
    l.save()

    s=Staff()
    s.staff_name=staff_name
    s.staff_photo=path
    s.staff_dob=dob
    s.gender=gender
    s.DEPARTMENT_id=department
    s.designation=designation
    s.staff_house=house
    s.staff_location=location
    s.staff_pincode=pin
    s.staff_phone=phone
    s.staff_email=email
    s.staff_education=staff_education
    s.staff_experience=staff_experience
    s.LOGIN=l
    s.save()
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login("ats.kmct@gmail.com","tlac urcf svwy mupy")
    to=email
    subject="KMCT-ATS credentials"
    body="Hi "+str(staff_name)+",\n""Your registration to ATS has been completed successfully.\nPlease refer your login credentials to ATS and reset the default password immedietly.\n\nUsername: " + str(email) + "\nPassword: "+str(dob)+"\n\nThanks,\nAdmin\nATS"
    msg=f"Subject:{subject}\n\n{body}"
    server.sendmail("ats.kmct@gmail.com",to,msg)
    server.quit()
    return HttpResponse('''<script>alert("Staff Added");window.location="/myapp/view_staff/#about"</script>''')


def edit_staff(request,id):
    a=Department.objects.all()
    b=Staff.objects.get(LOGIN=id)
    return render(request, "admin/edit_staff.html", {'data1':a,'data2':b})

def edit_staff_post(request):
    staff_name = request.POST['textfield']
    # photo = request.FILES['photo']
    dob = request.POST['textfield2']
    gender = request.POST['r1']
    department = request.POST['select1']
    designation = request.POST['select2']
    house = request.POST['textfield3']
    location = request.POST['textfield4']
    pin = request.POST['textfield6']
    phone = request.POST['textfield7']
    email = request.POST['textfield8']
    staff_education = request.POST['textfield10']
    staff_experience = request.POST['textfield11']
    id=request.POST['id']

    s = Staff.objects.get(LOGIN=id)

    if 'photo' in request.FILES:
        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        f = FileSystemStorage()
        photo = request.FILES['photo']
        f.save(d, photo)
        path = f.url(d)
        s.staff_photo = path
        s.save()


    s.staff_name = staff_name
    s.staff_dob = dob
    s.gender = gender
    s.DEPARTMENT_id = department
    s.designation = designation
    s.staff_house = house
    s.staff_location = location
    s.staff_pincode = pin
    s.staff_phone = phone
    s.staff_email = email
    s.staff_education = staff_education
    s.staff_experience = staff_experience
    s.save()


    l = Login.objects.get(id=id)
    l.username = email
    l.type = designation
    l.save()

    return HttpResponse('''<script>alert("Staff Edited");window.location="/myapp/view_staff/#about"</script>''')



def delete_staff(request,id):
    a = Staff.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Staff Deleted");window.location="/myapp/view_staff/#about"</script>''')



def view_student(request):
    s=Student.objects.all()
    d=Department.objects.all()
    return render(request, "admin/student.html", {'data':s,'dep':d})

def view_student_post(request):
    d = Department.objects.all()
    dep=request.POST['department']
    name = request.POST['search']
    if name:
        a = Student.objects.filter(student_name__startswith=name)
    elif dep:
        a = Student.objects.filter(DEPARTMENT_id=dep)
    elif dep and name:
        a = Student.objects.filter(student_name__startswith=name,DEPARTMENT_id=dep)
    else:
        a = Student.objects.all()
    return render(request, "admin/student.html", {'data': a,'dep':d})

def add_student(request):
    d=Department.objects.all()
    c=Course.objects.all()
    return render(request, "admin/add_student.html", {'data':d, 'data1':c})

def add_student_post(request):
    student_name = request.POST['textfield']
    photo = request.FILES['photo']
    dob = request.POST['textfield2']
    gender = request.POST['r1']
    parent_name = request.POST['pname']
    department = request.POST['select1']
    course = request.POST['select2']
    house = request.POST['textfield3']
    location = request.POST['textfield4']
    pin = request.POST['textfield6']
    phone = request.POST['textfield7']
    email = request.POST['textfield8']
    semester = request.POST['textfield10']

    try:
        existing_student = Student.objects.get(student_email=email)
        return HttpResponse(
            '<script>alert("Student with this email already exists!"); window.location="/myapp/add_student/#about";</script>')
    except ObjectDoesNotExist:
        pass

    from datetime import datetime
    d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
    f = FileSystemStorage()
    f.save(d, photo)
    path = f.url(d)

    l = Login()
    l.username = email
    l.password = dob
    l.type = 'student'
    l.save()

    v = Login()
    v.username = email
    v.password = phone
    v.type = 'parent'
    v.save()

    s = Student()
    s.student_name = student_name
    s.student_photo = path
    s.student_dob = dob
    s.gender = gender
    s.DEPARTMENT_id = department
    s.COURSE_id = course
    s.student_house = house
    s.student_location = location
    s.student_pincode = pin
    s.student_phone = phone
    s.student_email = email
    s.parent_name = parent_name
    s.sem = semester
    s.LOGIN = l
    s.save()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("ats.kmct@gmail.com", "tlac urcf svwy mupy")
    to = email
    subject = "Your registration on KMCT college has been completed"
    body = "Hi "+str(student_name)+",\n""Your registration to KMCT college has been completed successfully.\nPlease refer your login credentials to ATS app and reset the default password immedietly.\n\nStudent Username: " + str(email) + "\nStudent Password: "+str(dob)+"\nParent Password: "+str(phone)+"\n\nThanks,\nAdmin\nATS"
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail("ats.kmct@gmail.com", to, msg)
    server.quit()
    return HttpResponse('''<script>alert("Student Added");window.location="/myapp/view_student/#about"</script>''')



def edit_student(request,id):
    a = Department.objects.all()
    b = Student.objects.get(LOGIN=id)
    c = Course.objects.all()
    return render(request, "admin/edit_student.html", {'data1':a,'data2':b,'data3':c})

def edit_student_post(request):
    student_name = request.POST['textfield']
    # photo = request.FILES['photo']
    dob = request.POST['textfield2']
    gender = request.POST['r1']
    parent_name = request.POST['pname']
    department = request.POST['select1']
    course = request.POST['select2']
    house = request.POST['textfield3']
    location = request.POST['textfield4']
    pin = request.POST['textfield6']
    phone = request.POST['textfield7']
    email = request.POST['textfield8']
    # password = request.POST['textfield9']
    semester = request.POST['textfield10']
    id=request.POST['id']

    s = Student.objects.get(LOGIN=id)


    if 'photo' in request.FILES:
        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        f = FileSystemStorage()
        photo = request.FILES['photo']
        f.save(d, photo)
        path = f.url(d)
        s.student_photo = path
        s.save()


    s.student_name = student_name
    # s.student_photo = path
    s.student_dob = dob
    s.gender = gender
    s.DEPARTMENT_id = department
    s.COURSE_id = course
    s.student_house = house
    s.student_location = location
    s.student_pincode = pin
    s.student_phone = phone
    s.student_email = email
    s.parent_name = parent_name
    s.sem = semester
    s.save()
    l = Login.objects.get(id=id)
    l.username = email
    l.save()
    return HttpResponse('''<script>alert("Student Edited");window.location="/myapp/view_student/#about"</script>''')


def delete_student(request,id):
    a = Student.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Student Deleted");window.location="/myapp/view_student/#about"</script>''')





def addsubcheck(request):
    cid=request.POST['cid']
    cc=Course.objects.get(id=cid).DEPARTMENT_id
    print(cc)
    ss=Staff.objects.filter(DEPARTMENT__id=cc)
    l=[]
    for i in ss:
        l.append({"id":i.id,"staff_name":i.staff_name})
    return JsonResponse({"status":"ok","data":l})




def addstudcheck(request):
    did=request.POST['cid']
    d=Department.objects.get(id=did).id
    print(d)
    c=Course.objects.filter(DEPARTMENT__id=d)
    l=[]
    for i in c:
        l.append({"id":i.id,"course_name":i.course_name})
    return JsonResponse({"status":"ok","data":l})







# ----------------------------------------------HOD------------------------------------------------------------------------------------









def hod_home(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).staff_name
    return render(request, "staff/hod_home_index.html",{'name':ff})

def hod_view_subject(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    b=Subject.objects.filter(COURSE__DEPARTMENT=ff)
    return render(request, "staff/hod_subjects.html", {'data':b})

def hod_view_subject_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    name = request.POST['search']
    if name:
        a = Subject.objects.filter(subject_name__icontains=name,COURSE__DEPARTMENT_id=ff)
    else:
        a = Subject.objects.filter(COURSE__DEPARTMENT_id=ff)
    return render(request, "staff/hod_subjects.html", {'data': a})



def hod_add_subject(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    a = Course.objects.filter(DEPARTMENT_id=ff)
    b=Staff.objects.filter(DEPARTMENT_id=ff)
    return render(request,"staff/hod_subject_add.html",{'cdata':a,'sdata':b})


def hod_add_subject_post(request):
    subject_name=request.POST['textfield']
    semester=request.POST['textfield2']
    course=request.POST['select']
    staff=request.POST['select2']
    c=Subject()
    c.subject_name=subject_name
    c.sem=semester
    c.COURSE_id=course
    c.STAFF_id=staff
    c.save()
    return HttpResponse('''<script>alert("Subject Added");window.location="/myapp/hod_view_subject/#about"</script>''')

def hod_edit_subject(request,id):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    a = Course.objects.filter(DEPARTMENT_id=ff)
    b = Staff.objects.filter(DEPARTMENT_id=ff)
    c=Subject.objects.get(id=id)
    return render(request,"staff/hod_edit_subject.html",{'data1':a,'data2':b,'data3':c})

def hod_edit_subject_post(request):
    subject_name = request.POST['textfield']
    semester = request.POST['textfield2']
    course = request.POST['select']
    staff = request.POST['select2']
    id=request.POST['id']
    c = Subject.objects.get(id=id)
    c.subject_name = subject_name
    c.semester = semester
    c.COURSE_id = course
    c.STAFF_id= staff
    c.save()
    return HttpResponse('''<script>alert("Subject Edited");window.location="/myapp/hod_view_subject/#about"</script>''')

def hod_delete_subject(request,id):
    a = Subject.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Subject Deleted");window.location="/myapp/hod_view_subject/#about"</script>''')



def hod_view_student(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    s=Student.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/hod_student.html", {'data':s})

def hod_view_student_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    name = request.POST['search']
    if name:
        a = Student.objects.filter(student_name__startswith=name,DEPARTMENT_id=ff)
    else:
        a = Student.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/hod_student.html", {'data': a})



def hod_add_student(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    d=Department.objects.get(id=ff)
    c=Course.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/hod_add_student.html", {'data':d, 'data1':c})

def hod_add_student_post(request):
    student_name = request.POST['textfield']
    photo = request.FILES['photo']
    dob = request.POST['textfield2']
    gender = request.POST['r1']
    parent_name = request.POST['pname']
    department = request.POST['select1']
    course = request.POST['select2']
    house = request.POST['textfield3']
    location = request.POST['textfield4']
    pin = request.POST['textfield6']
    phone = request.POST['textfield7']
    email = request.POST['textfield8']
    semester = request.POST['textfield10']

    try:
        existing_student = Student.objects.get(student_email=email)
        return HttpResponse(
            '<script>alert("Student with this email already exists!"); window.location="/myapp/hod_add_student/#about";</script>')
    except ObjectDoesNotExist:
        pass

    from datetime import datetime
    d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
    f = FileSystemStorage()
    f.save(d, photo)
    path = f.url(d)

    l = Login()
    l.username = email
    l.password = dob
    l.type = 'student'
    l.save()

    v = Login()
    v.username = email
    v.password = phone
    v.type = 'parent'
    v.save()

    s = Student()
    s.student_name = student_name
    s.student_photo = path
    s.student_dob = dob
    s.gender = gender
    s.DEPARTMENT_id = department
    s.COURSE_id = course
    s.student_house = house
    s.student_location = location
    s.student_pincode = pin
    s.student_phone = phone
    s.student_email = email
    s.parent_name = parent_name
    s.sem = semester
    s.LOGIN = l
    s.save()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("ats.kmct@gmail.com", "tlac urcf svwy mupy")
    to = email
    subject = "Your registration on KMCT college has been completed"
    body = "Hi " + str(student_name) + ",\n""Your registration to KMCT college has been completed successfully.\nPlease refer your login credentials to ATS app and reset the default password immedietly.\n\nStudent Username: " + str(
        email) + "\nStudent Password: " + str(dob) + "\nParent Password: " + str(phone) + "\n\nThanks,\nAdmin\nATS"
    msg = f"Subject:{subject}\n\n{body}"
    server.sendmail("ats.kmct@gmail.com", to, msg)
    server.quit()
    return HttpResponse('''<script>alert("Student Added");window.location="/myapp/hod_view_student/#about"</script>''')



def hod_edit_student(request,id):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    a = Department.objects.get(id=ff)
    b = Student.objects.get(LOGIN=id)
    c = Course.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/hod_edit_student.html", {'data1':a,'data2':b,'data3':c})




def hod_edit_student_post(request):
    student_name = request.POST['textfield']
    # photo = request.FILES['photo']
    dob = request.POST['textfield2']
    gender = request.POST['r1']
    parent_name = request.POST['pname']
    department = request.POST['select1']
    course = request.POST['select2']
    house = request.POST['textfield3']
    location = request.POST['textfield4']
    pin = request.POST['textfield6']
    phone = request.POST['textfield7']
    email = request.POST['textfield8']
    # password = request.POST['textfield9']
    semester = request.POST['textfield10']
    id=request.POST['id']

    s = Student.objects.get(LOGIN=id)


    if 'photo' in request.FILES:
        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        f = FileSystemStorage()
        photo = request.FILES['photo']
        f.save(d, photo)
        path = f.url(d)
        s.student_photo = path
        s.save()


    s.student_name = student_name
    # s.student_photo = path
    s.student_dob = dob
    s.gender = gender
    s.DEPARTMENT_id = department
    s.COURSE_id = course
    s.student_house = house
    s.student_location = location
    s.student_pincode = pin
    s.student_phone = phone
    s.student_email = email
    s.parent_name = parent_name
    s.sem = semester
    s.save()
    l = Login.objects.get(id=id)
    l.username = email
    l.save()
    return HttpResponse('''<script>alert("Student Edited");window.location="/myapp/hod_view_student/#about"</script>''')


def hod_delete_student(request,id):
    a = Student.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Student Deleted");window.location="/myapp/hod_view_student/#about"</script>''')



def view_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff/profile.html", {'data':ff})

def view_profile_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff/profile.html", {'data':ff})

def edit_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff/profile.html/", {'data':ff})


def edit_profile_post(request):
    staff_name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['r1']
    house = request.POST['hname']
    location = request.POST['loc']
    pin = request.POST['pin']
    phone = request.POST['phone']
    email = request.POST['email']
    staff_education = request.POST['edu1']
    staff_experience = request.POST['edu2']
    password = request.POST['password']

    if 'photo' in request.FILES:
        photo = request.FILES['photo']

        print(photo)

        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d%H%M%S') + ".jpg"
        f = FileSystemStorage()
        f.save(d, photo)
        path = f.url(d)

        s = Staff.objects.get(LOGIN_id=request.session['lid'])
        s.staff_photo = path
        s.staff_name = staff_name
        s.staff_dob = dob
        s.gender = gender
        s.staff_house = house
        s.staff_location = location
        s.staff_pincode = pin
        s.staff_phone = phone
        s.staff_email = email
        s.staff_education = staff_education
        s.staff_experience = staff_experience
        s.save()

        l = Login.objects.get(id=request.session['lid'])
        l.username = email
        l.password = password
        l.save()
        s.save()
        return HttpResponse('''<script>alert("Profile Edited");window.location="/myapp/view_profile/"</script>''')

    else:
        s = Staff.objects.get(LOGIN_id=request.session['lid'])

        s.staff_name = staff_name
        s.staff_dob = dob
        s.gender = gender
        s.staff_house = house
        s.staff_location = location
        s.staff_pincode = pin
        s.staff_phone = phone
        s.staff_email = email
        s.staff_education = staff_education
        s.staff_experience = staff_experience
        s.save()

        l = Login.objects.get(id=request.session['lid'])
        l.username = email
        l.password = password
        l.save()

        return HttpResponse('''<script>alert("Profile Edited");window.location="/myapp/view_profile/"</script>''')


def add_timetable(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    c=Course.objects.filter(DEPARTMENT_id=ff)
    b=Subject.objects.filter(COURSE__DEPARTMENT=ff)
    return render(request, "staff/hod_add_titmetable.html", {'data1':c,'data2':b})

def add_timetable_post(request):
    course = request.POST['select1']
    sem = request.POST['sem']
    day = request.POST['select3']
    h1 = request.POST['select4']
    h2 = request.POST['select5']
    h3 = request.POST['select6']
    h4 = request.POST['select7']
    h5 = request.POST['select8']
    h6 = request.POST['select9']
    t=Timetable()
    t.COURSE_id=course
    t.sem=sem
    t.Day=day
    t.SUBJECT_1_id=h1
    t.SUBJECT_2_id=h2
    t.SUBJECT_3_id=h3
    t.SUBJECT_4_id=h4
    t.SUBJECT_5_id=h5
    t.SUBJECT_6_id=h6
    t.save()
    return HttpResponse('''<script>alert("Timetable Added");window.location="/myapp/view_timetable/"</script>''')


def edit_timetable(request,id):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    c=Course.objects.filter(DEPARTMENT_id=ff)
    b=Subject.objects.filter(COURSE__DEPARTMENT=ff)
    d=Timetable.objects.get(id=id)
    return render(request, "staff/hod_edit_titmetable.html", {'data1':c,'data2':b,'data3':d})


def edit_timetable_post(request):
    course = request.POST['select1']
    sem = request.POST['sem']
    day = request.POST['select3']
    h1 = request.POST['select4']
    h2 = request.POST['select5']
    h3 = request.POST['select6']
    h4 = request.POST['select7']
    h5 = request.POST['select8']
    h6 = request.POST['select9']
    t=Timetable()
    t.COURSE_id=course
    t.sem=sem
    t.Day=day
    t.SUBJECT_1_id=h1
    t.SUBJECT_2_id=h2
    t.SUBJECT_3_id=h3
    t.SUBJECT_4_id=h4
    t.SUBJECT_5_id=h5
    t.SUBJECT_6_id=h6
    t.save()
    return HttpResponse('''<script>alert("Timetable Added");window.location="/myapp/view_timetable/"</script>''')






def view_timetable(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    res=Timetable.objects.filter(COURSE__DEPARTMENT_id=ff)
    return render(request,"staff/view_timetable.html",{'data':res})

def view_timetable_post(request):
    sem = request.POST['search']
    if sem:
        a = Timetable.objects.filter(sem=sem)
    else:
        a = Student.objects.filter(sem=1)
    return render(request, "staff/view_timetable.html", {'data': a})



def delete_timetable(request,id):
    a = Timetable.objects.get(id=id).delete()
    return HttpResponse('''<script>alert("Timetable Deleted");window.location="/myapp/view_timetable/#about"</script>''')



##########################################-----------STAFF-------------###########################################################




def staff_home(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).staff_name
    return render(request, "staff/staff_home_index.html",{'name':ff})


def staff_view_timetable(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    res = Timetable.objects.filter(COURSE__DEPARTMENT_id=ff)
    return render(request, "staff/staff_view_timetable.html", {'data': res})

def staff_view_timetable_post(request):
    sem = request.POST['search']
    if sem:
        a = Timetable.objects.filter(sem=sem)
    else:
        a = Student.objects.filter(sem=1)
    return render(request, "staff/staff_view_timetable.html", {'data': a})

def staff_view_student(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    s=Student.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/staff_student.html", {'data':s})

def staff_view_student_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    name = request.POST['search']
    if name:
        a = Student.objects.filter(student_name__startswith=name,DEPARTMENT_id=ff)
    else:
        a = Student.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/staff_student.html", {'data': a})


def staff_view_subject(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    b=Subject.objects.filter(COURSE__DEPARTMENT=ff)
    return render(request, "staff/staff_subjects.html", {'data':b})

def staff_view_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff/staff_profile.html", {'data':ff})

def staff_view_subject_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    name = request.POST['search']
    if name:
        a = Subject.objects.filter(subject_name__icontains=name,COURSE__DEPARTMENT_id=ff)
    else:
        a = Subject.objects.filter(COURSE__DEPARTMENT_id=ff)
    return render(request, "staff/staff_subjects.html", {'data': a})



def staff_view_profile_post(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff/staff_profile.html", {'data':ff})

def staff_edit_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "staff/staff_profile.html/", {'data':ff})


def staff_edit_profile_post(request):
    staff_name = request.POST['name']
    dob = request.POST['dob']
    gender = request.POST['r1']
    house = request.POST['hname']
    location = request.POST['loc']
    pin = request.POST['pin']
    phone = request.POST['phone']
    email = request.POST['email']
    staff_education = request.POST['edu1']
    staff_experience = request.POST['edu2']
    password = request.POST['password']

    s = Staff.objects.get(LOGIN_id=request.session['lid'])

    if 'photo' in request.FILES:
        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        f = FileSystemStorage()
        photo = request.FILES['photo']
        f.save(d, photo)
        path = f.url(d)
        s.staff_photo = path
        s.save()

    s.staff_name = staff_name
    s.staff_dob = dob
    s.gender = gender
    s.staff_house = house
    s.staff_location = location
    s.staff_pincode = pin
    s.staff_phone = phone
    s.staff_email = email
    s.staff_education = staff_education
    s.staff_experience = staff_experience
    s.save()

    l = Login.objects.get(id=request.session['lid'])
    l.username = email
    l.password = password
    l.save()

    return HttpResponse('''<script>alert("Profile Edited");window.location="/myapp/staff_view_profile/"</script>''')






def staff_view_leave(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).id
    l=Leave.objects.filter(STAFF=ff,status='Pending')
    return render(request, "staff/leave_request.html/",{'data':l})


def staff_view_leave_post(request):
    name = request.POST['search']
    date =request.POST['date']
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).id
    if name:
        a = Leave.objects.filter(STAFF=ff, STUDENT__student_name__istartswith=name, status='Pending')
        return render(request, "staff/leave_request.html/", {'data':a})
    elif date:
        a = Leave.objects.filter(STAFF=ff,status='Pending',start_date=date)
        return render(request, "staff/leave_request.html/", {'data': a})
    elif name and date:
        a = Leave.objects.filter(STAFF=ff, status='Pending', start_date=date,STUDENT__student_name__istartswith=name)
        return render(request, "staff/leave_request_history.html/", {'data': a})
    else:
        l = Leave.objects.filter(STAFF=ff, status='Pending')
        return render(request, "staff/leave_request.html/", {'data': l})




def staff_leave_history(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).id
    l = Leave.objects.filter(STAFF=ff, status='Approved' or 'Rejected')
    return render(request, "staff/leave_request_history.html/", {'data': l})

def staff_leave_history_post(request):
    name=request.POST['search']
    date=request.POST['date']
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).id
    if name:
        a=Leave.objects.filter(STAFF=ff,STUDENT__student_name__istartswith=name,status='Approved' or 'Rejected')
        return render(request, "staff/leave_request_history.html", {'data':a})
    elif date:
        a = Leave.objects.filter(STAFF=ff, status='Approved' or 'Rejected', start_date=date)
        return render(request, "staff/leave_request_history.html/", {'data': a})
    elif name and date:
        a = Leave.objects.filter(STAFF=ff, status='Approved' or 'Rejected', start_date=date,STUDENT__student_name__istartswith=name)
        return render(request, "staff/leave_request_history.html/", {'data': a})
    else:
        l = Leave.objects.filter(STAFF=ff, status='Approved' or 'Rejected')
        return render(request, "staff/leave_request_history.html/", {"data":l})



def approve_leave(request,id):
    p=Leave.objects.filter(pk=id).update(status='Approved')
    return HttpResponse('''<script>alert("Leave Approved");window.location="/myapp/staff_view_leave/"</script>''')

def reject_leave(request,id):
    p = Leave.objects.filter(pk=id).update(status='Rejected')
    return HttpResponse('''<script>alert("Leave Rejected");window.location="/myapp/staff_view_leave/"</script>''')



def chat(request,id):
    sid = id
    # qry = Staff.objects.get(LOGIN=cid)

    qry = Student.objects.get(id=sid)
    toid = Login.objects.filter(username=qry.student_email, type='parent')[0].id
    request.session["userid"] = str(toid)
    cid = str(request.session["userid"])
    request.session["new"] = cid
    return render(request, "staff/chat.html", {'photo': qry.student_photo, 'name': qry.student_name, 'toid': str(toid)})

def chat_view(request):
    fromid = request.session["lid"]
    toid = request.session["userid"]
    qry = Student.objects.get(student_email=Login.objects.get(id=request.session["userid"], type='parent').username)
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.date.strftime("%Y-%m-%d")+"<br>"+i.desc, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    return JsonResponse({'photo': qry.student_photo, "data": l, 'name': qry.parent_name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.session["lid"]
    toid = request.session["userid"]
    message = msg
    # qry = Student.objects.get(student_email=Login.objects.get(id=request.session["userid"], type='parent').username)

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.desc = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})



def view_parentchat(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    res=Student.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/view_parent.html", {'data':res,})



def hod_view_parentchat(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT.id
    res=Student.objects.filter(DEPARTMENT_id=ff)
    return render(request, "staff/hod_view_parent.html", {'data':res,})








def hod_view_attendance(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    res=Student.objects.filter(DEPARTMENT_id=ff)

    ls=[]
    for i in res:

        m=[]
        m.append(i.student_name)
        h = ["1", "2", "3", "4", "5", "6"]
        for  k in h:

            d=Attendance.objects.filter(STUDENT=i, period=k, date=datetime.now().date())
            if d.exists():
                print(datetime,"Helllo",k)
                m.append(1)
            else:
                print(datetime, "hi",k)
                m.append(0)

        ls.append(m)


    print(ls)
    return render(request, 'staff/hod_view_attendance.html', {"data": ls, 'date':datetime.now().date()})












def hod_view_attendance_post(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    date=request.POST['date']
    name=request.POST['name']
    sem=request.POST['sem']


    if date!='' and name!='' and sem!='':
        # d = date.strftime("%B %d, %Y")
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff, student_name__icontains=name,sem=sem)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(period=k,date=date)
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
        return render(request, 'staff/hod_view_attendance.html', {"data": ls, 'date':date})
    elif date!='':
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(STUDENT=i, period=k, date=date)
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
        return render(request, 'staff/hod_view_attendance.html', {"data": ls, 'date':date})
    elif name!='':
        # d=datetime.now().strftime("%Y-%m-%d")
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff, student_name__icontains=name)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter( period=k, STUDENT__student_name__icontains=name)
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
        return render(request, 'staff/hod_view_attendance.html', {"data": ls, 'date':date})
    elif sem:
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff, sem=sem)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(STUDENT=i, period=k, date=datetime.now())
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
            print(ls)
        return render(request, 'staff/hod_view_attendance.html', {"data": ls, 'date': date})
    else:
        # d = datetime.now().strftime("%Y-%m-%d")
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(STUDENT=i, period=k, date=datetime.now())
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
            print(ls)
        return render(request, 'staff/hod_view_attendance.html', {"data": ls, 'date':date})










def staff_view_attendance(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    res=Student.objects.filter(DEPARTMENT_id=ff)

    ls=[]
    for i in res:

        m=[]
        m.append(i.student_name)
        h = ["1", "2", "3", "4", "5", "6"]
        for  k in h:

            d=Attendance.objects.filter(STUDENT=i, period=k, date=datetime.now().date())
            if d.exists():
                print(datetime,"Helllo",k)
                m.append(1)
            else:
                print(datetime, "hi",k)
                m.append(0)

        ls.append(m)


    print(ls)
    return render(request, 'staff/staff_view_attendance.html', {"data": ls, 'date':datetime.now().date()})










def staff_view_attendance_post(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    date=request.POST['date']
    name=request.POST['name']
    if date!='' and name!='':
        # d = date.strftime("%B %d, %Y")
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff, student_name__icontains=name)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(period=k,date=date)
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
        return render(request, 'staff/staff_view_attendance.html', {"data": ls, 'date':date})
    elif date!='':
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(STUDENT=i, period=k, date=date)
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
        return render(request, 'staff/staff_view_attendance.html', {"data": ls, 'date':date})
    elif name!='':
        # d=datetime.now().strftime("%Y-%m-%d")
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff, student_name__icontains=name)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter( period=k, STUDENT__student_name__icontains=name,date=datetime.now().date())
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
        return render(request, 'staff/staff_view_attendance.html', {"data": ls, 'date':datetime.now().date()})
    else:
        # d = datetime.now().strftime("%Y-%m-%d")
        ls = []
        res = Student.objects.filter(DEPARTMENT_id=ff, student_name__icontains=name)
        for i in res:

            m = []
            m.append(i.student_name)
            h = ["1", "2", "3", "4", "5", "6"]
            for k in h:

                d = Attendance.objects.filter(STUDENT=i, period=k, date=datetime.now())
                if d.exists():
                    print(datetime, "Helllo", k)
                    m.append(1)
                else:
                    print(datetime, "hi", k)
                    m.append(0)

            ls.append(m)
            print(ls)
        return render(request, 'staff/staff_view_attendance.html', {"data": ls, 'date':date})







def attendance_subject(request):
    lid = request.session['lid']
    dep = Staff.objects.get(LOGIN_id=lid).DEPARTMENT.id
    sa = Student.objects.filter(DEPARTMENT_id=dep)
    if len(sa) < 1:
        return HttpResponse(
            '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
    subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
    print(subject, "hello")
    fnl = []
    for i in subject:
        m = []
        l = []
        att = Attendance.objects.filter(SUBJECT=i)
        for ii in att:
            aa = str(ii.period) + str(ii.date)
            if aa not in m:
                m.append(aa)

        l.append(i.subject_name)

        for j in sa:
            s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
            count=0
            ss = 0
            try:
                ss = float(len(s)) / float(len(m))
            except:
                ss = 0
            ss=ss*100
            sss=str(ss)

            l.append(
                sss+" %"
            )
        fnl.append(l)

    print(fnl)

    fnl=[list(i) for i in zip(*fnl)]


    j=-1
    kk=[]
    for i in fnl:
        k=[]
        if j==-1:
            k.append("")
            j=j+1

        else:
            k.append(sa[j].student_name)
            j=j+1
        for m in i:
            k.append(m)
        kk.append(k)
    return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})






def attendance_subject_post(request):
    lid = request.session['lid']
    name=request.POST['name']
    sub=request.POST['subject']
    dep = Staff.objects.get(LOGIN_id=lid).DEPARTMENT.id
    if name:
        sa = Student.objects.filter(DEPARTMENT_id=dep,student_name__icontains=name)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})

    if sub:
        sa = Student.objects.filter(DEPARTMENT_id=dep)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem,subject_name__icontains=sub)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})

    if name and sub:
        sa = Student.objects.filter(DEPARTMENT_id=dep,student_name__icontains=name)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem,subject_name__icontains=sub)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})

    else:
        sa = Student.objects.filter(DEPARTMENT_id=dep)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})


def staff_attendance_subject(request):
    lid = request.session['lid']
    dep = Staff.objects.get(LOGIN_id=lid).DEPARTMENT.id
    sa = Student.objects.filter(DEPARTMENT_id=dep)
    if len(sa) < 1:
        return HttpResponse(
            '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
    subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
    print(subject, "hello")
    fnl = []
    for i in subject:
        m = []
        l = []
        att = Attendance.objects.filter(SUBJECT=i)
        for ii in att:
            aa = str(ii.period) + str(ii.date)
            if aa not in m:
                m.append(aa)

        l.append(i.subject_name)

        for j in sa:
            s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
            count = 0
            ss = 0
            try:
                ss = float(len(s)) / float(len(m))
            except:
                ss = 0
            ss = ss * 100
            sss = str(ss)

            l.append(
                sss + " %"
            )
        fnl.append(l)

    print(fnl)

    fnl = [list(i) for i in zip(*fnl)]

    j = -1
    kk = []
    for i in fnl:
        k = []
        if j == -1:
            k.append("")
            j = j + 1

        else:
            k.append(sa[j].student_name)
            j = j + 1
        for m in i:
            k.append(m)
        kk.append(k)
    return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})


def staff_attendance_subject_post(request):
    lid = request.session['lid']
    name = request.POST['name']
    sub = request.POST['subject']
    dep = Staff.objects.get(LOGIN_id=lid).DEPARTMENT.id
    if name:
        sa = Student.objects.filter(DEPARTMENT_id=dep, student_name__icontains=name)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})

    if sub:
        sa = Student.objects.filter(DEPARTMENT_id=dep)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem, subject_name__icontains=sub)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})

    if name and sub:
        sa = Student.objects.filter(DEPARTMENT_id=dep, student_name__icontains=name)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem, subject_name__icontains=sub)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})

    else:
        sa = Student.objects.filter(DEPARTMENT_id=dep)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)
        return render(request, "staff/attendance_subject.html", {'data': kk, 'sa': sa})


def attendance_month(request):
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    a = Attendance.objects.all()
    students = Student.objects.filter(DEPARTMENT_id=ff)
    l =[]
    attendance =[]

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter(date__month=datetime.now().month).values_list('date').distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id, date__month=datetime.now().month).values_list('date','period').distinct()
        total=(ttlAtt*6)
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt/total)*100
            d = str(percentage)
            l.append({
                'Std': i.student_name,
                'cnt': tcnt,
                'total':int(total),
                'percentage': d[:4] + " %",
            })
        m=datetime.now().month
        if m==1:
            month='January'
        elif m==2:
            month='February'
        elif m==3:
            month='March'
        elif m==4:
            month='April'
        elif m==5:
            month='May'
        elif m==6:
            month='June'
        elif m==7:
            month='July'
        elif m==8:
            month='August'
        elif m==9:
            month='September'
        elif m==10:
            month='October'
        elif m==11:
            month='November'
        elif m==12:
            month='December'
    return render(request, "staff/attendance_month.html",{'data':l,'month':month})


def attendance_month_post(request):
    name=request.POST['name']
    month=request.POST['month']
    if month == '01':
        months = 'January'
    elif month == '02':
        months = 'February'
    elif month == '3':
        months = 'March'
    elif month == '04':
        months = 'April'
    elif month == '05':
        months = 'May'
    elif month == '06':
        months = 'June'
    elif month == '07':
        months = 'July'
    elif month == '08':
        months = 'August'
    elif month == '09':
        months = 'September'
    elif month == '10':
        months = 'October'
    elif month == '11':
        months = 'November'
    elif month == '12':
        months = 'December'


    if month:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
                'date','period').distinct()
            total=(ttlAtt*6)
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d=str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4]+" %",
                })

    elif name:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(student_name__icontains=name,DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=datetime.now().month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
                'date', 'period').distinct()
            total = (ttlAtt*6)/4
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4] + " %",
                })

    elif name and month:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(student_name__icontains=name,DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
                'date', 'period').distinct()
            total = (ttlAtt*6)/4
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4] + " %",
                })
    else:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []
        # for i in a:

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=datetime.now().month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=datetime.now().month).values_list('date',
                                                                                                           'period').distinct()
            total = ttlAtt * 6
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4] + " %",
                })


    return render(request, "staff/attendance_month.html",{'month':months,'data':l})




def staff_attendance_month(request):
    a = Attendance.objects.all()
    ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    students = Student.objects.filter(DEPARTMENT_id=ff)
    l =[]
    attendance =[]

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter(date__month=datetime.now().month).values_list('date').distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id, date__month=datetime.now().month).values_list('date','period').distinct()
        total=(ttlAtt*6)
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt/total)*100
            d = str(percentage)
            l.append({
                'Std': i.student_name,
                'cnt': tcnt,
                'total': int(total),
                'percentage': d[:4] + " %",
            })
        m=datetime.now().month
        if m==1:
            month='January'
        elif m==2:
            month='February'
        elif m==3:
            month='March'
        elif m==4:
            month='April'
        elif m==5:
            month='May'
        elif m==6:
            month='June'
        elif m==7:
            month='July'
        elif m==8:
            month='August'
        elif m==9:
            month='September'
        elif m==10:
            month='October'
        elif m==11:
            month='November'
        elif m==12:
            month='December'
    return render(request, "staff/staff_attendance_month.html",{'data':l,'month':month})


def staff_attendance_month_post(request):
    name=request.POST['name']
    month=request.POST['month']
    if month == '01':
        months = 'January'
    elif month == '02':
        months = 'February'
    elif month == '03':
        months = 'March'
    elif month == '04':
        months = 'April'
    elif month == '05':
        months = 'May'
    elif month == '06':
        months = 'June'
    elif month == '07':
        months = 'July'
    elif month == '08':
        months = 'August'
    elif month == '09':
        months = 'September'
    elif month == '10':
        months = 'October'
    elif month == '11':
        months = 'November'
    elif month == '12':
        months = 'December'


    if month:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
                'date','period').distinct()
            total=(ttlAtt*6)
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d=str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4]+" %",
                })

    if name:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(student_name__icontains=name,DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=datetime.now().month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
                'date', 'period').distinct()
            total = (ttlAtt*6)/4
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4] + " %",
                })

    if name and month:
        ff = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(student_name__icontains=name,DEPARTMENT_id=ff)
        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=month).values_list('date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
                'date', 'period').distinct()
            total = (ttlAtt*6)/4
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4] + " %",
                })



    return render(request, "staff/staff_attendance_month.html",{'month':months,'data':l})



def hod_attendance_total(request):
    f = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    a = Attendance.objects.all()
    students = Student.objects.filter(DEPARTMENT_id=f)
    l = []
    attendance = []

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter().values_list().distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
            'date','period').distinct()
        total=ttlAtt*6
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt / total) * 100
            d=str(percentage)


            l.append({
                'name' : i.student_name,
                'cnt': tcnt,
                'total':int(total),
                'percentage': d[:4]+" %",
            })

    return render(request, "staff/hod_attendance_total.html", {'data':l})



def hod_attendance_total_post(request):
    name=request.POST['name']
    f = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    a = Attendance.objects.all()
    if name:
        students = Student.objects.filter(DEPARTMENT_id=f,student_name__icontains=name)
        l = []
        attendance = []

        dates = []
        # for i in a:

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter().values_list().distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
                'date','period').distinct()
            total=ttlAtt*6
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d=str(percentage)


                l.append({
                    'name' : i.student_name,
                    'cnt': tcnt,
                    'total':int(total),
                    'percentage': d[:4]+" %",
                })

        return render(request, "staff/hod_attendance_total.html", {'data':l})
    else:
        students = Student.objects.filter(DEPARTMENT_id=f)
        l = []
        attendance = []

        dates = []
        # for i in a:

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter().values_list().distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
                'date', 'period').distinct()
            total = ttlAtt * 6
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)

                l.append({
                    'name': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4]+" %",
                })

        return render(request, "staff/hod_attendance_total.html", {'data': l})





def staff_attendance_total(request):
    f = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    a = Attendance.objects.all()
    students = Student.objects.filter(DEPARTMENT_id=f)
    l = []
    attendance = []

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter().values_list().distinct().count()
        s=Attendance.objects.all()

        k=[]

        for m in s:

            if m.date not in k:
                k.append(m.date)

        total=len(k)*6
        att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
            'date', 'period').distinct()
        # total = ttlAtt * 6
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt / total) * 100
            d = str(percentage)

            l.append({
                'name': i.student_name,
                'cnt': tcnt,
                'total': int(total),
                'percentage': d[:4] + " %",
            })

    return render(request, "staff/staff_attendance_total.html", {'data': l})


def staff_attendance_total_post(request):
    name = request.POST['name']
    f = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
    a = Attendance.objects.all()
    if name:
        students = Student.objects.filter(DEPARTMENT_id=f, student_name__icontains=name)
        l = []
        attendance = []

        dates = []
        # for i in a:

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter().values_list().distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
                'date', 'period').distinct()
            total = ttlAtt * 6
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)

                l.append({
                    'name': i.student_name,
                    'cnt': tcnt,
                    'total': total,
                    'percentage': d[:4] + " %",
                })

        return render(request, "staff/staff_attendance_total.html", {'data': l})
    else:
        students = Student.objects.filter(DEPARTMENT_id=f)
        l = []
        attendance = []

        dates = []
        # for i in a:

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter().values_list().distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
                'date', 'period').distinct()
            total = ttlAtt * 6
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)

                l.append({
                    'name': i.student_name,
                    'cnt': tcnt,
                    'total': int(total),
                    'percentage': d[:4] + " %",
                })

        return render(request, "staff/staff_attendance_total.html", {'data': l})


#####################################################################################################################
#######################################################ANDROID##########################################################

def user_loginpost(request):
    username = request.POST['username']
    password = request.POST['password']
    cls = Login.objects.filter(username=username, password=password)
    if cls.exists():
        clss = Login.objects.get(username=username, password=password)

        if clss.username != username or clss.password != password:
            return JsonResponse({'status':'no'})

        if clss.type == 'student':
            lid=clss.id
            return JsonResponse({'status':'ok','lid':str(lid),'type':clss.type})
        elif clss.type == 'parent':
            lid=clss.id
            return JsonResponse({'status':'ok','lid':str(lid),'type':clss.type})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status':'no'})









def parent_viewprofile(request):
    lid=request.POST['lid']
    dd = Login.objects.get(id=lid).username
    res=Student.objects.get(student_email=dd)
    resa = Student.objects.get(student_email=dd).id
    date = datetime.now().date()
    latest_attendance = Attendance.objects.filter(STUDENT_id=resa, date=date)

    print(latest_attendance, latest_attendance.count(), "hellllllloooo")

    if latest_attendance.count() > 0:
        print("yes")

        latest_attendance = latest_attendance[len(latest_attendance) - 1]
        a = {
            'student_name': res.student_name,
            'student_photo': res.student_photo,
            'student_email': res.student_email,
            'student_phone': res.student_phone,
            'sem': res.sem,
            'gender': res.gender,
            'student_house': res.student_house,
            'student_location': res.student_location,
            'student_pincode': res.student_pincode,
            'student_dob': res.student_dob,
            'course': res.COURSE.course_name,
            'parent_name': res.parent_name,
            'department': res.DEPARTMENT.dept_name,
            'time': latest_attendance.hour,

        }
        return JsonResponse({'status': 'ok', 'student_name': res.student_name,
                             'student_photo': res.student_photo,
                             'student_email': res.student_email,
                             'student_phone': res.student_phone,
                             'sem': res.sem,
                             'gender': res.gender,
                             'student_house': res.student_house,
                             'student_location': res.student_location,
                             'student_pincode': res.student_pincode,
                             'student_dob': res.student_dob,
                             'course': res.COURSE.course_name,
                             'parent_name': res.parent_name,
                             'department': res.DEPARTMENT.dept_name, 'time': latest_attendance.hour})
    else:
        a = {
            'student_name': res.student_name,
            'student_photo': res.student_photo,
            'student_email': res.student_email,
            'student_phone': res.student_phone,
            'sem': res.sem,
            'gender': res.gender,
            'student_house': res.student_house,
            'student_location': res.student_location,
            'student_pincode': res.student_pincode,
            'student_dob': res.student_dob,
            'course': res.COURSE.course_name,
            'parent_name': res.parent_name,
            'department': res.DEPARTMENT.dept_name,
            'time': "-/-",
        }
        return JsonResponse({'status': 'ok', 'student_name': res.student_name,
                             'student_photo': res.student_photo,
                             'student_email': res.student_email,
                             'student_phone': res.student_phone,
                             'sem': res.sem,
                             'gender': res.gender,
                             'student_house': res.student_house,
                             'student_location': res.student_location,
                             'student_pincode': res.student_pincode,
                             'student_dob': res.student_dob,
                             'course': res.COURSE.course_name,
                             'parent_name': res.parent_name,
                             'department': res.DEPARTMENT.dept_name, 'time': "-/-"})


def user_viewprofile(request):
    lid=request.POST['lid']
    res=Student.objects.get(LOGIN_id=lid)
    sid=Student.objects.get(LOGIN_id=lid).id
    date=datetime.now().date()
    latest_attendance = Attendance.objects.filter(STUDENT_id=sid, date=date)



    print(latest_attendance,latest_attendance.count(),"hellllllloooo")

    if latest_attendance.count()>0:

        print("yes")

        latest_attendance=latest_attendance[len(latest_attendance)-1]

        a={
            'student_name':res.student_name,
            'student_photo':res.student_photo,
            'student_email':res.student_email,
            'student_phone':res.student_phone,
            'sem':res.sem,
            'gender':res.gender,
            'student_house':res.student_house,
            'student_location':res.student_location,
            'student_pincode':res.student_pincode,
            'student_dob':res.student_dob,
            'course':res.COURSE.course_name,
            'parent_name':res.parent_name,
            'department':res.DEPARTMENT.dept_name,
            'time':latest_attendance.hour,
            'subject': latest_attendance.SUBJECT.subject_name
           }
        return JsonResponse({'status':'ok','student_name':res.student_name,
            'student_photo':res.student_photo,
            'student_email':res.student_email,
            'student_phone':res.student_phone,
            'sem':res.sem,
            'gender':res.gender,
            'student_house':res.student_house,
            'student_location':res.student_location,
            'student_pincode':res.student_pincode,
            'student_dob':res.student_dob,
            'course':res.COURSE.course_name,
            'parent_name':res.parent_name,
            'department':res.DEPARTMENT.dept_name,'time':latest_attendance.hour,
            'subject': latest_attendance.SUBJECT.subject_name})
    else:
        a = {
            'student_name': res.student_name,
            'student_photo': res.student_photo,
            'student_email': res.student_email,
            'student_phone': res.student_phone,
            'sem': res.sem,
            'gender': res.gender,
            'student_house': res.student_house,
            'student_location': res.student_location,
            'student_pincode': res.student_pincode,
            'student_dob': res.student_dob,
            'course': res.COURSE.course_name,
            'parent_name': res.parent_name,
            'department': res.DEPARTMENT.dept_name,
            'time': "-/-",
            'subject':"-/-"
        }
        return JsonResponse({'status': 'ok', 'student_name': res.student_name,
                             'student_photo': res.student_photo,
                             'student_email': res.student_email,
                             'student_phone': res.student_phone,
                             'sem': res.sem,
                             'gender': res.gender,
                             'student_house': res.student_house,
                             'student_location': res.student_location,
                             'student_pincode': res.student_pincode,
                             'student_dob': res.student_dob,
                             'course': res.COURSE.course_name,
                             'parent_name': res.parent_name,
                             'department': res.DEPARTMENT.dept_name,'time': "-/-",'subject':"-/-" })


def user_change_password(request):
    lid = request.POST['lid']
    old_password = request.POST['old']
    new_password = request.POST['newp']
    c_password = request.POST['cp']
    res=Login.objects.filter(id=lid,password=old_password)
    if res.exists():
        res=Login.objects.get(id=lid,password=old_password)
        res.password=new_password
        res.save()
        return JsonResponse({'status': 'ok'})

    else:
        return JsonResponse({'status':'no'})



def staff_view(request):
    lid = request.POST['lid']
    dept = Student.objects.get(LOGIN_id=lid).DEPARTMENT_id
    s = Staff.objects.filter(DEPARTMENT_id=dept)
    l=[]
    for i in s:
        l.append({"staff_id":i.id,'staff_name':i.staff_name})
        print(l)
    return JsonResponse({'status':'ok','data':l})




def leave_request(request):
    lid = request.POST['lid']
    s=Student.objects.get(LOGIN_id=lid).id
    sdate=str(request.POST['sdate']).split(' ')[0]
    edate=str(request.POST['edate']).split(' ')[0]
    desc=request.POST['desc']
    staff=request.POST['staffname']

    a=Leave()
    a.STUDENT_id=s
    a.desc=desc
    a.start_date=sdate
    a.end_date=edate
    a.STAFF_id=staff
    a.status='Pending'
    a.save()

    return JsonResponse({'status':'ok'})




def leave_history(request):
    lid = request.POST['lid']
    s = Student.objects.get(LOGIN_id=lid).id
    l=Leave.objects.filter(STUDENT_id=s)
    a=[]
    for i in l:
        a.append({'id':i.id,'desc':i.desc,'sdate':i.start_date,'edate':i.end_date,'msg':i.status})
    return JsonResponse({'status':'ok','data':a})




def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.desc=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    print(toid,'jhbjhj')
    print(fromid)




    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid))
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.desc+"\n"+i.date.strftime("%Y-%m-%d"), "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})





def view_staff_chat(request):
    lid = request.POST['lid']
    dd=Login.objects.get(id=lid).username
    bb=Student.objects.get(student_email=dd).DEPARTMENT.id
    b =Staff.objects.filter(DEPARTMENT=bb)
    l = []
    for i in b:
        l.append({"staff_id":i.LOGIN.id,'staff_name':i.staff_name,"staff_photo":i.staff_photo})
    return JsonResponse({'status':'ok', 'data':l})






def forget_password(request):
    em = request.POST['username']
    import random
    log = Login.objects.filter(username=em)
    print(em)
    if log.exists():
        for i in log:
            print(i.type)
            if i.type == 'parent':
                print('hello')
                new_pass = random.randint(00000000, 99999999)
                logg = Login.objects.get(username=em,type='parent')
                message = 'temporary parent password is ' + str(new_pass)
                send_mail(
                'temp password',
                message,
                settings.EMAIL_HOST_USER,
                [em, ],
                fail_silently=False
                )
                loggg=Login.objects.filter(username=em,type='parent').update(password = new_pass)
                print(new_pass)
                # logg.password = new_pass
                # logg.save()
                return JsonResponse({'status':'ok'})
            elif i.type == 'student':
                new_pass = random.randint(00000000, 99999999)
                logg = Login.objects.get(username=em,type='student')
                print("hiiiiiiiiiiiiii")
                message = 'temporary password is ' + str(new_pass)
                send_mail(
                    'temp password',
                    message,
                    settings.EMAIL_HOST_USER,
                    [em, ],
                    fail_silently=False
                )
                loggg=Login.objects.filter(username=em,type='student').update(password = new_pass)
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})





# def staff_view_attendance(request):
#     f = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
#     a=Attendance.objects.filter(STUDENT__DEPARTMENT_id=f)
#     return render(request, "staff/student_attendance.html",{'data':a})


# def student_view_attendance(request):
#     lid = request.POST['lid']
#     s=Student.objects.get(LOGIN_id=lid)
#     a=Attendance.objects.filter(STUDENT_id=s)
#     t=[]
#     for i in a:
#         t.append({'id':i.id,'date':i.date,'time':i.hour,'msg':i.status})
#     return JsonResponse({'status':'ok','data':t})



def student_view_attendance(request):
    lid=request.POST['lid']

    date=request.POST['date']
    res=Student.objects.filter(LOGIN_id=lid)

    ls=[]
    for i in res:

        m=[]
        m.append(i.student_name)
        h = ["1", "2", "3", "4", "5", "6"]
        for  k in h:

            d=Attendance.objects.filter(STUDENT=i, period=k, date=date)
            if d.exists():
                print(datetime,"Helllo",k)
                m.append(1)
            else:
                print(datetime, "hi",k)
                m.append(0)

        ls.append(m)



    print(ls)
    return JsonResponse({'status':'ok','data':ls})





def student_attendance_month(request):
    lid=request.POST['lid']
    month=request.POST['month']
    a = Attendance.objects.all()
    students = Student.objects.filter(LOGIN_id=lid)
    l = []
    attendance = []

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter(date__month=month).values_list('date').distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
            'date','period').distinct()
        total=ttlAtt*6
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt / total) * 100
            d=str(percentage)
            l.append({
                'cnt': tcnt,
                'percentage': d[:5],
            })

    return JsonResponse({'status':'ok','month':month,'data':l})






def student_attendance_total(request):
    lid=request.POST['lid']
    a = Attendance.objects.all()
    students = Student.objects.filter(LOGIN_id=lid)
    l = []
    attendance = []

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter().values_list().distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
            'date','period').distinct()
        total=ttlAtt*6
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt / total) * 100
            d=str(percentage)


            l.append({
                # 'cnt': tcnt,
                'percentage': d[:5],
            })

    return JsonResponse({'status':'ok','data':l})






def student_attendance_subject(request):
    lid = request.POST['lid']

    sa=Student.objects.get(LOGIN_id=lid)
    subject =  Subject.objects.filter(COURSE_id=sa.COURSE_id, sem=sa.sem)

    l=[]

    for i in subject:
        m=[]

        att= Attendance.objects.filter(SUBJECT=i)

        for ii in att:

            aa=str(ii.period)+ str(ii.date)

            if aa not in m:

                m.append(aa)

        print(m)
        s= Attendance.objects.filter(STUDENT=sa, SUBJECT=i)

        ss=0
        try:
            ss=float(len(s)) / float(len(m))
        except:
            ss=0


        l.append({
            'subject': i.subject_name, 'present': len(s),'total': len(m),'percentage': ss*100
        })

    return  JsonResponse(

        {
            'status':'ok',
            'data':l
        }
    )








def parent_view_attendance(request):
    lid=request.POST['lid']
    dd = Login.objects.get(id=lid).username
    bb = Student.objects.get(student_email=dd).id
    date=request.POST['date']
    res=Student.objects.filter(id=bb)

    ls=[]
    for i in res:

        m=[]
        m.append(i.student_name)
        h = ["1", "2", "3", "4", "5", "6"]
        for  k in h:

            d=Attendance.objects.filter(STUDENT=i, period=k, date=date)
            if d.exists():
                print(datetime,"Helllo",k)
                m.append(1)
            else:
                print(datetime, "hi",k)
                m.append(0)

        ls.append(m)



    print(ls)
    return JsonResponse({'status':'ok','data':ls})










def parent_attendance_month(request):
    lid=request.POST['lid']
    dd = Login.objects.get(id=lid).username
    bb = Student.objects.get(student_email=dd).id
    month=request.POST['month']
    a = Attendance.objects.all()
    students = Student.objects.filter(id=bb)
    l = []
    attendance = []

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter(date__month=month).values_list('date').distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id, date__month=month).values_list(
            'date','period').distinct()
        total=ttlAtt*6
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt / total) * 100
            d=str(percentage)
            l.append({
                'cnt': tcnt,
                'percentage': d[:5],
            })

    return JsonResponse({'status':'ok','month':month,'data':l})






def parent_attendance_total(request):
    lid=request.POST['lid']
    dd = Login.objects.get(id=lid).username
    bb = Student.objects.get(student_email=dd).id
    a = Attendance.objects.all()
    students = Student.objects.filter(id=bb)
    l = []
    attendance = []

    dates = []
    # for i in a:

    for i in students:
        if i.id in attendance:
            continue
        attendance.append(i.id)
        ttlAtt = Attendance.objects.filter().values_list().distinct().count()
        att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
            'date','period').distinct()
        total=ttlAtt*6
        if att.exists():
            tcnt = att.count()
            att = att[0]

            percentage = (tcnt / total) * 100
            d=str(percentage)


            l.append({
                # 'cnt': tcnt,
                'percentage': d[:5],
            })

    return JsonResponse({'status':'ok','data':l})






def parent_attendance_subject(request):
    lid = request.POST['lid']
    dd = Login.objects.get(id=lid).username
    bb = Student.objects.get(student_email=dd).id
    sa=Student.objects.get(id=bb)
    subject =  Subject.objects.filter(COURSE_id=sa.COURSE_id, sem=sa.sem)

    l=[]

    for i in subject:
        m=[]

        att= Attendance.objects.filter(SUBJECT=i)

        for ii in att:

            aa=str(ii.period)+ str(ii.date)

            if aa not in m:

                m.append(aa)

        print(m)
        s= Attendance.objects.filter(STUDENT=sa, SUBJECT=i)

        ss=0
        try:
            ss=float(len(s)) / float(len(m))
        except:
            ss=0


        l.append({
            'subject': i.subject_name, 'present': len(s),'total': len(m),'percentage': ss*100
        })

    return  JsonResponse(

        {
            'status':'ok',
            'data':l
        }
    )








def parent_view_attendance(request):
    lid=request.POST['lid']
    dd = Login.objects.get(id=lid).username
    bb = Student.objects.get(student_email=dd).id
    date=request.POST['date']
    res=Student.objects.filter(id=bb)

    ls=[]
    for i in res:

        m=[]
        m.append(i.student_name)
        h = ["1", "2", "3", "4", "5", "6"]
        for  k in h:

            d=Attendance.objects.filter(STUDENT=i, period=k, date=date)
            if d.exists():
                print(datetime,"Helllo",k)
                m.append(1)
            else:
                print(datetime, "hi",k)
                m.append(0)

        ls.append(m)



    print(ls)
    return JsonResponse({'status':'ok','data':ls})















##########################################pdf generation########################################################


# Import necessary modules
from reportlab.lib.pagesizes import letter,A3
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from django.http import HttpResponse
# from .models import Volunteer
from io import BytesIO
# Define function to generate PDF with volunteer details


def generate_attendance(sa, kk):
    buffer = BytesIO()

    # Create a PDF canvas
    document = SimpleDocTemplate(buffer, pagesize=letter)
    # Define data for volunteer table header
    attendance_table_data = [kk[0]]
    department_name = sa[0].DEPARTMENT.dept_name
    sem = sa[0].sem

    # Iterate over each volunteer and add their details to the table
    for i in kk[1:]:
        attendance_table_data.append(i)

    # Create volunteer table
    table = Table(attendance_table_data, rowHeights=30)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subheading_style = styles['Heading3']

    heading_text = f"Subject-wise Attendance"
    department_subheading_text = f"Department: {department_name}"
    semester_subheading_text = f"Semester: {sem}"
    Pp = Paragraph(heading_text, title_style)
    department_subheading = Paragraph(department_subheading_text, subheading_style)
    semester_subheading = Paragraph(semester_subheading_text, subheading_style)

    elements = [Pp, department_subheading, semester_subheading]

    # Define table style
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add table to PDF
    elements.append(table)
    signature_text = "<br/><br/><br/><br/>HOD: _______________________<br/><br/><br/>Tutor: _______________________<br/>"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)
    document.build(elements)

    buffer.seek(0)
    return buffer


def generate_report(request):
    try:

        lid = request.session['lid']
        dep = Staff.objects.get(LOGIN_id=lid).DEPARTMENT.id
        sa = Student.objects.filter(DEPARTMENT_id=dep)
        if len(sa) < 1:
            return HttpResponse(
                '''<Script>alert("No students available");window.location="/myapp/hod_view_attendance/"</Script>''')
        subject = Subject.objects.filter(COURSE_id=sa[0].COURSE_id, sem=sa[0].sem)
        print(subject, "hello")
        fnl = []
        for i in subject:
            m = []
            l = []
            att = Attendance.objects.filter(SUBJECT=i)
            for ii in att:
                aa = str(ii.period) + str(ii.date)
                if aa not in m:
                    m.append(aa)

            l.append(i.subject_name)

            for j in sa:
                s = Attendance.objects.filter(STUDENT=j, SUBJECT=i)
                count = 0
                ss = 0
                try:
                    ss = float(len(s)) / float(len(m))
                except:
                    ss = 0
                ss = ss * 100
                sss = str(ss)

                l.append(
                    sss + " %"
                )
            fnl.append(l)

        print(fnl)

        fnl = [list(i) for i in zip(*fnl)]

        j = -1
        kk = []
        for i in fnl:
            k = []
            if j == -1:
                k.append("")
                j = j + 1

            else:
                k.append(sa[j].student_name)
                j = j + 1
            for m in i:
                k.append(m)
            kk.append(k)


        buffer = generate_attendance(sa, kk)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = f"attendance_{datetime.now().date()}.pdf"
        file_path = fs.save('pdf/' + filename, buffer)

        # Prepare the HTTP response containing the generated PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="attendance.pdf"'
        response.write(buffer.getvalue())

        return response
    except Attendance.DoesNotExist:
        return HttpResponse("Attendance does not exist")







def generate_report_month(request):
    try:
        current_month = datetime.now().strftime("%B %Y")  # Get the current month name
        a = Attendance.objects.all()
        ff=Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        students = Student.objects.filter(DEPARTMENT_id=ff)
        sem = students[0].sem
        dept=Department.objects.get(id=ff).dept_name

        l = []
        attendance = []

        dates = []

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter(date__month=datetime.now().month).values_list(
                'date').distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id, date__month=datetime.now().month).values_list(
                'date',
                'period').distinct()
            total = (ttlAtt*6)
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)
                l.append({
                    'Std': i.student_name,
                    'cnt': tcnt,
                    'total':int(total),
                    'percentage': d[:4] + " %",
                })

        buffer = generate_attendance_month(l, current_month,dept,sem)  # Pass current month to generate_attendance_month

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = f"attendance_{datetime.now().date()}.pdf"
        file_path = fs.save('pdf/' + filename, buffer)

        # Prepare the HTTP response containing the generated PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="attendance.pdf"'
        response.write(buffer.getvalue())

        return response
    except Attendance.DoesNotExist:
        return HttpResponse("Attendance does not exist")


def generate_attendance_month(l, month,dept,sem):  # Modified to accept month as argument
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter)
    attendance_table_data = [["Student Name", "Total Present", "Percentage"]]

    for i in l:
        attendance_table_data.append(
            [i['Std'], f"{i['cnt']}/{i['total']}", i['percentage']]
        )

    table = Table(attendance_table_data, rowHeights=30)
    styles = getSampleStyleSheet()
    title_style = styles['Title']

    heading_text = f"Attendance of {month}"

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    subheading_style = styles['Heading3']
    department_subheading_text = f"Department: {dept}"
    semester_subheading_text = f"Semester: {sem}"

    department_subheading = Paragraph(department_subheading_text, subheading_style)
    semester_subheading = Paragraph(semester_subheading_text, subheading_style)
    Pp = Paragraph(heading_text, title_style)
    elements = [Pp, department_subheading, semester_subheading]
    #
    # Pp = Paragraph(heading_text, title_style)
    # elements = [Pp]

    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black), ]))

    elements.append(table)
    signature_text = "<br/><br/><br/><br/>HOD: _______________________<br/><br/><br/>Tutor: _______________________<br/>"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)

    document.build(elements)

    buffer.seek(0)
    return buffer






def generate_report_total(request):
    try:
        f = Staff.objects.get(LOGIN_id=request.session['lid']).DEPARTMENT_id
        a = Attendance.objects.all()
        students = Student.objects.filter(DEPARTMENT_id=f)
        dep=students[0].DEPARTMENT_id
        dept=Department.objects.get(id=dep).dept_name
        sem=students[0].sem
        l = []
        attendance = []

        dates = []
        # for i in a:

        for i in students:
            if i.id in attendance:
                continue
            attendance.append(i.id)
            ttlAtt = Attendance.objects.filter().values_list().distinct().count()
            att = Attendance.objects.filter(STUDENT_id=i.id).values_list(
                'date', 'period').distinct()
            total = ttlAtt * 6
            if att.exists():
                tcnt = att.count()
                att = att[0]

                percentage = (tcnt / total) * 100
                d = str(percentage)

                l.append({
                    'name': i.student_name,
                    'cnt': tcnt,
                    'total': total,
                    'percentage': d[:4] + " %",
                })

        buffer = generate_attendance_total(l,dept,sem)  # Pass current month to generate_attendance_month

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="bill.pdf"'
        response.write(buffer.getvalue())

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = f"attendance_{datetime.now().date()}.pdf"
        file_path = fs.save('pdf/' + filename, buffer)

        # Prepare the HTTP response containing the generated PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="attendance.pdf"'
        response.write(buffer.getvalue())

        return response
    except Attendance.DoesNotExist:
        return HttpResponse("Attendance does not exist")






def generate_attendance_total(l,dept,sem):  # Modified to accept month as argument
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter)
    attendance_table_data = [["Student Name", "Total Present", "Percentage"]]

    for i in l:
        attendance_table_data.append(
            [i['name'], f"{i['cnt']}/{i['total']}", i['percentage']]
        )

    table = Table(attendance_table_data, rowHeights=30)
    styles = getSampleStyleSheet()
    title_style = styles['Title']

    heading_text = f"Total Attendance"  # Include month in the heading
    subheading_style = styles['Heading3']
    department_subheading_text = f"Department: {dept}"
    semester_subheading_text = f"Semester: {sem}"

    department_subheading = Paragraph(department_subheading_text, subheading_style)
    semester_subheading = Paragraph(semester_subheading_text, subheading_style)
    Pp = Paragraph(heading_text, title_style)
    elements = [Pp, department_subheading, semester_subheading]


    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black), ]))

    elements.append(table)

    signature_text = "<br/><br/><br/><br/>HOD: _______________________<br/><br/><br/>Tutor: _______________________<br/>"
    signature_paragraph = Paragraph(signature_text, styles['Normal'])
    elements.append(signature_paragraph)

    document.build(elements)

    buffer.seek(0)
    return buffer












        #######################################################################################################################