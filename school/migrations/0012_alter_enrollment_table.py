# Generated by Django 5.0.6 on 2024-09-19 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_rename_enrollment_date_enrollment_enrollmentdate_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='enrollment',
            table='school_enrollment',
        ),
    ]
