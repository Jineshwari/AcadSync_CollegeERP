# Generated by Django 5.0.7 on 2025-03-28 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0007_alter_submission_assignment_alter_submission_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='resources/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='faculty.classroom')),
            ],
        ),
    ]
