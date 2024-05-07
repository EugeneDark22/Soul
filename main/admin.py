from django.contrib import admin
from .models import Specialist, Tag, Certification, Review, Appointment


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1  # How many rows to show


class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'reviews_count', 'service_price')  # Змінено на reviews_count
    list_filter = ('rating', 'tags')
    search_fields = ('name', 'description', 'about_me', 'education')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('name', 'image', 'description', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('rating', 'service_price', 'about_me', 'education'),  # Вилучено reviews з налаштувань
        }),
    )
    inlines = [CertificationInline]

    def reviews_count(self, obj):
        return obj.reviews.count()  # Використовує related_name 'reviews' для підрахунку відгуків
    reviews_count.short_description = 'Кількість відгуків'  # Задає назву колонки

admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Tag)
admin.site.register(Certification)
admin.site.register(Appointment)