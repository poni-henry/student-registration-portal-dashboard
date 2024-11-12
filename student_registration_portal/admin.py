from django.contrib import admin
from .models import Student
from django.contrib.auth.admin import UserAdmin
from .models import BankStatement

#Registereed models
admin.site.register(Student)
admin.site.register(BankStatement)