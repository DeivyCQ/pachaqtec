from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Programa(models.Model):
    id = models.AutoField(primary_key = True)
    nombre_programa = models.CharField(max_length=200, blank=False, null=False)
    descripcion_programa = models.TextField(blank=False, null=False)
    portada = models.ImageField(upload_to='images/programas', max_length=255)
    slug = models.CharField(max_length=50, blank=True, null=False)
    estado = models.BooleanField()
    precio = models.IntegerField()

    class Meta:
        db_table = 'Programas'
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
    
    def __str__(self):
        return self.nombre_programa

class Horario(models.Model):
    id = models.AutoField(primary_key = True)
    dias = models.CharField(max_length = 100)
    horario = models.CharField(max_length = 100)
    programa = models.ForeignKey('Programa', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
    
    def __str__(self):
        return self.dias + ' ' + self.horario

class Unidad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre_unidad = models.CharField(max_length = 100)
    programa = models.ForeignKey('Programa', on_delete= models.CASCADE)

    class Meta:
        verbose_name = 'Unidad'
        verbose_name_plural = 'Unidades'
    
    def __str__(self):
        return self.nombre_unidad

class Semana(models.Model):
    id = models.AutoField(primary_key = True)
    nombre_semana = models.CharField(max_length = 50)
    tema = models.CharField(max_length = 50)
    descripcion = models.TextField(blank=False, null=False)            
    unidad = models.ForeignKey('Unidad', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Semana'
        verbose_name_plural = 'Semanas'
    
    def __str__(self):
        return self.nombre_semana


class Postulante(models.Model):
    id = models.AutoField(primary_key = True)
    nombre_postulante = models.CharField(max_length = 100)
    celular = models.CharField(max_length = 12)
    correo = models.EmailField(max_length = 100)
    programa = models.ForeignKey('Programa', on_delete = models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Postulantes'
        verbose_name = 'Postulante'
        verbose_name_plural = 'Postulantes'
    
    def __str__(self):
        return self.nombre_postulante
    
class Cupon(models.Model):
    id = models.AutoField(primary_key = True)
    codigo_cupon = models.CharField(max_length= 10)
    porcentaje_descuento = models.FloatField()
    fecha_fin = models.DateField()
    en_uso = models.BooleanField()

    class Meta:
        verbose_name = 'Cupón'
        verbose_name_plural = 'Cupones'
    
    def __str__(self):
        return self.codigo_cupon

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_venta = models.DateField(auto_now_add=True)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    subtotal = models.FloatField()
    cupon = models.ForeignKey('Cupon', on_delete=models.SET_NULL, blank=True, null=True)
    total = models.FloatField()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return self.id
    
class Detalle_Venta(models.Model):
    id = models.AutoField(primary_key = True)
    venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    programa = models.ForeignKey('Programa', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalle Ventas'

    def __str__(self):
        return self.id

class Matricula(models.Model):
    id = models.AutoField(primary_key = True)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    programa = models.ForeignKey('Programa', on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'

    def __str__(self):
        return self.id