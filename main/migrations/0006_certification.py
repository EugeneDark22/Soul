# Generated by Django 5.0.4 on 2024-05-03 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_specialist_about_me_specialist_education_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='certifications/')),
                ('specialist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='main.specialist')),
            ],
        ),
    ]
