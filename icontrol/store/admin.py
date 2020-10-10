from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from store.models import ProductCategory, ProductStore, IngredientOfProductStore
from store.forms import ProductCategoryForm, ProductStoreForm
from utils.image_utils import ImagePreview
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


class IngredientsInline(admin.TabularInline):
    model = IngredientOfProductStore
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(DjangoMpttAdmin, ImagePreview):
    form = ProductCategoryForm
    list_display = ['get_image_thumb_preview', 'name', 'parent', 'active']
    fields = ['active', 'parent', 'image', 'get_image_preview', 'name']
    search_fields = ['name', 'parent__name']
    readonly_fields = ('get_image_preview',)


@admin.register(ProductStore)
class ProductStoreAdmin(admin.ModelAdmin, SortableAdminMixin, ImagePreview):
    form = ProductStoreForm
    search_fields = ['barcode', 'name', 'description', 'category__name']
    list_filter = ['category', 'active']
    list_display = ['get_image_thumb_preview', 'name', 'category', 'price', 'discount', 'active']
    fields = ['active', 'category', 'image', 'get_image_preview', 'price', 'discount', 'name', 'description', 'barcode']
    readonly_fields = ('get_image_preview',)
    autocomplete_fields = ['category']
    inlines = (IngredientsInline, )

    def get_queryset(self, request):
        queryset = super(__class__, self).get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset #.filter(user=request.user)
