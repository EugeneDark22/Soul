from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import specialist_detail, custom_logout_view

urlpatterns = [
    path('', views.index),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('login/specialist/<int:specialist_id>/', views.login, name='login_with_specialist'),  # Змініть шлях для більшої ясності
    path('test/', views.test, name='test'),
    path('test/result/', views.test_result, name='test_result'),
    path('psychologist/', views.psychologist, name='psychologist'),
    path('specialists/', views.specialists, name='specialists'),
    path('specialist/<int:id>/', specialist_detail, name='specialist_detail'),
    path('registration/', views.registration_view, name='registration_view'),
    path('registration/<int:specialist_id>/', views.registration_with_specialist, name='registration_with_specialist'),
    path('booking/<int:specialist_id>/', views.booking_page, name='booking_page'),
    path('logout/', custom_logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)