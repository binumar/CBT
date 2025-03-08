from django.contrib import admin
from .models import Subject, Question, Answer, Exam, Result, SchoolInfo

admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Exam)
admin.site.register(SchoolInfo)

