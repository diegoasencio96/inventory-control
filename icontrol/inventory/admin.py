from django.contrib import admin
from django.utils.html import format_html
from django_mptt_admin.admin import DjangoMpttAdmin
from suit.sortables import SortableModelAdmin, SortableTabularInline, SortableStackedInline
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from inventory.models import IngredientProduct, IngredientProductCategory, IngredientProductProvider
from utils.image_utils import ImagePreview
from inventory.forms import IngredientProductCategoryForm, IngredientProductForm


# Register your models here.


@admin.register(IngredientProductCategory)
class IngredientProductCategoryAdmin(DjangoMpttAdmin, ImagePreview):
    form = IngredientProductCategoryForm
    list_display = ['get_image_thumb_preview', 'name', 'parent', 'active']
    fields = ['active', 'parent', 'image', 'get_image_preview', 'name']
    search_fields = ['name', 'parent__name']
    readonly_fields = ('get_image_preview',)
    # autocomplete_fields = ['parent']


@admin.register(IngredientProductProvider)
class IngredientProductProviderAdmin(admin.ModelAdmin, ImagePreview):
    list_display = ['get_image_thumb_preview', 'name', 'cc_nit', 'phone', 'cellphone', 'email', 'address', 'active']
    fields = ['active', 'image', 'get_image_preview', 'name', 'cc_nit', 'phone', 'cellphone', 'email', 'address']
    search_fields = ['name', 'phone', 'email', 'cc_nit']
    readonly_fields = ('get_image_preview',)


@admin.register(IngredientProduct)
class IngredientProductAdmin(admin.ModelAdmin, SortableAdminMixin, ImagePreview):
    form = IngredientProductForm
    search_fields = ['name', 'description', 'category__name', 'provider__name']
    list_filter = ['category', 'provider', 'active']
    list_display = ['get_image_thumb_preview', 'name', 'category', 'provider',
                    'stock', 'active']
    fields = ['active', 'category', 'image', 'get_image_preview', 'name', 'description',
              'stock', 'provider']
    readonly_fields = ('get_image_preview',)
    autocomplete_fields = ['provider', 'category']

    def get_queryset(self, request):
        queryset = super(__class__, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset #.filter(user=request.user)
