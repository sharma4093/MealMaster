# Generated by Django 4.1.7 on 2023-05-04 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_mess_off_leave_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mess_off_leave',
            name='days',
        ),
    ]