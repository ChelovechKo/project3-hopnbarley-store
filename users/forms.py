from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from typing import Any, Dict

UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserModel
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

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if cleaned_data is None:
            return {}
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email") or ""
        email = str(email)
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'class': 'Input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'qwerty123', 'class': 'Input'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email', 'username', 'first_name', 'last_name', 'phone', 'city', 'address')
        widgets = {
            'email': forms.EmailInput(
                attrs={'placeholder': 'example@mail.com', 'class': 'Input'}),
            'username': forms.TextInput(
                attrs={'placeholder': 'Your username', 'class': 'Input'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'John', 'class': 'Input'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Doe', 'class': 'Input'}),
            'phone': forms.TextInput(
                attrs={'placeholder': '+(123)1234567', 'class': 'Input'}),
            'city': forms.TextInput(
                attrs={'placeholder': 'City', 'class': 'Input'}),
            'address': forms.Textarea(
                attrs={'placeholder': 'Address', 'class': 'Textarea', 'rows': 3})
        }
        labels = {
            'email': 'Email',
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone',
            'address': 'Address',
            'city': 'City',
        }
