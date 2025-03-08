from django.urls import path
from . import views


app_name = 'profiles'

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('update-student/', views.update_student, name = 'update-student'),
    path('login/', views.Login, name = 'login'),
    path('logout/', views.Logout, name = 'logout'),
    path('admin-dashboard/', views.admin_dashboard, name = 'admin-dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name = 'teacher-dashboard'),
    path('student-dashboard/', views.student_dashboard, name = 'student-dashboard'),
    path('students/', views.students, name = 'students'),
    path('staffs/', views.staffs, name = 'staffs'),
    path('subjects/', views.subjects, name = 'subjects'),
    path('levels/', views.levels, name = 'levels'),
    path('profiles/', views.profiles, name = 'profiles')
]