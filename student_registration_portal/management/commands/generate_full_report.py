# myapp/management/commands/generate_full_report.py
from django.core.management.base import BaseCommand
from student_registration_portal.models import Student, BankStatement
import pandas as pd
import io

class Command(BaseCommand):
    help = 'Generate a full report of all students and bank statements'

    def handle(self, *args, **options):
        # Query all student data
        students = Student.objects.all().values('student_name', 'registration_number', 'status', 'contact_no', 'state', 'county')

        # Query all bank statements data
        bank_statements = BankStatement.objects.all().values('student__student_name', 'statement', 'uploaded_at')

        # Create DataFrames
        df_students = pd.DataFrame(students)
        df_statements = pd.DataFrame(bank_statements)

        # Save the reports to files
        buffer_students = io.StringIO()
        df_students.to_csv(buffer_students, index=False)
        buffer_students.seek(0)

        buffer_statements = io.StringIO()
        df_statements.to_csv(buffer_statements, index=False)
        buffer_statements.seek(0)

        # Write files to disk
        with open('full_student_report.csv', 'w') as file:
            file.write(buffer_students.read())

        with open('full_bank_statement_report.csv', 'w') as file:
            file.write(buffer_statements.read())

        self.stdout.write(self.style.SUCCESS('Successfully generated the full reports'))
