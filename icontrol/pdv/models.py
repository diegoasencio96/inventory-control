# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from store.models import ProductStore
from django.db.models import Sum
from django.utils import timezone


class Invoice(models.Model):
    datetime = models.DateTimeField(verbose_name='Fecha y hora', default=timezone.now)
    seller = models.ForeignKey(User, verbose_name='Vendedor(a)', related_name='invoice_seller', null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductStore, through='InvoiceDetail', blank=True)
    total_price = models.FloatField(verbose_name='Precio Total', null=True, blank=True)

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'

    def __str__(self):
        return '{}'.format(self.datetime)

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, verbose_name='Factura', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductStore, verbose_name='Producto', on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Cantidad', default=1)
    price = models.FloatField(verbose_name='Precio', null=True, blank=True)

    # subtotal
    # total

    class Meta:
        verbose_name = 'Detalle de la venta'
        verbose_name_plural = 'Detalles de las ventas'
        unique_together = ['id', 'invoice']

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.invoice, self.product, self.quantity, self.price)
