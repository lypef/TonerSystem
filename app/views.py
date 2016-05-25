from django.shortcuts import render
from django.http import HttpResponse 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from models import clients

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
    		errors.append('error') 
    		messages.add_message(request, messages.INFO, 'Ingrese el nombre.')
    	if not request.POST.get('empresa', ''): 
    		errors.append('error')
    		messages.add_message(request, messages.INFO, 'Ingrese empresa.')
    	if request.POST.get('telefono', '') and not request.POST.get('telefono', '').isdigit(): 
            errors.append('error')
            messages.add_message(request, messages.INFO, 'El telefono no es valido.')
        if request.POST.get('movil', '') and not request.POST.get('movil', '').isdigit(): 
            errors.append('error')
            messages.add_message(request, messages.INFO, 'El movil no es valido.')    
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('error')
            messages.add_message(request, messages.INFO, 'El email no es valido.')    

    	if not errors:
    		insert = clients(nombre = request.POST.get('nombre', '').upper(), 
    			empresa = request.POST.get('empresa', '').upper(),
    			direccion = request.POST.get('direccion', '').upper(),
    			telefono = request.POST.get('telefono', ''),
    			movil = request.POST.get('movil', ''),
    			email = request.POST.get('email', '')
    			)
    		insert.save()
    		messages.add_message(request, messages.INFO, 'Cliente agregado con exito')
    		return render(request,'manage.html')

    	
    return render(request, 'newclient.html', {
        'nombre': request.POST.get('nombre', ''),
        'empresa': request.POST.get('empresa', ''),
        'direccion': request.POST.get('direccion', ''),
        'telefono': request.POST.get('telefono', ''),
        'movil': request.POST.get('movil', ''),
        'email': request.POST.get('email', '')
        }) 
def search(request):
    
    if request.method == "POST":
        return render (request,'manage.html')
    return render (request,'search.html')

def list_clients(request):
    Lclients = clients
    return render (request,'list_clients.html',{'Lclientes':Lclients})