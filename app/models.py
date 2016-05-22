from django.db import models

# Create your models here.
class clients(models.Model): 
    nombre = models.CharField(max_length=60) 
    empresa = models.CharField(max_length=60) 
    direccion = models.CharField(max_length=60) 
    telefono = models.CharField(max_length=60) 
    movil = models.CharField(max_length=60) 
    email = models.EmailField()

