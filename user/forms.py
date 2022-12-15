from django import forms


class UserRegisterForm(forms.Form):
    User_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Почта'}))
    Password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    Password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторный пароль'}))
    Check_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Код проверки'}))
