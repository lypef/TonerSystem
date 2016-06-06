from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from models import clients, cartridges

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
    		return redirect('/list_clients')


    	
    return render(request, 'newclient.html', {
        'nombre': request.POST.get('nombre', ''),
        'empresa': request.POST.get('empresa', ''),
        'direccion': request.POST.get('direccion', ''),
        'telefono': request.POST.get('telefono', ''),
        'movil': request.POST.get('movil', ''),
        'email': request.POST.get('email', '')
        }) 

@login_required
def list_clients(request):
    if request.method == "GET":
        Llclients = clients.objects.all().order_by('-id')   
    if request.method == "POST":
        Llclients = clients.objects.filter(nombre__contains=request.POST.get('search', '')).order_by('nombre')
            
    paginator = Paginator(Llclients, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        Lclients = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        Lclients = paginator.page(1)
    except EmptyPage:
        # If page is out osf range (e.g. 9999), deliver last page of results.
        Lclients = paginator.page(paginator.num_pages)

    return render (request,'list_clients.html',{'Lclients':Lclients})

@login_required
def list_clients_edit(request):
    try:
        update = clients.objects.get(id=request.POST.get('id', ''))
        update.nombre = request.POST.get('nombre', '').upper()
        update.empresa = request.POST.get('empresa', '').upper()
        update.direccion = request.POST.get('direccion', '').upper()
        update.telefono = request.POST.get('telefono', '').upper()
        update.movil = request.POST.get('movil', '').upper()
        update.email = request.POST.get('email', '').upper()
        update.save()
        
        messages.add_message(request, messages.INFO, 'Cliente editado con exito')
        return redirect ('/list_clients') 
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_clients') 
    
@login_required
def list_clients_delete(request):
    try:
        delete = clients.objects.get(id= request.POST.get('id',''))
        delete.delete()

        messages.add_message(request, messages.INFO, 'Cliente eliminado con exito')
        return redirect ('/list_clients')        

    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_clients')        
    
@login_required
def newcartridges(request):
    Lclients = clients.objects.all().order_by('nombre')
    

    if request.method == 'POST':
        errors = []
        if not request.POST.get('modelo_toner', ''): 
            errors.append('error') 
            messages.add_message(request, messages.INFO, 'Ingrese el modelo')
        if not request.POST.get('cliente', ''): 
            errors.append('error')
            messages.add_message(request, messages.INFO, 'Seleccione un cliente')
        
        if not request.POST.get('numero_recarga', ''): 
            errors.append('error')
            messages.add_message(request, messages.INFO, 'Ingrese un numero maximo de recargas')
        
        if not errors:
            try:
                insert = cartridges(
                    modelo_imp = request.POST.get('modelo_impresora', '').upper(), 
                    modelo = request.POST.get('modelo_toner', '').upper(), 
                    numero_recarga_maxima = request.POST.get('numero_recarga', ''), 
                    client = clients.objects.get(id=request.POST.get('cliente', '')), 
                    descripcion = request.POST.get('descripcion', '').upper(), 
                    observaciones = request.POST.get('observaciones', '').upper(),
                    cilindro_drum = 0,
                    rodillo_magnetico = 0,
                    rodillo_carga = 0,
                    cuchilla_impiadora = 0,
                    cuchilla_dosificadora = 0
                )
                insert.save()
                messages.add_message(request, messages.INFO, 'Cartucho agregado con exito')
                return redirect('/list_cartridges')
            except Exception, e:
                messages.add_message(request, messages.INFO, e)

    
    

    return render(request, 'newcartridges.html', {
        'modelo_impresora': request.POST.get('modelo_impresora', ''),
        'modelo_toner': request.POST.get('modelo_toner', ''),
        'numero_recarga': request.POST.get('numero_recarga', ''),
        'descripcion': request.POST.get('descripcion', ''),
        'observaciones': request.POST.get('observaciones', ''),
        'Lclients': Lclients, 
        
        }) 

@login_required
def list_cartridges(request):
    Lclients = clients.objects.all()

    if request.method == "GET":
        Lcartridges = cartridges.objects.all().order_by('-id')   
    if request.method == "POST":
        Lcartridges = cartridges.objects.filter(id__contains=request.POST.get('code', '')).order_by('id')
            
    paginator = Paginator(Lcartridges, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        Lcartridges = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        Llcartridges = paginator.page(1)
    except EmptyPage:
        # If page is out osf range (e.g. 9999), deliver last page of results.
        Lcartridges = paginator.page(paginator.num_pages)

    return render (request,'list_cartridges.html',{'Lclients':Lcartridges, 'Lclients0': Lclients})

@login_required
def list_cartridges_edit(request):
    try:
        update = cartridges.objects.get(id=request.POST.get('id', ''))
        update.modelo_imp = request.POST.get('modelo_impresora', '').upper()
        update.modelo = request.POST.get('modelo_toner', '').upper()
        update.numero_recarga_maxima = request.POST.get('numero_recarga', '').upper()
        update.client = clients.objects.get(id=request.POST.get('clientselect', ''))
        update.descripcion = request.POST.get('descripcion', '').upper()
        update.observaciones = request.POST.get('observaciones', '').upper()
        update.save()
        
        messages.add_message(request, messages.INFO, 'Cartucho editado con exito')
        return redirect ('/list_cartridges') 
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_cartridges')     


@login_required
def list_cartridges_delete(request):
    try:
        delete = cartridges.objects.get(id= request.POST.get('id',''))
        delete.delete()

        messages.add_message(request, messages.INFO, 'Cartucho eliminado con exito')
        return redirect ('/list_cartridges')        

    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_cartridges')            

@login_required
def recharge_cartridge(request):
    
    try:
        errors = []
        update = cartridges.objects.get(id=request.POST.get('id', ''))
        
        if update.cilindro_drum + 1 <= update.numero_recarga_maxima:
            update.cilindro_drum = update.cilindro_drum + 1
        else: 
            errors.append('error') 
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Drum]')

        if update.rodillo_magnetico + 1 <= update.numero_recarga_maxima:
            update.rodillo_magnetico = update.rodillo_magnetico + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Rodillo magnetico]')

        if update.rodillo_carga + 1 <= update.numero_recarga_maxima:
            update.rodillo_carga = update.rodillo_carga + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Rodillo de carga]')

        if update.cuchilla_impiadora + 1 <= update.numero_recarga_maxima:
            update.cuchilla_impiadora = update.cuchilla_impiadora + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Cuchilla limpiadora]')    

        if update.cuchilla_dosificadora + 1 <= update.numero_recarga_maxima:
            update.cuchilla_dosificadora = update.cuchilla_dosificadora + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Cuchilla dosificadora]')        
        
            
        if not errors:
            update.fecha_ultimo_servcio = datetime.datetime.now()
            update.save()
            messages.add_message(request, messages.INFO, 'Cartucho ['  + request.POST.get('id','')+ '] recargado con exito')
            return redirect ('/list_cartridges')
        else:
            return redirect ('/list_cartridges')
            

    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_cartridges')
    
@login_required
def restore_cartridge(request):
    try:
        update = cartridges.objects.get(id=request.POST.get('id', ''))
        update.cilindro_drum = 1
        update.rodillo_magnetico = 1
        update.rodillo_carga = 1
        update.cuchilla_impiadora = 1
        update.cuchilla_dosificadora = 1
        update.save()
        
        messages.add_message(request, messages.INFO, 'Cartucho ['  + request.POST.get('id','')+ '] remanufacturado con exito')
        return redirect ('/list_cartridges')
        
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_cartridges')
        