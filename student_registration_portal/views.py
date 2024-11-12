from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from .forms import SignUpForm, StudentRegistrationForm, BankStatementForm
from .models import Student, BankStatement
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak



def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            error_message = 'Invalid username or password'
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    return render(request, 'base.html')

@login_required
def enroll(request):
    if request.method == 'POST':
        request.session['department'] = request.POST.get('department', '___________________')
        request.session['program'] = request.POST.get('program', '___________________')
        request.session['year_of_study'] = request.POST.get('year_of_study', '___________________')
        request.session['semester'] = request.POST.get('semester', '___________________')

        context = {
            'department': request.session['department'],
            'program': request.session['program'],
            'year_of_study': request.session['year_of_study'],
            'semester': request.session['semester'],
            'username': request.user.username
        }
        return render(request, 'dashboard.html', context)
    else:
        context = {
            'department': request.session.get('department', ''),
            'program': request.session.get('program', ''),
            'year_of_study': request.session.get('year_of_study', ''),
            'semester': request.session.get('semester', ''),
            'username': request.user.username
        }
        return render(request, 'dashboard.html', context)


@login_required
def register_page(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()

            # Store form data in session (optional)
            request.session['department'] = request.POST.get('department')
            request.session['program'] = request.POST.get('program')
            request.session['year_of_study'] = request.POST.get('year_of_study')
            request.session['semester'] = request.POST.get('semester')
            request.session['student_name'] = student.student_name
            request.session['registration_number'] = student.registration_number
            request.session['student_index_number'] = student.student_index_number
            request.session['contact_no'] = student.contact_no
            request.session['state'] = student.state
            request.session['county'] = student.county
            request.session['next_of_kin'] = student.next_of_kin
            request.session['next_of_kin_contact'] = student.next_of_kin_contact
            request.session['gender'] = student.gender
            request.session['admission'] = student.admission
            request.session['date_of_birth'] = str(student.date_of_birth)

            return redirect('dashboard')  # Redirect to dashboard to show the register tab with updated information

    else:
        form = StudentRegistrationForm()
        context = {
            'form': form,
            'department': request.session.get('department', ''),
            'program': request.session.get('program', ''),
            'year_of_study': request.session.get('year_of_study', ''),
            'semester': request.session.get('semester', ''),
            'student_name': request.session.get('student_name', ''),
            'registration_number': request.session.get('registration_number', ''),
            'student_index_number': request.session.get('student_index_number', ''),
            'contact_no': request.session.get('contact_no', ''),
            'state': request.session.get('state', ''),
            'county': request.session.get('county', ''),
            'next_of_kin': request.session.get('next_of_kin', ''),
            'next_of_kin_contact': request.session.get('next_of_kin_contact', ''),
            'gender': request.session.get('gender', ''),
            'admission': request.session.get('admission', ''),
            'date_of_birth': request.session.get('date_of_birth', ''),
            'username': request.user.username,
            'registration_status': 'Pending'  # Assuming a default status, adjust as necessary
        }
    return render(request, 'dashboard.html', context)

@login_required
def download_receipt(request):
    department = request.session.get('department', '___________________')
    program = request.session.get('program', '___________________')
    year_of_study = request.session.get('year_of_study', '___________________')
    semester = request.session.get('semester', '___________________')
    student_name = request.session.get('student_name', '___________________')
    registration_number = request.session.get('registration_number', '___________________')
    student_index_number = request.session.get('student_index_number', '___________________')
    contact_no = request.session.get('contact_no', '___________________')
    state = request.session.get('state', '___________________')
    county = request.session.get('county', '___________________')
    next_of_kin = request.session.get('next_of_kin', '___________________')
    next_of_kin_contact = request.session.get('next_of_kin_contact', '___________________')
    gender = request.session.get('gender', '___________________')
    admission = request.session.get('admission', '___________________')
    date_of_birth = request.session.get('date_of_birth', '___________________')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'header',
        parent=styles['Heading2'],
        alignment=1,  # Center alignment
        fontSize=14,
        spaceAfter=14
    )
    field_label_style = ParagraphStyle(
        'field_label',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6
    )
    value_style = ParagraphStyle(
        'value',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=12
    )

    elements = []

    # Title
    title = Paragraph("Payment Invoice", header_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Student and Program Information
    student_info_title = Paragraph("Student Information", header_style)
    elements.append(student_info_title)
    elements.append(Spacer(1, 12))

    # Student Information Fields
    student_fields = [
        ("Department", department),
        ("Program", program),
        ("Year of Study", year_of_study),
        ("Semester", semester),
        ("Student Name", student_name),
        ("Registration Number", registration_number),
        ("Student Index Number", student_index_number),
        ("Contact Number", contact_no),
        ("State", state),
        ("County", county),
        ("Next of Kin", next_of_kin),
        ("Next of Kin Contact", next_of_kin_contact),
        ("Gender", gender),
        ("Admission", admission),
        ("Date of Birth", date_of_birth),
    ]

    for label, value in student_fields:
        elements.append(Paragraph(f"<b>{label}:</b> {value}", value_style))
    elements.append(Spacer(1, 24))

    # Payment Information
    payment_info_title = Paragraph("Payment Information", header_style)
    elements.append(payment_info_title)
    elements.append(Spacer(1, 12))

    payment_fields = [
        ("Tuition Fees", "______________________________________"),
        ("Registration Fees", "______________________________________"),
    ]

    for label, value in payment_fields:
        elements.append(Paragraph(f"<b>{label}:</b> {value}", value_style))
    elements.append(Spacer(1, 24))

    # Bank Account Details
    bank_details_title = Paragraph("Bank Account Details", header_style)
    elements.append(bank_details_title)
    elements.append(Spacer(1, 12))

    bank_details = [
        ("Bank Name", "EcoBank"),
        ("Account Number", "123456789"),
        ("Amount to Pay", "500,000 SSP"),
        ("Branch", "Sample Branch"),
        ("SWIFT Code", "SBININBBXXX"),
    ]

    for label, value in bank_details:
        elements.append(Paragraph(f"<b>{label}:</b> {value}", value_style))
    elements.append(Spacer(1, 24))

    # Page Break if the content is too long
    elements.append(PageBreak())

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

@login_required
def upload_bank_statement(request):
    if request.method == 'POST':
        form = BankStatementForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a BankStatement object
            bank_statement = form.save(commit=False)
            # Associate it with the current user's Student instance
            student = Student.objects.get(user=request.user)
            bank_statement.student = student      
            # Save the BankStatement object
            bank_statement.save()
            return redirect('dashboard')
    else:
        form = BankStatementForm()
    return render(request, 'dashboard.html', {'bank_statement_form': form, 'tab': 'fees', 'username': request.user.username})

@login_required
def combined_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        student = None

    registration_form = StudentRegistrationForm()
    bank_statement_form = BankStatementForm()

    context = {
        'registration_form': registration_form,
        'bank_statement_form': bank_statement_form,
        'registration_status': student.status if student else 'Not Registered',
        'tab': request.GET.get('tab', 'enroll'),
        'username': request.user.username,
        'department': request.session.get('department', ''),
        'program': request.session.get('program', ''),
        'year_of_study': request.session.get('year_of_study', ''),
        'semester': request.session.get('semester', ''),
        'student_name': request.session.get('student_name', ''),
        'registration_number': request.session.get('registration_number', ''),
        'student_index_number': request.session.get('student_index_number', ''),
        'contact_no': request.session.get('contact_no', ''),
        'state': request.session.get('state', ''),
        'county': request.session.get('county', ''),
        'next_of_kin': request.session.get('next_of_kin', ''),
        'next_of_kin_contact': request.session.get('next_of_kin_contact', ''),
        'gender': request.session.get('gender', ''),
        'admission': request.session.get('admission', ''),
        'date_of_birth': request.session.get('date_of_birth', ''),
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def your_view_function(request):
    context = {
        'username': request.user.username  # Assuming user is authenticated
    }
    return render(request, 'dashboard.html', context)
