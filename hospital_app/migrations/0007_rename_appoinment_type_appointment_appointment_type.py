# Generated by Django 5.0.1 on 2024-09-23 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0006_doctor_details_appoinment_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='appoinment_type',
            new_name='appointment_type',
        ),
    ]
