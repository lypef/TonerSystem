from django.shortcuts import render
from django.http import HttpResponse 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


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

    errors = []
    if request.method == 'POST':
    	if not request.POST.get('nombre', ''): 
    		errors.append('Falta nombre de cliente.') 
    	if not request.POST.get('empresa', ''): 
    		errors.append('Falta el nombre de la empresa.')
    	
           	
    	if not errors:
    		return HttpResponse('Cliente agregado con exito.') 

    	
    return render(request, 'newclient.html', {'errors': errors, 
        'nombre': request.POST.get('nombre', ''),
        'empresa': request.POST.get('empresa', ''),
        'direccion': request.POST.get('direccion', ''),
        'telefono': request.POST.get('telefono', ''),
        'movil': request.POST.get('movil', ''),
        'email': request.POST.get('email', '')
        }) 
