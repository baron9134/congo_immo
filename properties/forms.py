from django import forms
from .models import Property, PropertyImage, Comment
from django.forms import modelformset_factory
from django.contrib.auth.models import User

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'address', 'city', 'price', 'description',
            'main_image', 'bedrooms', 'living_rooms',
            'has_water', 'has_electricity', 'phone_number'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['has_water', 'has_electricity']:
                field.required = True

            field.widget.attrs.update({
                'class': 'w-full p-2 border border-gray-300 rounded'
        })

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

from django import forms
from django.contrib.auth.models import User

class EditProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=False, label='Téléphone')
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
        label='Nouveau mot de passe',
        initial=''
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
        label='Confirmer le mot de passe',
        initial=''
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password')
        password2 = cleaned_data.get('confirm_new_password')

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Votre commentaire...'
            })
        }