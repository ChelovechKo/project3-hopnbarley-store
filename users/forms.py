from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # TODO: потерялись стили для полей с паролями
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}),
            'username': forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'Input'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'John', 'class': 'Input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Smith', 'class': 'Input'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'qwerty123', 'class': 'Input'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'qwerty123', 'class': 'Input'})
        }

        labels = {
            'email': 'Email',
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password1': 'Password',
            'password2': 'Confirm Password'
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'qwerty123', 'class': 'Input'}))