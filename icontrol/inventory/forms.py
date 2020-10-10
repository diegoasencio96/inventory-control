from django import forms
from .models import IngredientProduct, IngredientProductCategory, IngredientProductProvider


class IngredientProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IngredientProductForm, self).__init__(*args, **kwargs)  # populates the post
        if self.fields:
            self.fields['provider'].queryset = IngredientProductProvider.objects.filter(active=True)  # results
            self.fields['category'].queryset = IngredientProductCategory.objects.filter(active=True) #, parent__isnull=False)  # results

    class Meta:
        model = IngredientProduct
        fields = '__all__'


class IngredientProductCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(IngredientProductCategoryForm, self).__init__(*args, **kwargs)  # populates the post
        if self.fields:
            self.fields['parent'].queryset = IngredientProductCategory.objects.filter(active=True) #, parent__isnull=True)  # results

    class Meta:
        model = IngredientProductCategory
        fields = '__all__'
