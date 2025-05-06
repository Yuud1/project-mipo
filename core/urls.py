from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('inscricoes/', views.inscricoes, name='inscricoes'),
    path('criar_oportunidade/', views.criar_oportunidade, name='criar_oportunidade'),
    path('oportunidade/<int:oportunidade_id>/', views.detalhe_oportunidade, name='detalhe_oportunidade'),
    path('oportunidade/<int:oportunidade_id>/inscrever/', views.inscrever_oportunidade, name='inscrever_oportunidade'),
    path('inscricao/<int:inscricao_id>/status/<str:novo_status>/', views.atualizar_status_inscricao, name='atualizar_status_inscricao'),
    path('inscricao/<int:inscricao_id>/feedback/', views.dar_feedback, name='dar_feedback'),
    path('certificados/', views.certificados, name='certificados'),
]
