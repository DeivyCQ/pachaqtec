# Generated by Django 3.0.8 on 2020-11-29 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='programa',
            name='slug',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
