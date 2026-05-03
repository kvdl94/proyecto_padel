from django import forms
from .models import Usuario, Pista

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("confirmar_password"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class PistaForm(forms.ModelForm):
    class Meta:
        model = Pista
        fields = ['nombre', 'imagen_url', 'activa']
        labels = {
            'nombre': 'Nombre de la pista',
            'imagen_url': 'URL de la imagen (opcional)',
            'activa': 'Pista activa',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control'}),
        }