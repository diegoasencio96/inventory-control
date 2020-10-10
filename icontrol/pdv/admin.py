from django.contrib import admin
from django.urls import path
from .models import Invoice, InvoiceDetail
from store.models import ProductStore, ProductCategory
from django.template.response import TemplateResponse
import json


class InvoiceDetailInline(admin.TabularInline):
    extra = 0
    model = Invoice.products.through
    raw_id_fields = ['product', ]
    # readonly_fields = ['product', 'price', 'quantity']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ['datetime', ]
    list_display = ['datetime', ]
    inlines = [InvoiceDetailInline]
    # readonly_fields = ['datetime', 'total_price', 'seller']

    # def has_add_permission(self, request):
    #    return request.user.groups.filter(name='Developers').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def add_form(self, request):
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else we want in the context...
        )
        categories = ProductCategory.objects.filter(active=True, parent=None).values('id', 'name')
        result1_list = []
        for category in categories:
            subcategories = ProductCategory.objects.filter(active=True, parent=category.get('id')).values('id', 'name')
            result2_list = []
            for subcategory in subcategories:
                products = ProductStore.objects.filter(active=True, category=subcategory.get('id')).values('id', 'name', 'price', 'description', 'image')
                subcategory['products'] = list(products)
                result2_list.append(subcategory)
            category['subcategories'] = result2_list
            result1_list.append(category)
        context['data'] = result1_list

        return TemplateResponse(request, "admin/new-invoice.html", context)

    def get_urls(self):
        urls = super(InvoiceAdmin, self).get_urls()
        my_urls = [path('add/', self.admin_site.admin_view(self.add_form), name="new-invoice")]
        return my_urls + urls

    def save_model(self, request, obj, form, change):
        # Code Logic
        obj.save()
