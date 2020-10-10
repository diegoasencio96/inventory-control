from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import json
from django.db import transaction

from inventory.models import IngredientProduct
from store.models import IngredientOfProductStore
from .models import Invoice, ProductStore, InvoiceDetail
from utils import datetime_utils as datetime
# Create your views here.


@staff_member_required
def save_bill(request):
    if request.is_ajax():
        print('[+] Guardando venta ...')
        data = request.body.decode('utf-8')
        data_json = json.loads(data)

        products = data_json['products']
        print(products)
        if 1:
            with transaction.atomic():
                try:
                    bill = Invoice(datetime=datetime.now(), seller=request.user, total_price=0)
                    bill.save()
                    invoice = bill.pk
                    total_price = 0
                    for key in products:
                        product = products[key]
                        total_price += product['quantity'] * float(product['price'])

                        bill_detail = InvoiceDetail(
                            invoice_id=invoice,
                            product_id=product['id'],
                            quantity=product['quantity'],
                            price=product['price']
                        )
                        bill_detail.save()
                        ingredients = bill_detail.product.ingredients.all()
                        for ingredient in ingredients:
                            ingredient_of_product = IngredientOfProductStore.objects.get(
                                product__id=bill_detail.product_id,
                                ingredient_product__id=ingredient.id
                            )
                            ingredient.stock = ingredient.stock - product['quantity'] * ingredient_of_product.quantity
                            ingredient.save()
                    bill.total_price = total_price
                    bill.save()
                except:
                    print("[-] Error !!! -> Save invoice")
                    error = {"error": "Error, no se guardo la venta :S"}
                    return HttpResponse(json.dumps(error))
        success = {"success": "¡Venta Registrada!"}
        return HttpResponse(json.dumps(success))
    else:
        print('[!] Get Method Not Support ...')
        return HttpResponse("No se pudo guardar la venta")


@staff_member_required
def print_bill(request):
    if request.method == 'GET':
        print('[+] Imprimiendo venta ...')
    else:
        print('[!] Get Method Not Support ...')
    return HttpResponse("HTTP REQUEST")


@staff_member_required
def send_bill(request):
    if request.method == 'GET':
        print('[+] Enviando venta ...')
    else:
        print('[!] Get Method Not Support ...')
    return HttpResponse("HTTP REQUEST")


@staff_member_required
def list_client(request):
    if request.is_ajax():
        print('[+] Consultando clientes ...')
        clients = []
        for client in User.objects.filter(is_active=True, ):
            clients.append('{}-{}'.format(client.first_name, client.last_name))
        clients_dict = {'clients': clients}
        return HttpResponse(json.dumps(clients_dict))
    else:
        print('[!] Get Method Not Support ...')
    return HttpResponse("HTTP REQUEST")