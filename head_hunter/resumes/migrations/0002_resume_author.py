# Generated by Django 4.1.2 on 2022-11-14 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resumes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to=settings.AUTH_USER_MODEL, verbose_name='Автор резюме'),
        ),
    ]
