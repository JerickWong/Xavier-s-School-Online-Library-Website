# Generated by Django 3.0.5 on 2020-05-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_library', '0004_auto_20200504_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='book_manager',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='student_teacher',
            field=models.BooleanField(default=True),
        ),
    ]
