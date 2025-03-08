from django.db import models
# from django.contrib.auth.models import User
from profiles.models import User, Level
from profiles.models import StudentProfile
from ckeditor.fields import RichTextField

class SchoolInfo(models.Model):
    name = models.CharField(max_length=255)
    logo = models.FileField(upload_to = 'images')

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# class Level(models.Model):
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     level = models.ForeignKey(Level, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     level = models.ForeignKey(Level, on_delete=models.CASCADE)
#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

class Exam(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE,null=True)
    duration = models.FloatField(null=True)
    is_active = models.BooleanField(default=False, null=True)
    completed = models.BooleanField(default=False, null=True)
    number_of_questions = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.title} ({self.subject.name})'

# class Question(models.Model):
#     exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     mark = models.FloatField(null=True)
#     text = models.TextField()

#     def __str__(self):
#         return f'{self.text}'

class Question(models.Model):
    exam=models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, null= True, on_delete=models.CASCADE)
    file = models.FileField(upload_to='questions', null=True,blank = True)
    marks=models.PositiveIntegerField()
    question = RichTextField(blank = True,null = True)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('a','a'),('b','b'),('c','c'),('d','d'))
    correct_answer=models.CharField(max_length=200,choices=cat)
    def __str__(self):
        return f'{self.question} {self.subject}'

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

# class StudentTest(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

#     score = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.student} - {self.subject}"
    
# class Attendance(models.Model):
#     user = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='profile', null=True )
#     sign_in = models.BooleanField(default=False)
#     sign_out = models.BooleanField(default=False)

class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='profile', null=True )
    # student = models.CharField(max_length=255, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f'{self.student} - {self.subject.name} - {self.score}'

class StudentAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=100)  # Store the answer choice
    is_correct = models.BooleanField(default=False)  # Indicate if the answer is correct
    correct_answer = models.CharField(max_length=100)  # Store the correct answer

    def __str__(self):
        return f"{self.student.full_name} - {self.exam} - {self.question.id}"
