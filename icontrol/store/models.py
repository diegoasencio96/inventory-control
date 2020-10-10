from django.db import models

# Create your models here.

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
from inventory.models import IngredientProduct


class ProductCategory(MPTTModel):
    id = models.AutoField(primary_key=True)
    order = models.PositiveIntegerField(verbose_name='Orden de la categoría', default=0, blank=False, null=False)
    active = models.BooleanField(default=True, verbose_name='¿Categoría Activa?')
    image = models.ImageField(verbose_name='Imagen de la categoría', upload_to='{}'.format('products_categories'))
    name = models.CharField(max_length=80, unique=True, verbose_name='Nombre de la categoría')
    parent = TreeForeignKey('self', verbose_name='Categoría de producto padre', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')

    class Meta:
        ordering = ['order']
        verbose_name = 'Categoría del producto'
        verbose_name_plural = 'Categorías de productos'

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(ProductCategory, self).save(*args, **kwargs)
        ProductCategory.objects.rebuild()

    def __str__(self):
        return '{}'.format(self.name)


class ProductStore(models.Model):
    id = models.AutoField(primary_key=True)
    active = models.BooleanField(verbose_name='¿Producto Activo?', default=True)
    category = models.ForeignKey(ProductCategory, verbose_name='Categoría a la que pertenece', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Imagen del producto', upload_to='{}'.format('products'))
    name = models.CharField(max_length=180, verbose_name='Nombre')
    description = models.TextField(max_length=480, verbose_name='Descripción')
    barcode = models.CharField(max_length=60, verbose_name='Código de barras', blank=True)
    price = models.BigIntegerField(verbose_name='Precio')
    discount = models.FloatField(verbose_name='Descuento (%)', default=0.0)
    ingredients = models.ManyToManyField(
        IngredientProduct, verbose_name='Ingredientes', through='IngredientOfProductStore', related_name='ingredients',
    )
    order = models.PositiveIntegerField(verbose_name='Orden del producto', default=0, blank=False, null=False)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['order']

    def save(self, *args, **kwargs):
        super(ProductStore, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)


class IngredientOfProductStore(models.Model):
    product = models.ForeignKey(ProductStore, related_name='ingredients_of_products', on_delete=models.CASCADE)
    ingredient_product = models.ForeignKey(
        IngredientProduct, related_name='ingredients_of_products', verbose_name='Ingrediente', on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name='Cantidad', default=1)

    def __str__(self):
        return "%s - %s (%s cantidad)" % (self.product, self.ingredient_product, self.quantity)

    class Meta:
        unique_together = ('product', 'ingredient_product',)
        verbose_name = 'Ingrediente del producto'
        verbose_name_plural = 'Ingredientes de los Productos'
