from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)
        labels = {
            'username': 'Nome de Usuário',
        }
        help_texts = {
            'username': 'Obrigatório. Máximo de 150 caracteres. Somente letras, números e @/./+/-/_',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Traduzindo as labels de senha manualmente
        self.fields['password1'].label = "Senha"
        self.fields['password1'].help_text = "Sua senha deve ter pelo menos 8 caracteres e não pode ser muito comum."
        self.fields['password2'].label = "Confirmação de Senha"
        self.fields['password2'].help_text = "Digite a mesma senha de antes para confirmar."