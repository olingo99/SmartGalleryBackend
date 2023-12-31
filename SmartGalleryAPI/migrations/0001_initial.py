# Generated by Django 4.2.5 on 2023-10-04 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateTimeField(auto_created=True)),
                ('Path', models.CharField(max_length=200)),
                ('Locataion', models.CharField(max_length=200)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LinkPhotoPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BoundingBox', models.CharField(max_length=100)),
                ('Person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SmartGalleryAPI.person')),
                ('Photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SmartGalleryAPI.photo')),
            ],
        ),
    ]
