from django import forms
from store.models import ProductStore, ProductCategory


class ProductStoreForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductStoreForm, self).__init__(*args, **kwargs)  # populates the post
        if self.fields:
            self.fields['category'].queryset = ProductCategory.objects.filter(active=True, parent__isnull=False)  # results

    class Meta:
        model = ProductStore
        fields = '__all__'


class ProductCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCategoryForm, self).__init__(*args, **kwargs)  # populates the post
        if self.fields:
            self.fields['parent'].queryset = ProductCategory.objects.filter(active=True, parent__isnull=True)  # results

    class Meta:
        model = ProductCategory
        fields = '__all__'
