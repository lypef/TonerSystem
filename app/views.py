from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from models import clients, cartridges, logs

# Create your views here.
def login(request): 

    if request.user.is_authenticated():
    	return render(request,'manage.html')
    return render(request,'login.html')

@login_required
def manage(request):
    Llogs = logs.objects.all().order_by('-id')

    paginator = Paginator(Llogs, 9) # Show 25 contacts per page

    page = request.GET.get('page')
    
    try:
        Llogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        Llogs = paginator.page(1)
    except EmptyPage:
        # If page is out osf range (e.g. 9999), deliver last page of results.
        Llogs = paginator.page(paginator.num_pages)
    
    return render(request,'manage.html',{'Llogs':Llogs,'page_range':paginator.page_range,'count':paginator.num_pages})

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
                add_log('se creo cliente [' + str(insert.nombre) + '] con id ('+str(insert.id)+'), empresa ('+str(insert.empresa)+'), direccion ('+str(insert.direccion)+'), telefono ('+str(insert.telefono)+'), movil ('+str(insert.movil)+'), email ('+str(insert.email)+').')
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
        Llclients = clients.objects.filter(nombre__contains=request.POST.get('search', '').upper()).order_by('nombre')
            
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

    return render (request,'list_clients.html',{'Lclients':Lclients,'page_range':paginator.page_range,'count':paginator.num_pages})

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
        vartmp = 'se edito el cliente con id ('+str(update.id)+'). nombre ['+str(update.nombre)+'] , empresa ('+str(update.empresa)+'), direccion ('+str(update.direccion)+'), telefono ('+str(update.telefono)+'), movil ('+str(update.movil)+'), email ('+str(update.email)+')'
        update.save()
        vartmp += ' por nombre ['+str(update.nombre)+'] , empresa ('+str(update.empresa)+'), direccion ('+str(update.direccion)+'), telefono ('+str(update.telefono)+'), movil ('+str(update.movil)+'), email ('+str(update.email)+')'
        add_log(vartmp)
        messages.add_message(request, messages.INFO, 'Cliente editado con exito')
        return redirect ('/list_clients') 
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_clients') 
    
@login_required
def list_clients_delete(request):
    try:
        delete = clients.objects.get(id= request.POST.get('id',''))
        add_log('se elimino el cliente ['+str(delete.nombre)+'] con id('+str(delete.id)+')')
        delete.delete()
        messages.add_message(request, messages.INFO, 'Cliente eliminado con exito')
        return redirect ('/list_clients')        

    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_clients')        
    
@login_required
def newcartridges(request):
    Lclients = clients.objects.all().order_by('nombre')
    
    if request.method == 'GET':
        return render(request, 'newcartridges.html',{'Lclients': Lclients,})

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
                add_log('se agrego cartucho con id ('+str(insert.id)+') y cliente ['+str(insert.client.nombre)+']')
                messages.add_message(request, messages.INFO, 'Cartucho agregado con exito')
                return redirect('/list_cartridges')
            except Exception, e:
                messages.add_message(request, messages.INFO, e)

        if  request.POST.get('cliente', '').isdigit() == True:
            return render(request, 'newcartridges.html', {
        'modelo_impresora': request.POST.get('modelo_impresora', ''),
        'modelo_toner': request.POST.get('modelo_toner', ''),
        'numero_recarga': request.POST.get('numero_recarga', ''),
        'descripcion': request.POST.get('descripcion', ''),
        'observaciones': request.POST.get('observaciones', ''),
        'Lclients': Lclients, 
        'idclient': clients.objects.get(id=request.POST.get('cliente', '')).id 
        }) 
        else:
            return render(request, 'newcartridges.html', {
        'modelo_impresora': request.POST.get('modelo_impresora', ''),
        'modelo_toner': request.POST.get('modelo_toner', ''),
        'numero_recarga': request.POST.get('numero_recarga', ''),
        'descripcion': request.POST.get('descripcion', ''),
        'observaciones': request.POST.get('observaciones', ''),
        'Lclients': Lclients
        })


@login_required
def list_cartridges(request):
    Lclients = clients.objects.all().order_by('nombre')

    if request.method == "GET":
        Lcartridges = cartridges.objects.all().order_by('-id')   
    if request.method == "POST":
        Lcartridges = cartridges.objects.filter(id__contains=request.POST.get('code', '')).order_by('id')
            
    paginator = Paginator(Lcartridges, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        Lcartridges = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        Llcartridges = paginator.page(1)
    except EmptyPage:
        # If page is out osf range (e.g. 9999), deliver last page of results.
        Lcartridges = paginator.page(paginator.num_pages)

    return render (request,'list_cartridges.html',{'Lclients':Lcartridges, 'Lclients0': Lclients,'page_range':paginator.page_range,'count':paginator.num_pages})

@login_required
def list_cartridges_id(request,id):
    Lclients = clients.objects.all().order_by('nombre')

    Lcartridges = cartridges.objects.filter(id=id).order_by('id')
    
    return render (request,'list_cartridges.html',{'Lclients':Lcartridges, 'Lclients0': Lclients})    

@login_required
def list_cartridges_edit(request):
    try:
        update = cartridges.objects.get(id=request.POST.get('id', ''))
        vartmp = 'se actualizo cartucho numero ['+str(update.id)+']: [numero r. maxima ('+str(update.numero_recarga_maxima)+'), cliente ('+str(update
                .client.nombre)+')]'
        update.modelo_imp = request.POST.get('modelo_impresora', '').upper()
        update.modelo = request.POST.get('modelo_toner', '').upper()
        update.numero_recarga_maxima = request.POST.get('numero_recarga', '').upper()
        update.client = clients.objects.get(id=request.POST.get('clientselect', ''))
        update.descripcion = request.POST.get('descripcion', '').upper()
        update.observaciones = request.POST.get('observaciones', '').upper()
        update.save()
        vartmp += ' por: [numero r. maxima ('+str(update.numero_recarga_maxima)+'), cliente ('+str(update
                .client.nombre)+')]'
        add_log(vartmp)
        messages.add_message(request, messages.INFO, 'Cartucho [' + request.POST.get('id', '') + '] editado con exito')
        return redirect (request.POST.get('url', '')) 
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect (request.POST.get('url', ''))     


@login_required
def list_cartridges_delete(request):
    try:
        delete = cartridges.objects.get(id= request.POST.get('id',''))
        vartmp = 'se elimina el cartucho numero: ('+str(delete.id)+'), cliente ['+str(delete.client.nombre)+']'
        delete.delete()
        add_log(vartmp)
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
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Drum] - Cartucho ['  + request.POST.get('id','')+ ']')

        if update.rodillo_magnetico + 1 <= update.numero_recarga_maxima:
            update.rodillo_magnetico = update.rodillo_magnetico + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Rodillo magnetico] - Cartucho ['  + request.POST.get('id','')+ ']')

        if update.rodillo_carga + 1 <= update.numero_recarga_maxima:
            update.rodillo_carga = update.rodillo_carga + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Rodillo de carga] - Cartucho ['  + request.POST.get('id','')+ ']')

        if update.cuchilla_impiadora + 1 <= update.numero_recarga_maxima:
            update.cuchilla_impiadora = update.cuchilla_impiadora + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Cuchilla limpiadora] - Cartucho ['  + request.POST.get('id','')+ ']')    

        if update.cuchilla_dosificadora + 1 <= update.numero_recarga_maxima:
            update.cuchilla_dosificadora = update.cuchilla_dosificadora + 1
        else:
            errors.append('error')  
            messages.add_message(request, messages.INFO, 'Es necesario cambiar [Cuchilla dosificadora] - Cartucho ['  + request.POST.get('id','')+ ']')        
        
            
        if not errors:
            update.fecha_ultimo_servcio = datetime.datetime.now()
            update.observaciones += "\n\n - SE REALIZO RECARGA DE TONER CON EXITO. " + str(datetime.datetime.now()) 
            update.save()
            add_log('se realiza recarga normal a cartucho numero: ('+str(update.id)+'), cliente ['+str(update.client.nombre)+']')
            messages.add_message(request, messages.INFO, 'Cartucho ['  + request.POST.get('id','')+ '] recargado con exito')
            return redirect ('/list_cartridges')
        else:
            return redirect (request.POST.get('url',''))
            

    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect (request.POST.get('url',''))
    
@login_required
def restore_cartridge(request):
    try:
        update = cartridges.objects.get(id=request.POST.get('id', ''))
        update.cilindro_drum = 1
        update.rodillo_magnetico = 1
        update.rodillo_carga = 1
        update.cuchilla_impiadora = 1
        update.cuchilla_dosificadora = 1
        update.descripcion = ""
        update.observaciones = " - SE REALIZO REMANUFACTURA Y RECARGA CON EXITO." + str(datetime.datetime.now()) 
        update.fecha_ultimo_servcio = datetime.datetime.now()
        update.save()
        add_log('se realiza remanufactura total a cartucho numero: ('+str(update.id)+'), cliente ['+str(update.client.nombre)+']')
        messages.add_message(request, messages.INFO, 'Cartucho ['  + request.POST.get('id','')+ '] remanufacturado con exito')
        return redirect (request.POST.get('url',''))
        
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect (request.POST.get('url',''))
        
@login_required
def list_cartridges_service_edit(request):
    try:
        update = cartridges.objects.get(id=request.POST.get('id', ''))
        vartmp = 'se realiza actualizacion de cartucho numero: ('+str(update.id)+'), [c- drum ('+str(update.cilindro_drum)+'), rodillo magnetico ('+str(update.rodillo_magnetico)+'), rodillo de carga ('+str(update.rodillo_carga)+'), c-limpiadora ('+str(update.cuchilla_impiadora)+'), c-dosificadora ('+str(update.cuchilla_dosificadora)+')]'
        update.cilindro_drum = request.POST.get('drum','')
        update.rodillo_magnetico = request.POST.get('rmagnetico','')
        update.rodillo_carga = request.POST.get('rcarga','')
        update.cuchilla_impiadora = request.POST.get('cclean','')
        update.cuchilla_dosificadora  = request.POST.get('cdosificadora','')
        update.observaciones = request.POST.get('observaciones','').upper() + ' ' +str(datetime.datetime.now()) 
        update.save()
        vartmp += ' por, [c- drum ('+str(update.cilindro_drum)+'), rodillo magnetico ('+str(update.rodillo_magnetico)+'), rodillo de carga ('+str(update.rodillo_carga)+'), c-limpiadora ('+str(update.cuchilla_impiadora)+'), c-dosificadora ('+str(update.cuchilla_dosificadora)+')]'
        add_log(vartmp)
        messages.add_message(request, messages.INFO, 'Cartucho [' + request.POST.get('id', '') + '] editado con exito')
        return redirect (request.POST.get('url', '')) 
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect (request.POST.get('url', ''))             


@login_required
def list_cartridges_clients(request, clientid):
    Lcartridges = cartridges.objects.filter(client=clientid)

    paginator = Paginator(Lcartridges, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        Lcartridges = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        Lcartridges = paginator.page(1)
    except EmptyPage:
        # If page is out osf range (e.g. 9999), deliver last page of results.
        Lcartridges = paginator.page(paginator.num_pages)


    return render (request,'list_cartridges_clients.html',
        {'Lcartridges':Lcartridges,'page_range':paginator.page_range,'count':paginator.num_pages})

@login_required
def change_cartridge(request):
    try:
        cvaciotmp = cartridges.objects.get(id=request.POST.get('cvacio', ''))
        cllenotmp = cartridges.objects.get(id=request.POST.get('clleno', ''))
        
        cvacio = cartridges.objects.get(id=cvaciotmp.id)
        cvacio.client = clients.objects.get(id=cllenotmp.client.id)
        cvacio.observaciones += '\n\nSE REALIZA CAMBIO POR CARTUCHO NUMERO [ '+str(cllenotmp.id)+' ] DE ( '+str(cllenotmp.client.nombre)+' ) - ' + str(datetime.datetime.now())

        clleno = cartridges.objects.get(id=cllenotmp.id)
        clleno.client = clients.objects.get(id=cvaciotmp.client.id)    
        clleno.observaciones += '\n\nSE REALIZA CAMBIO POR CARTUCHO NUMERO [ '+str(cvaciotmp.id)+' ] DE ( '+str(cvaciotmp.client.nombre)+' ) - ' + str(datetime.datetime.now())


        cvacio.save()
        clleno.save()


        vartmp = 'se realiza cambio de cartucho optimo. numero: ('+str(cvaciotmp.id)+'), cliente ['+str(cvaciotmp.client.nombre)+'] por cartucho vacio. numero: ('+str(cllenotmp.id)+'), cliente ['+str(cllenotmp.client.nombre)+']'
        cvacio.save()
        clleno.save()
        add_log(vartmp)

        messages.add_message(request, messages.INFO, 'Cartucho [ '+ request.POST.get('cvacio','') +' ] cambiado exitosamente.')
        return redirect ('/list_cartridges/'+ request.POST.get('cvacio','') +'/')
    except Exception, e:
        messages.add_message(request, messages.INFO, e)
        return redirect ('/list_cartridges')




def add_log(registrotxt):
    insert = logs(
        registro = registrotxt.upper(),
        fecha = datetime.datetime.now(),
        )
    insert.save()
    

