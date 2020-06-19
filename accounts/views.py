from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import UserRegisterForm


def index(request):
    if(request.user.is_authenticated):
        return redirect('/app')
    return redirect('/login')


def register(request):
    if request.method.lower() == 'post':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account is created! You will now be able to login.')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
