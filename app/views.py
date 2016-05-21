from django.shortcuts import render
from django.http import HttpResponse 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django import forms

# Create your views here.
def login(request): 

    if request.user.is_authenticated():
    	return render(request,'manage.html')
    return render(request,'login.html')

@login_required
def manage(request):

    return render(request,'manage.html')

@login_required
def newclient(request):
    if request.method == 'POST':
    	return render(request,'manage.html')
    
    return render (request,'newclient.html')
