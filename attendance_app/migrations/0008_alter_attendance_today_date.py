# Generated by Django 4.0.5 on 2022-06-02 12:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_app', '0007_alter_attendance_today_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='today_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
