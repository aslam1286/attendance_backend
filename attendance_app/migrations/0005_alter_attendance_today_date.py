# Generated by Django 4.0.4 on 2022-05-27 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_app', '0004_alter_attendance_today_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='today_date',
            field=models.TextField(max_length=255, null=True),
        ),
    ]
