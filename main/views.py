from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils.dateparse import parse_date, parse_time
from django.views.decorators.csrf import csrf_exempt

from .forms import AnxietyDepressionForm, RegistrationForm, PsychologistSelectionForm
from .models import Specialist, Appointment  # Імпорт моделі Specialist
from .forms import ReviewForm
from django.contrib.auth import login as auth_login, authenticate, logout


def index(request):
    # Відображення головної сторінки
    return render(request, 'main/index.html')

def home(request):
    # Відображення головної сторінки
    return render(request, 'main/index.html')

def login(request, specialist_id=None):
    if request.user.is_authenticated:
        if specialist_id:
            return redirect('booking_page', specialist_id=specialist_id)
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if specialist_id:
                return redirect('booking_page', specialist_id=specialist_id)
            return redirect('home')
        else:
            context = {'error': 'Неправильний логін або пароль'}
            if specialist_id:
                context['specialist_id'] = specialist_id
            return render(request, 'main/login.html', context)

    # Відображення сторінки входу
    return render(request, 'main/login.html', {'specialist_id': specialist_id if specialist_id else None})


def test(request):
    if request.method == 'POST':
        form = AnxietyDepressionForm(request.POST)
        if form.is_valid():
            anxiety_score, depression_score = form.calculate_scores()
            request.session['results'] = {
                'anxiety_score': anxiety_score,
                'depression_score': depression_score
            }
            return redirect('test_result')
        else:
            return render(request, 'main/test.html', {'form': form})
    else:
        form = AnxietyDepressionForm()
        return render(request, 'main/test.html', {'form': form})

def test_result(request):
    if request.session.get('results'):
        context = request.session.pop('results')
        return render(request, 'main/test_result.html', context)
    else:
        # Перенаправити користувача назад на форму тестування, якщо немає збережених результатів
        return redirect('test')

def psychologist(request):
    if request.method == 'POST':
        form = PsychologistSelectionForm(request.POST)
        if form.is_valid():
            selected_tags = [value for key, value in form.cleaned_data.items() if value]
            specialists = Specialist.objects.filter(tags__name__in=selected_tags).distinct()
            return render(request, 'main/specialists.html', {'specialists': specialists})
    else:
        form = PsychologistSelectionForm()

    # Завжди повертайте HttpResponse
    return render(request, 'main/psychologist.html', {'form': form})

def specialists(request):
    selected_tags = request.session.get('selected_tags', [])
    if selected_tags:
        # Фільтрація спеціалістів, що мають хоча б один із вибраних тегів
        specialists = Specialist.objects.filter(tags__name__in=selected_tags).distinct()
    else:
        specialists = Specialist.objects.all()

    return render(request, 'main/specialists.html', {'specialists': specialists})



def specialist_detail(request, id):
    specialist = get_object_or_404(Specialist, pk=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.specialist = specialist
            review.save()
            return redirect('specialist_detail', id=id)
    else:
        form = ReviewForm()

    reviews = specialist.reviews.all()
    return render(request, 'main/specialist_detail.html', {'specialist': specialist, 'form': form, 'reviews': reviews})


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Тут user автоматично зберігається
            auth_login(request, user)  # Автоматичний вхід після реєстрації
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'main/registration_page.html', {'form': form})

def registration_with_specialist(request, specialist_id):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            request.session['specialist_id'] = specialist_id
            return redirect('login_with_specialist', specialist_id=specialist_id)
    else:
        form = RegistrationForm()
    return render(request, 'main/registration_page.html', {'form': form, 'specialist_id': specialist_id})


@login_required
def booking_page(request, specialist_id):
    specialist = get_object_or_404(Specialist, pk=specialist_id)
    if request.method == 'POST':
        date_str = request.POST.get('appointment_date')
        time_str = request.POST.get('appointment_time')
        date = parse_date(date_str)
        time = parse_time(time_str)

        if not date or not time:
            return JsonResponse({'error': 'Дата та час мають бути вказані.'}, status=400)

        try:
            appointment = Appointment.objects.create(
                user=request.user,
                specialist=specialist,
                date=date,
                time=time
            )
            return JsonResponse({
                'message': 'Запис успішно створено!',
                'appointment_info': appointment.formatted_datetime()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'main/booking_page.html', {'specialist': specialist})
def custom_logout_view(request):
    logout(request)  # Вихід користувача
    return redirect('home')  # Переадресація на головну сторінку