# Generated by Django 4.2.5 on 2023-11-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartGalleryAPI', '0009_alter_person_name_alter_person_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='Tag',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
