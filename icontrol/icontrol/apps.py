from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem
from django.utils.translation import ugettext_lazy as _


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
    menu = (
        ParentItem(_('Usuarios del sistema'), children=[
            ChildItem(model='auth.user'),
            ChildItem(model='auth.group'),
        ], icon='fa fa-users'),
        ParentItem(_('Tienda'), children=[
            ChildItem(model='store.productcategory'),
            ChildItem(model='store.productstore'),
        ], icon='fa fa-shopping-cart'),
        ParentItem(_('Inventario'), children=[
            ChildItem(model='inventory.ingredientproductprovider'),
            ChildItem(model='inventory.ingredientproductcategory'),
            ChildItem(model='inventory.ingredientproduct'),
        ], icon='fa fa-book'),
        ParentItem(_('Punto de Venta'), children=[
            ChildItem(model='pdv.invoice'),
            ChildItem(model='pdv.newinvoice'),
        ], icon='fa fa-credit-card'),
    )
