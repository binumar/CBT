from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Subject, Question, Answer, Result, Exam, SchoolInfo, StudentAnswer, StudentAnswer
from django.contrib.auth import authenticate, login, logout
from .forms import QuestionForm, ExamForm, AnswerForm
from django.contrib.auth.forms import UserCreationForm
from profiles.models import StudentProfile, Level
from django.contrib import messages

from .forms import BulkUploadForm

from django.utils import timezone
import csv
from django.http import HttpResponse

# def register(request):
#     return render(request, 'register.html')

# def Login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username =username, password = password)
#         if user is not None and user.is_active:
#             login(request,user)
#             if request.user.profile.is_admin:
#                 return redirect('admin-profile')
            
#             if request.user.profile.is_teacher:
#                 return redirect('teacher-profile')
            
#             if request.user.profile.is_student:
#                 return redirect('student-profile')
            
#         else:
#             return redirect('/account/signup/')
#     else:
#         return render(request, 'login.html')

# def admin_profile(request):
#     return render(request, 'profile/admin_profile.html')

# def teacher_profile(request):
#     return render(request, 'profile/teacher_profile.html')

# def profile(request):
#     return render(request, 'profile/profile.html')

def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, 'exam created successifully')
            return redirect('exams:exams')
    else:
        form = ExamForm()

    context = {
        'form':form,
    }
    return render(request, 'exam_form.html', context)

def exams(request):
    exams = Exam.objects.all()
    context = {
        'exams':exams,
    }
    return render(request, 'exams.html', context)

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'exam created successifully')
            return redirect('exams:questions')
    else:
        form = QuestionForm()

    context = {
        'form':form,
    }
    return render(request, 'question_form.html', context)

def update_question(request, pk):
    question = Question.objects.get(id = pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'exam updated successifully')
            return redirect('exams:questions')
    else:
        form = QuestionForm(instance = question)

    context = {
        'form':form,
    }
    return render(request, 'question_form.html', context)

def delete_question(request, pk):
    question = Question.objects.get(id = pk)
    question.delete()
    messages.success(request, 'exam deleted successifully')
    return redirect('exams:questions')


def questions(request):
    questions = Question.objects.all()
    context = {
        'questions':questions,
    }
    return render(request, 'questions.html', context)

def add_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save()
            messages.success(request, 'exam created successifully')
            return redirect('exams:answers')
    else:
        form = AnswerForm()

    context = {
        'form':form,
    }
    return render(request, 'answer_form.html', context)

def answers(request):
    answers = Answer.objects.all()
    context = {
        'answers':answers,
    }
    return render(request, 'answers.html', context)

def edit_exam(request):
    return render(request, 'add_exam.html')

def exam(request):
    student = request.user.profile
    try:
        # Attempt to get the first active and incomplete exam
        exam = Exam.objects.filter(is_active=True, completed=False).first()

        # If no exam is found, send a message to the user
        if exam is None:
            messages.info(request, 'There is no available exam at the moment.')
            return render(request, 'exam.html')  # Render the exam template without an exam

        # If exam is found, render exam.html with the context
        context = {
            'student':student,
            'exam': exam
        }
        return render(request, 'exam.html', context)

    except Exam.DoesNotExist:
        # In case of an exception, send a message to the user
        messages.error(request, 'An error occurred while fetching the exam.')
        return render(request, 'exam.html')  # Render the exam template without an exam


def exam_details(request):
    student = request.user.profile
    # exam = Exam.objects.filter(level = student.level, completed = False)[0]
    exam = Exam.objects.filter(is_active = True, completed = False)[0]
    print(exam.title)
    context = {
        'student':student,
        'exam':exam
    }
    return render(request, 'exam_details.html', context)

#original take_test
# @login_required
# def take_test(request, exam_id):
#     exam = get_object_or_404(Exam, id=exam_id)
#     # subject = get_object_or_404(Subject, id=subject_id)
#     subject = exam.subject
#     if timezone.now() < exam.start_time or timezone.now() > exam.end_time:
#         return render(request, 'not_in_time.html')
    
#     questions = Question.objects.filter(exam = exam, subject = exam.subject)
#     if request.method == 'POST':
#         total_score = 0
#         for q in range(len(questions)):
#             selected_answer = request.POST.get(str(q+1))
#             actual_answer = questions[q].correct_answer
#             if selected_answer:
#                 student_answer = selected_answer
#                 if student_answer == actual_answer:
#                     total_score += questions[q].marks
#             else:
#                 total_score += 0
#         Result.objects.create(student=request.user.profile, subject=subject, score=total_score)
#         # return redirect('exams:result', subject_id=subject.id)
#         # this can be linked to the result page
#         return redirect('exams:finish')
    
#     return render(request, 'take_test.html', {'subject': subject, 'questions': questions})

def take_test(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    subject = exam.subject
    current_time = timezone.now()
    
    # Prevent retaking the exam
    if Result.objects.filter(student=request.user.profile, subject=subject).exists():
        return render(request, 'already_taken.html')  # Display a message if already taken
    
    # Ensure the exam is being taken within the allowed time
    if current_time < exam.start_time or current_time > exam.end_time:
        return render(request, 'not_in_time.html')
    
    # Fetch questions for the exam
    questions = Question.objects.filter(exam=exam, subject=subject)
    
    if request.method == 'POST':
        total_score = 0

        # Iterate over questions and save answers
        for index, question in enumerate(questions, start=1):
            selected_answer = request.POST.get(str(index))
            if selected_answer:
                # Check if the answer is correct
                is_correct = selected_answer == question.correct_answer
                if is_correct:
                    total_score += question.marks

                ## Save student's answer with correctness info and correct answer if wrong
                # StudentAnswer.objects.create(
                #     student=request.user.profile,
                #     exam=exam,
                #     question=question,
                #     selected_answer=selected_answer,
                #     is_correct=is_correct,
                #     correct_answer=question.correct_answer if not is_correct else ""
                # )

        # Store the student's final score
        Result.objects.create(student=request.user.profile, subject=subject, score=total_score)
        
        # Redirect to the finish page
        return redirect(reverse('exams:finish'))
    
    return render(request, 'take_test.html', {'subject': subject, 'questions': questions})


def finish(request):
    logout(request)
    return render(request, 'finish.html')

@login_required
def view_result(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    # result = get_object_or_404(Result, student=request.user.profile, subject=subject)
    # for this one it should include the class for the filter
    result = Result.objects.filter(subject = subject)
    return render(request, 'result.html', {'result': result})

def answer_sheet(request):
    student = request.user.profile
    student_answers = StudentAnswer.objects.filter(student=student)
    
    return render(request, 'answer_sheet.html', {
        'student': student,
        'student_answers': student_answers,
    })

def student_answer_sheet(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = request.user.profile
    student_answers = StudentAnswer.objects.filter(student=student, exam=exam)
    
    # Fetch total score and max score for display
    result = Result.objects.filter(student=student, subject=exam.subject).first()
    total_score = result.score if result else 0
    max_score = sum(question.marks for question in exam.question_set.all())
    
    return render(request, 'answer_sheet.html', {
        'exam': exam,
        'subject': exam.subject,
        'student': student,
        'student_answers': student_answers,
        'total_score': total_score,
        'max_score': max_score,
    })


# @login_required
# def student_result(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id)
#     result = get_object_or_404(Result, student=request.user.profile, subject=subject)
#     return render(request, 'result.html', {'result': result})

@login_required
def results(request):
    # exams = Exam.objects.all()
    exams = Exam.objects.filter(is_active = True, completed = True)
    return render(request, 'results.html', {'exams': exams})

def home(request):
    return render(request, 'index.html')

def generate_report(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    results = Result.objects.filter(subject=subject)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{subject.name}_results.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name','Class', 'Score'])
    
    for result in results:
        writer.writerow([result.student, result.student.level.name, result.score])
    
    return response

#generate text document
# def generate_report(request, subject_id):
#     # Get the subject, or return a 404 if it doesn't exist
#     subject = get_object_or_404(Subject, id=subject_id)
    
#     # Query for all results associated with this subject
#     results = Result.objects.filter(subject=subject)
    
#     # Handle the case where there are no results
#     if not results.exists():
#         return HttpResponse("No results available for this subject.", content_type="text/plain")
    
#     # Prepare the response as plain text
#     response = HttpResponse(content_type='text/plain')
#     response['Content-Disposition'] = f'attachment; filename="{subject.name}_results.txt"'
    
#     # Write the header (column names) to the text file
#     response.write("Admission Number | Name | Class | Score\n")
#     response.write("-" * 50 + "\n")  # Adds a separator line
    
#     # Write each result to the text file
#     for result in results:
#         response.write(f"{result.student.admission_number} | "
#                         f"{result.student} | "
#                         f"{result.student.level.name} | "
#                         f"{result.score}\n")
    
#     # Return the response with the plain text file
#     return response




def ui_test(request):
    return render(request, 'ui_test.html')

def not_in_time(request):
    return render(request, 'not_in_time.html')

# def bulk_upload(request):
#     form = BulkUploadForm()
#     context = {
#         'form':form,
#     }
#     return render(request, 'bulk_upload_questions.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Exam, Subject, Question

def bulk_upload(request, exam_id, subject_id):
    exam = get_object_or_404(Exam, id=exam_id)
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        questions = []
        invalid_lines = []  # Track invalid lines for feedback

        # Process the CSV file line by line
        try:
            for line_num, line in enumerate(file.readlines(), start=1):
                line = line.decode('utf-8').strip()  # Decode bytes and remove newline characters
                parts = [part.strip() for part in line.split(',')]  # Trim spaces

                if len(parts) < 7:
                    invalid_lines.append(f"Line {line_num}: Missing data (skipped)")
                    continue

                question_text = parts[0]
                option1 = parts[1]
                option2 = parts[2]
                option3 = parts[3]
                option4 = parts[4]
                correct_answer = parts[5]

                try:
                    marks = int(parts[6])
                except ValueError:
                    invalid_lines.append(f"Line {line_num}: Invalid marks value (skipped)")
                    continue

                if not all([question_text, option1, option2, option3, option4, correct_answer]):
                    invalid_lines.append(f"Line {line_num}: Missing one or more fields (skipped)")
                    continue

                # Create a Question instance and append it to the list
                questions.append(Question(
                    exam=exam,
                    subject=subject,
                    marks=marks,
                    question=question_text,
                    option1=option1,
                    option2=option2,
                    option3=option3,
                    option4=option4,
                    correct_answer=correct_answer
                ))

            # Bulk create questions in the database
            if questions:
                Question.objects.bulk_create(questions)
                messages.success(request, f"Successfully uploaded {len(questions)} questions.")
            else:
                messages.warning(request, "No valid questions were uploaded.")

            # Report invalid lines
            if invalid_lines:
                messages.error(request, "\n".join(invalid_lines))

            return redirect('success')  # Redirect to a success page after upload

        except Exception as e:
            messages.error(request, f"An error occurred while processing the file: {str(e)}")
            return redirect('exams:bulk-upload', exam_id=exam_id, subject_id=subject_id)  # Redirect to retry

    return render(request, 'bulk_upload.html', {'exam_id': exam_id, 'subject_id': subject_id})

# def bulk_upload(request, exam_id, subject_id):
#     exam = get_object_or_404(Exam, id=exam_id)
#     subject = get_object_or_404(Subject, id=subject_id)
#     print(f'{exam} {subject}')
#     if request.method == 'POST':
#         print('hello1')
#         form = BulkUploadForm(request.POST, request.FILES)
#         if form.is_valid():
            
#             file = form.cleaned_data['file']
#             questions = []

#             # Process the text file line by line
#             for line in file:
#                 line = line.decode('utf-8').strip()  # Decode and remove newline characters
#                 parts = line.split(',')

#                 if len(parts) < 7:
#                     continue  # Skip incomplete lines

#                 # Assuming you want a default exam and subject for each question or need to fetch these from the database
#                 exam = Exam.objects.get(id = exam)  # Replace with actual exam retrieval logic
#                 subject = Subject.objects.get(subject)  # Replace with actual subject retrieval logic
                
#                 # Map file parts to fields
#                 question_text = parts[0]
#                 option1 = parts[1]
#                 option2 = parts[2]
#                 option3 = parts[3]
#                 option4 = parts[4]
#                 correct_answer = parts[5]
#                 marks = int(parts[6])

#                 # Create a Question instance without saving it
#                 questions.append(Question(
#                     exam=exam,
#                     subject=subject,
#                     marks=marks,
#                     question=question_text,
#                     option1=option1,
#                     option2=option2,
#                     option3=option3,
#                     option4=option4,
#                     correct_answer=correct_answer
#                 ))

#             # Bulk create all question instances
#             Question.objects.bulk_create(questions)
#             return redirect('success')  # Redirect to a success page or wherever you'd like
#         else:
#             print(form.errors)

#     else:
        
#         form = BulkUploadForm()
#     return render(request, 'bulk_upload.html', {'form': form})


def upload_questions_view(request):
    exams = Exam.objects.all()
    subjects = Subject.objects.all()

    context = {
        'exams': exams,
        'subjects': subjects,
    }
    return render(request, 'question_grade_levels.html', context)

def success(request):
    return render(request, 'success.html')


