# Generated by Django 5.0.6 on 2024-06-26 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration_portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='contact_no',
            field=models.IntegerField(max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='next_of_kin_contact',
            field=models.IntegerField(max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_number',
            field=models.IntegerField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_index_number',
            field=models.IntegerField(max_length=50),
        ),
    ]
