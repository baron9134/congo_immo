from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requis.')
    phone_number = forms.CharField(max_length=20, required=False, help_text='Numéro de téléphone')
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Sauvegarde du profil
            phone = self.cleaned_data['phone_number']
            UserProfile.objects.create(user=user, phone_number=phone)
        return user
