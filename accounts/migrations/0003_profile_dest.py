# Generated by Django 4.0.5 on 2022-06-03 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='dest',
            field=models.CharField(max_length=50, null=True),
        ),
    ]