from django.contrib import admin
from .models import Specialist, Tag, Certification, Review, Appointment

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']

class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'reviews_count', 'service_price')
    list_filter = ('rating', 'tags__category')
    search_fields = ('name', 'description', 'about_me', 'education')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('name', 'image', 'description', 'tags')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('rating', 'service_price', 'about_me', 'education'),
        }),
    )
    inlines = [CertificationInline]

    def reviews_count(self, obj):
        return obj.reviews.count()
    reviews_count.short_description = 'Кількість відгуків'

admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Certification)
admin.site.register(Appointment)
