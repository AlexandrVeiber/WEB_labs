from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин или E-mail',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким E-mail уже существует.')

        return email
    
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        disabled=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='E-mail',
        disabled=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Старый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )