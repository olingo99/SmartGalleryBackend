# Generated by Django 4.2.5 on 2023-11-20 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartGalleryAPI', '0006_croppedface'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='Persons',
            field=models.ManyToManyField(through='SmartGalleryAPI.LinkPhotoPerson', to='SmartGalleryAPI.person'),
        ),
    ]