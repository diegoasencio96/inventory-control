from django.urls import path
from pdv.views import save_bill, list_client

urlpatterns = [
    path('pdv/invoice/save', save_bill),
    path('pdv/client/list', list_client),
]
