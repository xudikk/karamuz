from django import forms
from core.models import Category, New


class CtgForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class NewsForm(forms.ModelForm):
    class Meta:
        model = New
        exclude = ['view', "created", "updated"]













