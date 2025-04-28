from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Organizacao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizacao', null=True)
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Voluntario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='voluntario', null=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Oportunidade(models.Model):
    organizacao = models.ForeignKey(Organizacao, on_delete=models.CASCADE, related_name='oportunidades')
    titulo = models.CharField(max_length=255, default='Sem título')
    descricao = models.TextField()
    data = models.DateField(default=timezone.now)
    local = models.TextField()
    quantidade_vagas = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.organizacao.nome}"

class Inscricao(models.Model):
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, related_name='inscricoes')
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ], default='pendente')
    mensagem = models.TextField(blank=True, null=True)
    curriculo = models.FileField(upload_to='curriculos/', blank=True, null=True)

    class Meta:
        unique_together = ['oportunidade', 'voluntario']

    def __str__(self):
        return f"{self.voluntario.nome} - {self.oportunidade.titulo}"

class Feedback(models.Model):
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks_dados')
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE, related_name='feedbacks_recebidos')
    oportunidade = models.ForeignKey(Oportunidade, on_delete=models.CASCADE, related_name='feedbacks')
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    descricao = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['colaborador', 'voluntario', 'oportunidade']

    def __str__(self):
        return f"Feedback de {self.colaborador.username} para {self.voluntario.nome}"
