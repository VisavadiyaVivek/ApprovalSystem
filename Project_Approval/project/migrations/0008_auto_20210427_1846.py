# Generated by Django 3.1.7 on 2021-04-27 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20210427_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='team_id',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='project.team'),
        ),
    ]
