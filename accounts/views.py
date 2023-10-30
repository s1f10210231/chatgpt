from django.contrib.auth import login
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('login'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
