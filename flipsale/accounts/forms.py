from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(label="User Name     ", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    

class RegisterForm(forms.Form):
    username = forms.CharField(label="User Name     ", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}))
    firstName = forms.CharField(label="First Name", required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}))
    lastName = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    pwd = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    cpwd = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            raise ValidationError("Username already taken.")
        return self.cleaned_data.get('username')

    def clean(self):
        data = self.cleaned_data
        if data.get('pwd') != data.get('cpwd'):
            raise ValidationError("Password don't match.")
        return data