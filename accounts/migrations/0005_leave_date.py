# Generated by Django 4.0.5 on 2022-06-04 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_leave'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]