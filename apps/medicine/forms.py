from django import forms

from .models import Category, ProductImage


class CategoryAdminForm(forms.ModelForm):
    background_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = Category
        fields = '__all__'


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']  # Здесь укажите поле для изображения, если оно у вас в модели

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False
