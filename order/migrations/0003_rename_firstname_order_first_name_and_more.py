# Generated by Django 4.1.7 on 2023-06-14 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='firstname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='lastname',
            new_name='last_name',
        ),
    ]
