from genericpath import exists
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import *

# Create your views here.
def home(request):
    f = request.GET.get('f') if request.GET.get('f') != None else ''
    school_names = Schools_Profiles.objects.all()
   
    schools = Schools_Profiles.objects.filter(school_name__icontains=f)
    context = {
        'school_names' : school_names,
        'schools' : schools,
    }
    return render(request, 'index.html', context)
     
@login_required(login_url='login')
def school_page(request, school_name):
    school = Schools_Name.objects.get(school_name=school_name)
    exist = Schools_Profiles.objects.filter(school_name=school_name).exists()
    student = Student.objects.filter(student=request.user, school=school).exists()
    pay = Student.objects.filter(student=request.user, pay=False, school=school).exists()
    
    if exist:
        sch_profile = Schools_Profiles.objects.get(school_name=school_name)
        page = School_page.objects.filter(school_Profiles=sch_profile).exists()
        if page:
            school_page = School_page.objects.get(school_Profiles=sch_profile)
            images = School_images.objects.filter(schools_profile=sch_profile).exists()
            if images:
                school_images = School_images.objects.filter(schools_profile=sch_profile)
            else:
                images = False
                school_images = False
        else:
            images = False
            school_page = False
            school_images = False
        context = {
            'images' : images,
            'pay' : pay,
            'student' : student,
            'exists' : exist,
            'school_page': school_page,
            'school_name':school_name,
            'school_images' : school_images,
            'page' : page,
        }
        return render(request, 'school_page.html', context)
    else:
        return redirect('home')



def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').upper()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or password does not exit')

    context = {
        'page' : page,
    }
    return render(request, 'login-register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def register(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.upper()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
            
    context = {
        'page' : page,
        'form' : form,
    }
    return render(request, 'login-register.html', context)

def admission(request, school_name):
    school = Schools_Name.objects.get(school_name=school_name)
    admission =  Student_admission.objects.filter(School_name = school).exists()
    if  admission:
        stud_admissions = Student_admission.objects.filter(School_name = school)
    else:
        stud_admissions = None
    context = {
        'admission' : admission,
        'school_name' : school_name,
        'stud_admissions' : stud_admissions,
    }
    return render(request, 'admission.html', context)

def admission_detail(request, school_name, student):
    user = User.objects.get(username = student)
    school = Schools_Name.objects.get(school_name=school_name)
    images = Student_admission_image.objects.filter(student = user, school_name=school).exists()
    if images:
        details = Student_admission_image.objects.filter(student = user, school_name=school)
        stud_admission = Student_admission.objects.get(stud_admis=user, School_name=school)
    else:
        details = None
        stud_admission = None
    context = {
        'details': details,
        'stud_admission' : stud_admission,
        'images' : images,
        'school_name' : school_name,
    }
    return render(request, 'admission_detail.html', context) 

def stud_admission(request, school_name, student):
    
    user = User.objects.get(username = student)
    school = Schools_Name.objects.get(school_name=school_name)
    send_admission = Student_admission.objects.filter(stud_admis = user, School_name=school).exists()
    images = Student_admission_image.objects.filter(student = user, school_name=school)
    details = False
    refuse = Refuse_Admission.objects.filter(student=user, school_name=school).exists()
    accep_in_school = Accepted_Admission.objects.filter(student=user, school_name=school).exists()
    accepted = Accepted_Admission.objects.filter(student=request.user).exists()
    if accepted:
        accepted_stud = Accepted_Admission.objects.get(student=request.user)
    else:
        accepted_stud=False
    
    if send_admission:
        stud_admission = Student_admission.objects.get(stud_admis=user, School_name=school)
        if images:
            details = Student_admission_image.objects.filter(student = user, school_name=school)
    else:
        stud_admission = False
    context = {
        'accepted_stud' : accepted_stud,
        'accep' : accep_in_school,
        'images' : images,
        'send_admission' : send_admission,
        'details' : details,
        'stud_admission' : stud_admission,
        'school_name' : school_name,
        'refuse' : refuse,
        'accepted' : accepted
    }
    return render(request, 'stud_admission.html', context)

def register_admission(request, school_name, student):
    if request.method == 'POST':
        username = request.POST.get('username').upper()
        school = request.POST.get('school')
        description = request.POST.get('description')
        stud_image = request.FILES['image']
        classe = request.POST.get('class')
        stud_admis = User.objects.get(username=username)
        School_name = Schools_Name.objects.get(school_name=school)
        if not Student_admission.objects.filter(stud_admis = stud_admis, School_name=School_name).exists():
            new_stud_admis = Student_admission.objects.create(stud_admis=stud_admis, description=description, stud_image=stud_image, School_name=School_name, student_class=classe)
            new_stud_admis.save()
            #/student admission/SAINT MATIN TECHNICAL COLLEGE/TCHINDA_LANDRI/
            path = '/student admission/'+school_name+'/'+student+'/'
            return redirect(path)
        else:
            return redirect('home')
    else:
        page = 'Register Admission'
        schools = Schools_Name.objects.get(school_name=school_name)
        classes = School_class.objects.filter(school_name=schools)
        context = {
            'classes' : classes,
            'school_name' : school_name,
            'student' : student,
            'page' : page,
        }
        return render(request, 'register_admission.html', context)

def add_admission(request, school_name, student):
    if request.method == 'POST':
        username = request.POST.get('username')
        school = request.POST.get('school')
        #title = request.POST.get('title')
        #image = request.FILES['image']
        stud_admin = User.objects.get(username=username)
        School_name = Schools_Name.objects.get(school_name=school)
        #new_admin_student = Student_admission_image.objects.create(student=stud_admin, school_name=School_name, title=title, image=image)
        nw_ads_img = Student_admission_image()
        nw_ads_img.student = stud_admin
        nw_ads_img.school_name = School_name
        nw_ads_img.title = request.POST.get('title')
        #if len(request.FILES) != 0:
        nw_ads_img.image = request.FILES['image']

        nw_ads_img.save()
        #/student admission/SAINT MATIN TECHNICAL COLLEGE/TCHINDA_LANDRI/
        path = '/student admission/'+school_name+'/'+student+'/'
        return redirect(path)
    else:
        page = 'Add Admission Picuture'
        context = {
            'school_name' : school_name,
            'page' : page,
            'student' : student,
        }
        return render(request, 'register_admission.html', context)

def accept_admission(request, pk):
    stud_admis = Student_admission.objects.get(id=pk)
    student = stud_admis.stud_admis
    school = stud_admis.School_name
    stud_images = Student_admission_image.objects.filter(student=student, school_name=school)
    stud_images.delete()
    classes = School_class.objects.get(school_name=school, classes=stud_admis.student_class)
    Accepted_admis = Accepted_Admission.objects.create(student=student, school_name=school)
    Accepted_admis.save()
    New_Student = Student()
    New_Student.student = student
    New_Student.student_image = stud_admis.stud_image
    New_Student.student_class = classes
    New_Student.school = school
    New_Student.pay = False
    #New_Student = Student.objects.create(student=student, school=school, student_class=classes, student_image=stud_admis.stud_image, pay=False)
    New_Student.save()
    studss = Student_admission.objects.filter(stud_admis=student)
    studss.delete()
    stud_admis.delete()
    path = '/admission/'+school.school_name+'/'
    return redirect(path)

def refuse_admission(request, pk):
    stud_admis = Student_admission.objects.get(id=pk)
    student = stud_admis.stud_admis
    school = stud_admis.School_name
    refuse_admis = Refuse_Admission.objects.create(student=student, school_name=school)
    stud_images = Student_admission_image.objects.filter(student=student, school_name=school)
    stud_images.delete()
    refuse_admis.save()
    stud_admis.delete()
    #/admission/SAINT%20MATIN%20TECHNICAL%20COLLEGE/
    path = '/admission/'+school.school_name+'/'
    return redirect(path)

def add_school_image(request, school):
    school = Schools_Profiles.objects.get(school_name=school)
    if request.method == 'POST':
        sch_img = School_images()
        sch_img.image_title = request.POST.get('image_title')
        sch_img.schools_profile = school
        sch_img.school_image = request.FILES['image']
        sch_img.save()
        path = '/'+school.school_name+'/'
        return redirect(path)
    else:
        context = {
            'page' : 'Add School Image',
            'school_name' : school
        }
        return render(request, 'register_admission.html', context)

def delete_school_picture(request, pk):
    sch_img = School_images.objects.get(id=pk)
    sch_img.delete()
    path = '/'+sch_img.schools_profile.school_name+'/'
    return redirect(path)

def school_classes(request, schoolname):
    school = Schools_Name.objects.get(school_name=schoolname)
    classes = School_class.objects.filter(school_name=school)
    context = {
        'schoolname' : schoolname,
        'classes' : classes
    }
    return render(request, 'student_classes.html', context)

def students(request, schoolname, classe):
    school = Schools_Name.objects.get(school_name=schoolname)
    classe = School_class.objects.get(school_name=school, classes=classe)
    Students = Student.objects.filter(student_class=classe)
    Any_pay = Student.objects.filter(student_class=classe, pay=True).exists()
    Any_not_pay = Student.objects.filter(student_class=classe, pay=False).exists()
    context = {
        'Students' : Students,
        'Any_pay' : Any_pay,
        'Any_not_pay' : Any_not_pay,
        'school_name' : schoolname,
    }
    return render(request, 'students.html', context)

def payment(request, schoolname):
    school = Schools_Name.objects.get(school_name=schoolname)
    if Student.objects.filter(student=request.user, school=school).exists():
        student = Student.objects.get(student=request.user, school=school)
        context = {
            'student' : student
        }
        return render(request, 'payment.html', context)
    else:
        path = '/'+schoolname+'/'
        return redirect(path)

