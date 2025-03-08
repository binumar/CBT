from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload-questions/', views.upload_questions_view, name='upload-questions'),
    path('bulk-upload/<int:exam_id>/<int:subject_id>/', views.bulk_upload, name='bulk-upload'),
    path('success/', views.success, name='success'),
    path('not-in-time/', views.not_in_time, name='not-in-time'),
    path('ui-test/', views.ui_test, name='ui_test'),
    path('add-exam', views.add_exam, name='add-exam'),
    # path('admin-profile/', views.admin_profile, name='admin-profile'),
    # path('teacher-profile/', views.teacher_profile, name='teacher-profile'),
    # path('student-profile/', views.student_profile, name='student-profile'),
    path('answer-sheet/', views.answer_sheet, name='answer-sheet'),
    path('finish/', views.finish, name='finish'),
    path('exam/', views.exam, name='exam'),

    path('add-exam/', views.add_exam, name='add-exam'),
    path('exams/', views.exams, name='exams'),

    path('add-question/', views.add_question, name='add-question'),
    path('update-question/<str:pk>/', views.update_question, name='update-question'),
    path('delete-question/<str:pk>/', views.delete_question, name='delete-question'),
    path('questions/', views.questions, name='questions'),

    path('add-answer/', views.add_answer, name='add-answer'),
    path('answers/', views.answers, name='answers'),

    path('results/', views.results, name='results'),
    path('exam-details/', views.exam_details, name='exam-details'),
    path('take_test/<int:exam_id>/', views.take_test, name='take_test'),
    path('result/<int:subject_id>/', views.view_result, name='result'),
    path('report/<int:subject_id>/', views.generate_report, name='generate_report'),
]
