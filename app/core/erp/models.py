from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import generos
from core.models import BaseModel


class Area(models.Model):
    nombre_area = models.CharField(max_length=150, unique=True, null=True, verbose_name='area')


    def __str__(self):
        return self.nombre_area
        
    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['id']


class Bodega(models.Model):
    nombre_bodega = models.CharField(max_length=150, unique=True, null=True, verbose_name='bodega')

    def __str__(self):
        return self.nombre_bodega

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['id']

class Tipo_Contrato(models.Model):
    tipo_contrato = models.CharField(max_length=150, unique=True, null=True, verbose_name='tipo_contrato')

    def __str__(self):
        return self.tipo_contrato

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo_Contrato'
        verbose_name_plural = 'Tipos_Contratos'
        ordering = ['id']

class Puesto(models.Model):
    puesto = models.CharField(max_length=150, unique=True, null=True, verbose_name='puesto')

    def __str__(self):
        return self.puesto

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Puesto'
        verbose_name_plural = 'Puestos'
        ordering = ['id']

class Empleado(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    dpi = models.CharField(max_length=15, unique=True, verbose_name='DPI')
    fecha_nacimiento = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=150, null=True, blank=True, verbose_name='Teléfono')
    genero = models.CharField(max_length=10, choices=generos, default='male', verbose_name='Sexo')
    foto = models.ImageField(upload_to='Empleado/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['genero'] = {'id': self.genero, 'name': self.get_genero_display()}
        item['foto'] = self.get_image()
        item['fecha_nacimiento'] = self.fecha_nacimiento.strftime('%Y-%m-%d')
        return item

    def get_image(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL, self.foto)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['id']

class Contrato(models.Model):
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha de ingreso')
    tipo = models.ForeignKey(Tipo_Contrato, on_delete=models.CASCADE, verbose_name='Tipo_Contrato')
    puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE, verbose_name='Puesto')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='Empleado')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name='Empleado')
    fecha_inicio = models.DateField(default=datetime.now, verbose_name='Fecha de inicio')
    salario_base = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    salario_bonificacion = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.tipo

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['tipo'] = self.tipo.toJSON()
        item['puesto'] = self.puesto.toJSON()
        item['empleado'] = self.empleado.toJSON()
        item['area'] = self.area.toJSON()
        item['fecha_inicio'] = self.fecha_inicio.strftime('%Y-%m-%d')
        item['salario_base'] = format(self.salario_base, '.2f')
        item['salario_bonificacion'] = format(self.salario_bonificacion, '.2f')
        return item

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['id']


# indicadores

class Indicador(models.Model):
    nombre_indicador = models.CharField(max_length=150, unique=True, null=True, verbose_name='indicador')

    def __str__(self):
        return self.nombre_indicador

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        ordering = ['id']


class Ingreso_Indicadores(models.Model):
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha de ingreso')
    indicador = models.ForeignKey(Indicador, on_delete=models.CASCADE, verbose_name='Indicador')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name='Empleado')
    valor = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.indicador

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['indicador'] = self.indicador.toJSON()
        item['empleado'] = self.empleado.toJSON()
        item['valor'] = format(self.valor, '.2f')
        return item

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ['id']



# productos

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=150, unique=True, null=True, verbose_name='categoria')

    def __str__(self):
        return self.nombre_categoria

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Producto(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['image'] = self.get_image()
        item['precio'] = format(self.precio, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


# Clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellidos = models.CharField(max_length=150, verbose_name='Apellidos')
    nit = models.CharField(max_length=10, unique=True, verbose_name='nit')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    telefono = models.CharField(max_length=150, null=True, blank=True, verbose_name='Teléfono')

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


# pedidos
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cliente.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detpedido_set.all()]
        return item

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']

class DetPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item


    class Meta:
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalle de pedidos'
        ordering = ['id']


# ventas
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def __str__(self):
        return self.cliente.nombre

    def toJSON(self):
        item = model_to_dict(self)
        item['cliente'] = self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')

        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detventas_set.all()]
        return item


    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']


class DetVentas(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['venta'])
        item['prod'] = self.prod.toJSON()
        item['precio'] = format(self.precio, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalle de pedidos'
        ordering = ['id']
