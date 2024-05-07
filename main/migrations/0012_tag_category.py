# Generated by Django 5.0.4 on 2024-05-07 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_tag_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='category',
            field=models.CharField(choices=[('therapy_type', 'Тип терапії'), ('gender', 'Стать'), ('price', 'Цінова категорія'), ('experience', 'Досвід'), ('specialist_type', 'Тип спеціаліста'), ('method', 'Метод терапії'), ('age_preference', 'Перевага віку'), ('issue', 'Проблематика')], default='issue', max_length=20),
        ),
    ]
