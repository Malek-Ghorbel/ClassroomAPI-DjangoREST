# Generated by Django 4.2.7 on 2023-11-09 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_classroom', '0002_rename_name_classroom_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='teacher',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_classrooms', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]