# Generated by Django 4.2.14 on 2024-07-17 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comments',
            new_name='Comment',
        ),
    ]
