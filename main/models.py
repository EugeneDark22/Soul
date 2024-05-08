from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Tag(models.Model):
    CATEGORY_CHOICES = [
        ('therapy_type', 'Тип терапії'),
        ('gender', 'Стать'),
        ('price', 'Цінова категорія'),
        ('experience', 'Досвід'),
        ('specialist_type', 'Тип спеціаліста'),
        ('method', 'Метод терапії'),
        ('age_preference', 'Перевага віку'),
        ('issue', 'Проблематика'),
    ]
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='issue')

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

# Оновлена модель Specialist
class Specialist(models.Model):
    name = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='specialists')
    rating = models.PositiveIntegerField(default=5)
    review_count = models.PositiveIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(upload_to='specialists_images/')
    service_price = models.DecimalField(max_digits=8, decimal_places=2)
    about_me = models.TextField()
    education = models.TextField()

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def reviews_count(self):
        return self.reviews.all().count()

class Certification(models.Model):
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE, related_name='certifications')
    image = models.ImageField(upload_to='certifications/')

    def __str__(self):
        return f"{self.specialist.name} Certification"

class Review(models.Model):
    specialist = models.ForeignKey(Specialist, related_name='reviews', on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    text = models.TextField()

    def __str__(self):
        return f"Review by {self.author_name} for {self.specialist.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    def __str__(self):
        return f'{self.user.username} Profile'


class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.specialist.name} на {self.date} о {self.time}'

    def formatted_datetime(self):
        return f'{self.date.strftime("%d %b %Y")} о {self.time.strftime("%H:%M")}'