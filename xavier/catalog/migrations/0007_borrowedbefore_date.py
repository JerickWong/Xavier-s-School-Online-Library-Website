# Generated by Django 3.0.5 on 2020-05-21 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20200521_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowedbefore',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='Date Borrowed'),
        ),
    ]
