from django import forms
from .models import Property, PropertyImage
from django.forms import modelformset_factory

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'address', 'city', 'price', 'description',
            'main_image', 'bedrooms', 'living_rooms',
            'has_water', 'has_electricity', 'phone_number','owner'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

PropertyImageFormSet = modelformset_factory(
    PropertyImage,
    form=PropertyImageForm,
    extra=3,  # ou plus
    max_num=10,
    can_delete=False
)

