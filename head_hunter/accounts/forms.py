from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Group


class LoginForm(forms.Form):
    email = forms.CharField(required=True, label='Логин')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)
    next = forms.CharField(required=False, widget=forms.HiddenInput)


class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True, widget=forms.PasswordInput)
    phone = forms.CharField(label='Номер телефона')

    class Meta:
        model = get_user_model()
        fields = ('user_category', 'username', 'email', 'password', 'password_confirm', 'phone',  'avatar',)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
            # group_name = 'basic_users'
            # group = Group.objects.get(name=group_name)
            # user.groups.add(group)
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'avatar', 'phone', 'avatar')
        labels = {'username': 'Имя пользователя', 'email': 'Email'}


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']
