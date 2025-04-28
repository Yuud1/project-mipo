from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Voluntario, Organizacao, Oportunidade, Inscricao

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=[('voluntario', 'Voluntário'), ('organizacao', 'Organização')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class VoluntarioRegistrationForm(forms.ModelForm):
    class Meta:
        model = Voluntario
        fields = ['nome', 'telefone', 'endereco', 'foto']
        exclude = ['user', 'email', 'data_cadastro']

class OrganizacaoRegistrationForm(forms.ModelForm):
    class Meta:
        model = Organizacao
        fields = ['nome', 'tipo', 'telefone', 'endereco', 'foto']
        exclude = ['user', 'email', 'data_cadastro']

class OportunidadeForm(forms.ModelForm):
    class Meta:
        model = Oportunidade
        fields = ['titulo', 'descricao', 'data', 'local', 'quantidade_vagas']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'descricao': forms.Textarea(attrs={'rows': 4}),
        }

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['mensagem', 'curriculo']
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Deixe uma mensagem para a instituição (opcional)...'}),
        }
