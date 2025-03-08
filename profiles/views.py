from django.shortcuts import render, redirect
from  profiles.forms import RegisterationForm, StudentProfileForm
from .models import StudentProfile, TeacherProfile, AdminProfile, Level
from exams.models import Subject, Question, Answer, Result, Exam, SchoolInfo
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def students(request):
    students = StudentProfile.objects.all()
    context = {
        'students':students,
    }
    return render(request, 'data/students.html', context)

def staffs(request):
    staffs = TeacherProfile.objects.all()
    context = {
        'staffs':staffs,
    }
    return render(request, 'data/staffs.html', context)

def subjects(request):
    subjects = StudentProfile.objects.all()
    context = {
        'subjects':subjects,
    }
    return render(request, 'data/subjects.html', context)

def levels(request):
    levels = Level.objects.all()
    context = {
        'levels':levels,
    }
    return render(request, 'data/classes.html', context)


def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'dashboards/teacher_dashboard.html')

def student_dashboard(request):
    student = request.user.profile
    exam = Exam.objects.filter(level = student.level, completed = False)[0]
    context = {
        'student':student,
        'exam':exam
    }
    return render(request, 'dashboards/student_dashboard.html', context)

def Login(request):
    school_info = SchoolInfo.objects.all()[0]

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username =username, password = password)
        if user is not None and user.is_active:
            login(request,user)
            if request.user.is_support:
                return redirect('profiles:admin-dashboard')
            
            if request.user.is_teacher:
                return redirect('profiles:teacher-dashboard')
            
            if request.user.is_student:
                # return redirect('profiles:student-dashboard')
                return redirect('exams:exam')
        else:
            return redirect('profiles:signup')
    else:
        context = {
            'school_info':school_info
        }
        return render(request, 'accounts/login.html', context)
    

def Logout(request):
    logout(request)
    return redirect('profiles:login')

def signup(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            my_user = form.save(commit = False)
            my_user.is_student = True
            my_user.save()
            StudentProfile.objects.create(user = my_user, year_of_admission='2023')
            login(request,my_user)
            return redirect('profiles:update-student')
        else:
            return redirect('profiles:signup')
    else:
        form = RegisterationForm()
        context = {
            'form':form,
        }

    return render(request, 'accounts/signup.html', context)

def update_student(request):
    stdnt = StudentProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=stdnt)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'student {student.full_name} successifully updated')
            return redirect('profiles:student-dashboard')
    else:
        form = StudentProfileForm(instance=stdnt)

    context = {
        'form':form,
    }
    return render(request, 'accounts/profile.html', context)

def profiles(request):
    level = Level.objects.get(id = 1)
    # my_students = StudentProfile.objects.filter(level = level)
    my_students = StudentProfile.objects.all()
    
   
  
    context = {
        'my_students':my_students
    }
    return render(request, 'student_profiles.html', context)

