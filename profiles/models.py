from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import F
from django.db import transaction


class User(AbstractUser):
    is_teacher = models.BooleanField(default= False, null=True,blank=True)
    is_student = models.BooleanField(default= False, null=True,blank=True)
    is_support = models.BooleanField(default= False, null=True,blank=True)
    def __str__(self):
        return f'{self.username}'

class Level(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    years=(('2023','2023'),('2024','2024'),('2025','2025'),('2026','2026'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    admission_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    year_of_admission = models.CharField(max_length=255, choices = years)
    address = models.TextField(max_length=1000, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.full_name}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not self.admission_number:
            # Generate a unique admission number if not provided
            last_student = StudentProfile.objects.order_by('-id').first()
            last_enrollment_number = 0
            if last_student:
                # Safely parse the last admission number
                last_enrollment_number = int(last_student.admission_number.split('/')[-1])

            # Generate a new admission number
            self.admission_number = f"FSTC/{self.year_of_admission}/{last_enrollment_number + 1}"
        
        super(StudentProfile, self).save(*args, **kwargs)


# class StudentProfile(models.Model):
#     years=(('2023','2023'),('2024','2024'),('2025','2025'),('2026','2026'))

#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
#     admission_number = models.CharField(max_length = 255, null=True, blank=True)
#     full_name = models.CharField(max_length=255)
#     year_of_admission = models.CharField(max_length=255, choices = years)
#     address = models.TextField(max_length=1000)
#     level = models.ForeignKey(Level, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.full_name}"
    
#     def save(self, *args, **kwargs):
#         if not self.admission_number:
#             # Generate a unique enrollment number
#             last_student = StudentProfile.objects.order_by('-id').first()
#             if last_student:
#                 last_enrollment_number = int(last_student.admission_number.split(' ')[-1])
#             else:
#                 last_enrollment_number = 0
#             self.admission_number = f"FSTC/{self.year_of_admission}/{last_enrollment_number + 1}"
#         super(StudentProfile, self).save(*args, **kwargs)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tprofile', null=True)
    staff_number = models.CharField(max_length = 255, null=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField(max_length=1000)
    def __str__(self):
        return f"{self.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.staff_number:
            # Generate a unique enrollment number
            last_student = StudentProfile.objects.order_by('-id').first()
            if last_student:
                last_enrollment_number = int(last_student.staff_number.split(' ')[-1])
            else:
                last_enrollment_number = 0
            self.staff_number = f"FSTC/STAFF/{last_enrollment_number + 1}"
        super(StudentProfile, self).save(*args, **kwargs)

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='aprofile', null=True)
    full_name = models.CharField(max_length=255)
    address = models.TextField(max_length=1000)
    def __str__(self):
        return f"{self.full_name}"
