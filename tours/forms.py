from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Tour, Category, TagPost


DIRECTION_CHOICES = [
    ('', 'Направление не выбрано'),
    ('city', 'Городские экскурсии'),
    ('siberia', 'Туры по Сибири'),
    ('weekend', 'Туры выходного дня'),
]


def russian_title_validator(value):
    allowed_chars = (
        'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
        'абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
        '0123456789- '
    )

    if not set(value) <= set(allowed_chars):
        raise ValidationError(
            'Название должно содержать только русские буквы, цифры, пробел и дефис.'
        )


class AddTourForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        min_length=5,
        label='Название тура',
        validators=[russian_title_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Введите название тура.',
            'min_length': 'Название тура должно содержать минимум 5 символов.',
        }
    )

    slug = forms.SlugField(
        max_length=255,
        label='URL',
        validators=[
            MinLengthValidator(5, message='URL должен содержать минимум 5 символов.'),
            MaxLengthValidator(100, message='URL должен содержать не более 100 символов.'),
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Введите URL тура.',
            'invalid': 'URL может содержать только латинские буквы, цифры, дефис и подчёркивание.',
        }
    )

    description = forms.CharField(
        required=False,
        label='Описание',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
        })
    )

    duration = forms.CharField(
        required=False,
        max_length=100,
        label='Продолжительность',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    price = forms.CharField(
        required=False,
        max_length=100,
        label='Стоимость',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    direction = forms.ChoiceField(
        required=False,
        choices=DIRECTION_CHOICES,
        label='Направление',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Категория не выбрана',
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.all(),
        required=False,
        label='Теги',
        widget=forms.CheckboxSelectMultiple()
    )

    is_published = forms.TypedChoiceField(
        choices=Tour.Status.choices,
        coerce=int,
        initial=Tour.Status.PUBLISHED,
        label='Статус публикации',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def clean_slug(self):
        slug = self.cleaned_data['slug']

        if Tour.objects.filter(slug=slug).exists():
            raise ValidationError('Тур с таким URL уже существует.')

        return slug


class AddTourModelForm(forms.ModelForm):
    title = forms.CharField(
        max_length=255,
        label='Название тура',
        validators=[russian_title_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Введите название тура.',
        }
    )

    direction = forms.ChoiceField(
        required=False,
        choices=DIRECTION_CHOICES,
        label='Направление',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    cat = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Категория не выбрана',
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=TagPost.objects.all(),
        required=False,
        label='Теги',
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Tour
        fields = [
            'title',
            'slug',
            'description',
            'photo',
            'duration',
            'price',
            'direction',
            'cat',
            'tags',
            'is_published',
        ]

        labels = {
            'slug': 'URL',
            'description': 'Описание',
            'photo': 'Фото тура',
            'duration': 'Продолжительность',
            'price': 'Стоимость',
            'is_published': 'Статус публикации',
        }

        widgets = {
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
            }),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'is_published': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) > 50:
            raise ValidationError('Длина названия тура не должна превышать 50 символов.')

        return title


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Файл',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )