from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Student, BankStatement

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_name', 'registration_number', 'student_index_number',
            'contact_no', 'state', 'county', 'next_of_kin', 'next_of_kin_contact',
            'gender', 'admission', 'date_of_birth'
        ]

class BankStatementForm(forms.ModelForm):
    class Meta:
        model = BankStatement
        fields = ['statement']
