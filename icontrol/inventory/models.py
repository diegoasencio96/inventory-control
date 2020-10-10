from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


class IngredientProductCategory(MPTTModel):
    id = models.AutoField(primary_key=True)
    order = models.PositiveIntegerField(verbose_name='Orden de la categoría', default=0, blank=False, null=False)
    active = models.BooleanField(default=True, verbose_name='¿Categoría Activa?')
    image = models.ImageField(
        verbose_name='Imagen de la categoría', upload_to='{}'.format('ingredient_products_categories')
    )
    name = models.CharField(max_length=80, unique=True, verbose_name='Nombre de la categoría')
    parent = TreeForeignKey('self', verbose_name='Categoría padre', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    class Meta:
        ordering = ['order']
        verbose_name = 'Categoría del producto ingrediente'
        verbose_name_plural = 'Categorías de productos ingredientes'

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(IngredientProductCategory, self).save(*args, **kwargs)
        IngredientProductCategory.objects.rebuild()

    def __str__(self):
        return '{}'.format(self.name)


class IngredientProductProvider(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(default=True, verbose_name='¿Proveedor Activo?')
    image = models.ImageField(verbose_name='Imagen del proveedor', upload_to='{}'.format('products_providers'))
    name = models.CharField(max_length=80, verbose_name='Nombre del proveedor')
    cc_nit = models.CharField(max_length=40, verbose_name='C.C o NIT', unique=True)
    phone = models.CharField(max_length=10, verbose_name='Telefono (fijo)', blank=True)
    cellphone = models.CharField(max_length=10, verbose_name='Telefono (celular)', blank=True)
    email = models.EmailField(max_length=30, verbose_name='Correo electrónico', blank=True)
    address = models.CharField(max_length=40, verbose_name='Dirección', blank=True)

    class Meta:
        verbose_name = 'Proveedor del ingrediente'
        verbose_name_plural = 'Proveedores de los ingredientes'

    def __str__(self):
        return '{}'.format(self.name)


class IngredientProduct(models.Model):
    UNITS = [
        ('U', 'Unidad(es)'),
        ('P', 'Porción(es)'),
    ]
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(verbose_name='¿Ingrediente Activo?', default=True)
    image = models.ImageField(verbose_name='Imagen del producto', upload_to='{}'.format('products'))
    provider = models.ForeignKey(IngredientProductProvider, verbose_name='Proveedor del Ingrediente', null=True, blank=True,
                                 on_delete=models.CASCADE)
    category = models.ForeignKey(IngredientProductCategory, verbose_name='Categoría a la que pertenece', on_delete=models.CASCADE)
    name = models.CharField(max_length=180, verbose_name='Nombre')
    description = models.TextField(max_length=480, verbose_name='Descripción', blank=True)
    stock = models.PositiveIntegerField(verbose_name='Cantidad en inventario', default=1)
    unit = models.CharField(verbose_name='Unidad', max_length=20, choices=UNITS)
    order = models.PositiveIntegerField(verbose_name='Orden del ingrediente', default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Producto ingrediente'
        verbose_name_plural = 'Productos ingredientes'
        ordering = ['order']

    def save(self, *args, **kwargs):
        super(IngredientProduct, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)
