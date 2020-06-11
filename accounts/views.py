from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    if(request.method == 'POST'):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if(password1 == password2):
            if(User.objects.filter(username=username).exists()):
                messages.info(request, 'Username taken')
                return redirect('/')
            elif(User.objects.filter(email=email).exists()):
                messages.info(request, 'email taken')
                return redirect('/')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)

                user.save()
                messages.info(request, 'user created')
                return redirect('/dashboard')
        else:
            messages.info(request, 'passwords dont match')
            return redirect('/')

    else:
        return redirect('/')
