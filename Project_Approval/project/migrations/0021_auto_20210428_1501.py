# Generated by Django 3.1.7 on 2021-04-28 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_student_enrollment_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='enrollment_no',
            field=models.CharField(max_length=20),
        ),
    ]
