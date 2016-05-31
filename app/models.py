from django.db import models

# Create your models here.
class clients(models.Model): 
    nombre = models.CharField(max_length=60) 
    empresa = models.CharField(max_length=60) 
    direccion = models.CharField(max_length=60) 
    telefono = models.CharField(max_length=60) 
    movil = models.CharField(max_length=60) 
    email = models.EmailField()

    def __str__(self): # __unicode__ en Python 2 
        return self.nombre 

class cartridges (models.Model):
	descripcion = models.TextField()
	cilindro_drum = models.IntegerField(null=True)
	rodillo_magnetico = models.IntegerField(null=True)
	rodillo_carga = models.IntegerField(null=True)
	cuchilla_impiadora = models.IntegerField(null=True)
	cuchilla_dosificadora = models.IntegerField(null=True)
	observaciones = models.TextField()
	numero_recarga_maxima = models.IntegerField()
	fecha_ultimo_servcio = models.DateField(null=True)
	modelo = models.CharField(max_length=60) 
	modelo_imp = models.CharField(max_length=60) 
	client = models.ForeignKey(clients)