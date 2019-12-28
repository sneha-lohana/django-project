from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def logout_page(request):
    logout(request)
    return redirect("home")

def login_page(request):
    loginform = LoginForm(request.POST or None)
    context = {'form':loginform}
    if loginform.is_valid():
        un = loginform.data.get('username')
        pwd = loginform.data.get('pwd')
        # print(un, pwd)
        user = authenticate(username=un, password=pwd)
        print(user)
        if user:
            login(request, user)
            return redirect("home")
        context['errmsg'] = "Invalid Credentials"
    return render(request, "accounts/login.html", context)

def register_page(request):
    if request.method == 'GET':
        reg_form = RegisterForm()
    
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
    
    # reg_form = RegisterForm(request.POST or None)
    
    context = {'form': reg_form}
    if reg_form.is_valid():
        # print(password=reg_form.cleaned_data.get('pwd'))
        user = User.objects.create_user(username=reg_form.cleaned_data.get('username'),
        password=reg_form.cleaned_data.get('pwd'),
        email=reg_form.cleaned_data.get('email'), first_name=reg_form.cleaned_data.get('firstName'),
        last_name=reg_form.cleaned_data.get('lastName'))
        if user:
            context['reg_form'] = RegisterForm()
            context['msg'] = "User created successfully."
    
    return render(request, "accounts/register.html",context)