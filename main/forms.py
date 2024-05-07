from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput, TimeInput
from django.utils.translation import gettext_lazy as _
from .models import Review, UserProfile
from .models import Tag

class AnxietyDepressionForm(forms.Form):
    SCORING = [
        ('A', [(3, "Весь час"), (2, "Часто"), (1, "Час від часу, іноді"), (0, "Зовсім не відчуваю")]),
        ('D', [(0, "Безумовно так"), (1, "Напевно, що так"), (2, "Лише в дуже малому ступені це так"), (3, "Це зовсім не так")]),
        ('A', [(3, "Безумовно так, і страх дуже сильний"), (2, "Це так, але страх не дуже сильний"), (1, "Іноді, але це мене не турбує"), (0, "Зовсім не відчуваю")]),
        ('D', [(0, "Безумовно так"), (1, "Напевно, що так"), (2, "Лише в дуже малому ступені це так"), (3, "Зовсім не здатний")]),
        ('A', [(3, "Постійно"), (2, "Велику частину часу"), (1, "Час від часу і не так часто"), (0, "Тільки іноді")]),
        ('D', [(3, "Зовсім не відчуваю"), (2, "Дуже рідко"), (1, "Іноді"), (0, "Практично весь час")]),
        ('A', [(0, "Безумовно так"), (1, "Напевно, що так"), (2, "Лише зрідка це так"), (3, "Зовсім не можу")]),
        ('D', [(3, "Практично весь час"), (2, "Часто"), (1, "Іноді"), (0, "Зовсім ні")]),
        ('A', [(0, "Зовсім не відчуваю"), (1, "Іноді"), (2, "Часто"), (3, "Дуже часто")]),
        ('D', [(3, "Безумовно так"), (2, "Я не приділяю цьому стільки часу, скільки потрібно"), (1, "Може бути, я став менше приділяти цьому уваги"), (0, "Я стежу за собою так само, як і раніше")]),
        ('A', [(3, "Безумовно так"), (2, "Напевно, що так"), (1, "Лише в деякій мірі це так"), (0, "Зовсім не відчуваю")]),
        ('D', [(0, "Точно так само, як і зазвичай"), (1, "Так, але не в тій мірі, як раніше"), (2, "Значно менше, ніж зазвичай"), (3, "Зовсім так не вважаю")]),
        ('A', [(3, "Дуже часто"), (2, "Досить часто"), (1, "Не так уже часто"), (0, "Зовсім не буває")]),
        ('D', [(0, "Часто"), (1, "Іноді"), (2, "Рідко"), (3, "Дуже рідко")]),
    ]

    def __init__(self, *args, **kwargs):
        super(AnxietyDepressionForm, self).__init__(*args, **kwargs)
        for idx, (category, choices) in enumerate(self.SCORING, 1):
            field_name = f'question{idx}'
            self.fields[field_name] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=f'Питання {idx}'
            )

    def calculate_scores(self):
        anxiety_score = 0
        depression_score = 0
        for idx, (category, _) in enumerate(self.SCORING, 1):
            field_name = f'question{idx}'
            score = int(self.cleaned_data.get(field_name, 0))
            if category == 'A':
                anxiety_score += score
            elif category == 'D':
                depression_score += score
        return anxiety_score, depression_score

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['author_name', 'rating', 'text']
        labels = {
            'author_name': 'Ім\'я автора',
            'rating': 'Рейтинг',
            'text': 'Текст відгука'
        }
        widgets = {
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
        }

class RegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=13, required=True, label=_("Телефон"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone')
        labels = {
            'username': _('Ім\'я користувача'),
            'email': _('Електронна пошта'),
            'password1': _('Пароль'),
            'password2': _('Підтвердження пароля'),
            'phone': _('Телефон'),
        }
        help_texts = {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
            'phone': '',
        }
        error_messages = {
            'username': {
                'unique': _("Це ім'я користувача вже зайняте."),
            },
            'email': {
                'unique': _("Ця електронна пошта вже зареєстрована."),
            },
        }


class PsychologistSelectionForm(forms.Form):
    # Завантаження виборів для кожної категорії з бази даних
    therapy_type_choices = list(Tag.objects.filter(category='therapy_type').values_list('name', 'name'))
    gender_choices = list(Tag.objects.filter(category='gender').values_list('name', 'name'))
    price_choices = list(Tag.objects.filter(category='price').values_list('name', 'name'))
    experience_choices = list(Tag.objects.filter(category='experience').values_list('name', 'name'))
    specialist_type_choices = list(Tag.objects.filter(category='specialist_type').values_list('name', 'name'))
    method_choices = list(Tag.objects.filter(category='method').values_list('name', 'name'))
    age_preference_choices = list(Tag.objects.filter(category='age_preference').values_list('name', 'name'))
    issue_choices = list(Tag.objects.filter(category='issue').values_list('name', 'name'))

    therapy_type = forms.MultipleChoiceField(
        choices=therapy_type_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Який тип терапії вас цікавить?'
    )
    gender = forms.MultipleChoiceField(
        choices=gender_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Якої статі має бути фахівець?'
    )
    price = forms.MultipleChoiceField(
        choices=price_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Яка ціна за сесію буде для вас комфортна?'
    )
    experience = forms.MultipleChoiceField(
        choices=experience_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Спеціаліст має досвід роботи'
    )
    specialist_type = forms.MultipleChoiceField(
        choices=specialist_type_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Якого спеціаліста Ви шукаєте?'
    )
    method = forms.MultipleChoiceField(
        choices=method_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Якому методу роботи віддаєте перевагу?'
    )
    age_preference = forms.MultipleChoiceField(
        choices=age_preference_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='З яким психологом Вам буде комфортніше працювати?'
    )
    primary_issues = forms.MultipleChoiceField(
        choices=issue_choices,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        label='Оберіть до 3 запитів, які ви бажаєте обговорити першочергово'
    )