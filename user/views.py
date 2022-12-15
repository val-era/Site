from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    #if request.method == 'POST':
        #form = UserRegisterForm(request.POST)
        #if form.is_valid():
            #username = form.cleaned_data.get('User_name')
            #form.save()
            #messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            #return redirect('login')
    #else:
        #form = UserRegisterForm()
    return render(request, 'user/register.html' ) #{'form': form})


@login_required
def profile(request):
    return render(request, 'page2/index.html')