from django import forms

from .models import Category


class CategoryAdminForm(forms.ModelForm):
    background_color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))

    class Meta:
        model = Category
        fields = '__all__'
