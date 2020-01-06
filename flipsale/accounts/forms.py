from django import forms
# from django.contrib.auth.models import User
from django.forms import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    fullName = forms.CharField(label="Full Name", required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}))
    mobile = forms.IntegerField(label="Mobile", widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Mobile'}))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    cpwd = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data.get('email')).exists():
            raise ValidationError("Email already in use.")
        return self.cleaned_data.get('email')

    def clean(self):
        data = self.cleaned_data
        if data.get('pwd') != data.get('cpwd'):
            raise ValidationError("Password don't match.")
        return data