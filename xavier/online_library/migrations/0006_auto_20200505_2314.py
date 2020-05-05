# Generated by Django 3.0.5 on 2020-05-05 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_library', '0005_auto_20200505_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_number',
            field=models.CharField(default='N/A', editable=False, help_text='After your account has been created, it can never be edited.', max_length=8, verbose_name='ID Number'),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
