from django.forms import  ModelForm
from django import forms
from .models import Exam, Question, Answer
from django.contrib.auth.models import User

INPUT_CLASSES = 'w-full py-2 px-3 rounded-lg'

class ExamForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['end_time'].widget = forms.widgets.DateTimeInput(
    #         attrs={
    #             'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
    #             'class': 'form-control'
    #             }
    #         )
        
    class Meta:
        model = Exam
        fields = '__all__'
        widgets = {
            # CharField for title
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter exam title'
            }),
            
            # ForeignKey for subject (rendered as a dropdown)
            'subject': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            
            # ForeignKey for level (rendered as a dropdown)
            'level': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            
            # DateTimeField for start_time (rendered as datetime-local)
            'start_time': forms.DateTimeInput(attrs={
                'class': INPUT_CLASSES,
                'type': 'datetime-local'
            }),
            
            # DateTimeField for end_time (rendered as datetime-local)
            'end_time': forms.DateTimeInput(attrs={
                'class': INPUT_CLASSES,
                'type': 'datetime-local'
            }),
            
            # FloatField for duration (rendered as a number input)
            'duration': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter duration in hours'
            }),
            
            # BooleanField for is_active (rendered as a checkbox)
            'is_active': forms.CheckboxInput(attrs={
                'class': INPUT_CLASSES
            }),
            
            # BooleanField for completed (rendered as a checkbox)
            'completed': forms.CheckboxInput(attrs={
                'class': INPUT_CLASSES
            }),
            
            # IntegerField for number_of_questions (rendered as a number input)
            'number_of_questions': forms.NumberInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'Enter number of questions'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a default "Select" option to the subject field
        self.fields['subject'].empty_label = "Select Subject"
        self.fields['subject'].widget.attrs.update({'class': INPUT_CLASSES})
        
        # Add a default "Select" option to the level field
        self.fields['level'].empty_label = "Select Level"
        self.fields['level'].widget.attrs.update({'class': INPUT_CLASSES})

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            # ForeignKey for exam (rendered as a dropdown)
            'exam': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            # ForeignKey for subject (rendered as a dropdown)
            'subject': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            
            # CharField for title
            'marks': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'question weight'
            }),
                        # CharField for title
            'option1': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'question weight'
            }),
                        # CharField for title
            'option2': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'question weight'
            }),
                        # CharField for title
            'option3': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'question weight'
            }),
                        # CharField for title
            'option4': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'question weight'
            }),

            
            # ForeignKey for subject (rendered as a dropdown)
            'correct_answer': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a default "Select" option to the subject field
        self.fields['exam'].empty_label = "Select Exam"
        self.fields['exam'].widget.attrs.update({'class': INPUT_CLASSES})
        
        # Add a default "Select" option to the level field
        self.fields['subject'].empty_label = "Select Subject"
        self.fields['subject'].widget.attrs.update({'class': INPUT_CLASSES})

        # Add a default "Select" option to the level field
        self.fields['correct_answer'].empty_label = "Select correct answer"
        self.fields['correct_answer'].widget.attrs.update({'class': INPUT_CLASSES})

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'text', 'is_correct']
        

# class StudentRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'


class BulkUploadForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'subject', 'file']