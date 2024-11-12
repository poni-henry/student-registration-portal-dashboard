from django.contrib.auth.models import User
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    student_index_number = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=20)
    state = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    admission = models.CharField(max_length=20)
    date_of_birth = models.DateField(max_length=10)
    bank_statement = models.FileField(upload_to='bank_statement/', blank=True, null=True)
    status = models.CharField(max_length=100, default='Not Registered')

    def __str__(self):
        return self.student_name

class BankStatement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bank_statements')
    statement = models.FileField(upload_to='bank_statements/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
