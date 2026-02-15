from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Paper


# ---------------------------------------------------
# PAPER FORM
# ---------------------------------------------------
class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = [
            'title',
            'abstract',
            'keywords',
            'field',
            'teacher',
            'file'
        ]


# ---------------------------------------------------
# REGISTER FORM
# ---------------------------------------------------
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password']

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_password")

        if pwd != cpwd:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned


# ---------------------------------------------------
# LOGIN FORM
# ---------------------------------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


