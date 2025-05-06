from django.shortcuts import render, redirect, get_object_or_404
from .models import Oportunidade, Inscricao, Voluntario, Organizacao, Feedback, Certificado
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from .forms import OportunidadeForm, UserRegistrationForm, VoluntarioRegistrationForm, OrganizacaoRegistrationForm, InscricaoForm, FeedbackForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

@login_required
def inscricoes(request):
    """Página de atividades do usuário (oportunidades para organizações, inscrições para voluntários)"""
    if hasattr(request.user, 'organizacao'):
        # Organização: mostrar suas oportunidades
        oportunidades = Oportunidade.objects.filter(organizacao=request.user.organizacao).order_by('-data_cadastro')
        contexto = {
            'is_organizacao': True,
            'oportunidades': oportunidades,
        }
    else:
        # Voluntário: mostrar inscrições feitas
        voluntario = request.user.voluntario
        inscricoes = Inscricao.objects.filter(voluntario=voluntario).order_by('-data_inscricao')
        contexto = {
            'is_organizacao': False,
            'inscricoes': inscricoes,
        }
    return render(request, 'core/inscricoes.html', contexto)

from .forms import OportunidadeForm

@login_required
def criar_oportunidade(request):
    if request.method == 'POST':
        form = OportunidadeForm(request.POST)
        if form.is_valid():
            oportunidade = form.save(commit=False)
            oportunidade.organizacao = request.user.organizacao  # Pega organizacao logada
            oportunidade.save()
            return redirect('inscricoes')
    else:
        form = OportunidadeForm()
    return render(request, 'core/criar_oportunidade.html', {'form': form})

def home(request):
    """Página inicial do site"""
    oportunidades = Oportunidade.objects.all().order_by('-data_cadastro')
    ultimas_vagas = oportunidades[:3]
    vagas_antigas = oportunidades[3:]
    return render(request, 'core/home.html', {
        'ultimas_vagas': ultimas_vagas,
        'vagas_antigas': vagas_antigas
    })

def register(request):
    """Página de registro de usuário"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        user_type = request.POST.get('user_type')
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']
            user.save()
            
            if user_type == 'voluntario':
                voluntario = Voluntario.objects.create(
                    user=user,
                    nome=request.POST.get('nome'),
                    email=user.email,
                    telefone=request.POST.get('telefone'),
                    endereco=request.POST.get('endereco')
                )
                messages.success(request, 'Voluntário registrado com sucesso!')
            else:
                organizacao = Organizacao.objects.create(
                    user=user,
                    nome=request.POST.get('nome_org'),
                    email=user.email,
                    tipo=request.POST.get('tipo'),
                    telefone=request.POST.get('telefone_org'),
                    endereco=request.POST.get('endereco_org')
                )
                messages.success(request, 'Organização registrada com sucesso!')
            
            return redirect('login')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'core/register.html', {
        'user_form': user_form
    })

@login_required
def perfil(request):
    """Página de perfil do usuário"""
    if hasattr(request.user, 'organizacao'):
        perfil = request.user.organizacao
        is_organizacao = True
        oportunidades = Oportunidade.objects.filter(organizacao=perfil).order_by('-data_cadastro')
        feedbacks = None
    else:
        perfil = request.user.voluntario
        is_organizacao = False
        inscricoes = Inscricao.objects.filter(voluntario=perfil).order_by('-data_inscricao')
        feedbacks = Feedback.objects.filter(voluntario=perfil).select_related('organizacao', 'oportunidade').order_by('-data_cadastro')

    # Processa upload da foto
    if request.method == 'POST' and 'foto' in request.FILES:
        perfil.foto = request.FILES['foto']
        perfil.save()
        messages.success(request, 'Foto de perfil atualizada com sucesso!')
        return redirect('perfil')

    return render(request, 'core/perfil.html', {
        'perfil': perfil,
        'is_organizacao': is_organizacao,
        'oportunidades': oportunidades if is_organizacao else None,
        'inscricoes': inscricoes if not is_organizacao else None,
        'feedbacks': feedbacks
    })

def pesquisa(request):
    """Página de pesquisa de oportunidades"""
    query = request.GET.get('q', '').strip()
    oportunidades = Oportunidade.objects.all()
    if query:
        oportunidades = oportunidades.filter(
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query) |
            Q(organizacao__nome__icontains=query) |
            Q(local__icontains=query)
        ).distinct()
    return render(request, 'core/pesquisa.html', {
        'oportunidades': oportunidades,
        'query': query
    })

@login_required
def detalhe_oportunidade(request, oportunidade_id):
    """Página de detalhes de uma oportunidade"""
    oportunidade = get_object_or_404(Oportunidade, id=oportunidade_id)
    ja_inscrito = False
    form = None
    inscritos = None
    feedback_form = None

    if hasattr(request.user, 'voluntario'):
        voluntario = request.user.voluntario
        ja_inscrito = Inscricao.objects.filter(
            voluntario=voluntario,
            oportunidade=oportunidade
        ).exists()
        if not ja_inscrito:
            if request.method == 'POST':
                form = InscricaoForm(request.POST, request.FILES)
                if form.is_valid():
                    inscricao = form.save(commit=False)
                    inscricao.voluntario = voluntario
                    inscricao.oportunidade = oportunidade
                    inscricao.save()
                    messages.success(request, 'Inscrição realizada com sucesso!')
                    return redirect('detalhe_oportunidade', oportunidade_id=oportunidade_id)
            else:
                form = InscricaoForm()
    elif hasattr(request.user, 'organizacao') and oportunidade.organizacao == request.user.organizacao:
        inscritos = Inscricao.objects.filter(oportunidade=oportunidade).select_related('voluntario')
        feedback_form = FeedbackForm()

    return render(request, 'core/detalhe_oportunidade.html', {
        'oportunidade': oportunidade,
        'ja_inscrito': ja_inscrito,
        'form': form,
        'inscritos': inscritos,
        'feedback_form': feedback_form
    })

@login_required
def atualizar_status_inscricao(request, inscricao_id, novo_status):
    """Atualiza o status de uma inscrição"""
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    # Verifica se o usuário é da organização dona da oportunidade
    if not hasattr(request.user, 'organizacao') or inscricao.oportunidade.organizacao != request.user.organizacao:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
        return redirect('detalhe_oportunidade', oportunidade_id=inscricao.oportunidade.id)
    
    inscricao.status = novo_status
    inscricao.save()
    messages.success(request, f'Status da inscrição atualizado para {inscricao.get_status_display()}')
    return redirect('detalhe_oportunidade', oportunidade_id=inscricao.oportunidade.id)

@login_required
def dar_feedback(request, inscricao_id):
    """Adiciona feedback para uma inscrição"""
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    
    # Verifica se o usuário é da organização dona da oportunidade
    if not hasattr(request.user, 'organizacao') or inscricao.oportunidade.organizacao != request.user.organizacao:
        messages.error(request, 'Você não tem permissão para realizar esta ação.')
        return redirect('detalhe_oportunidade', oportunidade_id=inscricao.oportunidade.id)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.organizacao = request.user.organizacao
            feedback.voluntario = inscricao.voluntario
            feedback.oportunidade = inscricao.oportunidade
            feedback.inscricao = inscricao
            feedback.save()
            messages.success(request, 'Feedback enviado com sucesso!')
            return redirect('detalhe_oportunidade', oportunidade_id=inscricao.oportunidade.id)
    
    return redirect('detalhe_oportunidade', oportunidade_id=inscricao.oportunidade.id)

@login_required
def inscrever_oportunidade(request, oportunidade_id):
    """View para inscrever em uma oportunidade"""
    oportunidade = get_object_or_404(Oportunidade, id=oportunidade_id)
    
    if hasattr(request.user, 'voluntario'):
        voluntario = request.user.voluntario
        if not Inscricao.objects.filter(voluntario=voluntario, oportunidade=oportunidade).exists():
            Inscricao.objects.create(
                voluntario=voluntario,
                oportunidade=oportunidade
            )
            messages.success(request, 'Inscrição realizada com sucesso!')
    
    return redirect('detalhe_oportunidade', oportunidade_id=oportunidade_id)

def login(request):
    """Página de login do usuário"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def certificados(request):
    if hasattr(request.user, 'organizacao'):
        feedbacks_dados = Feedback.objects.filter(organizacao=request.user.organizacao)
        feedbacks_recebidos = None
        certificados = None
    else:
        feedbacks_dados = None
        feedbacks_recebidos = Feedback.objects.filter(voluntario=request.user.voluntario)
        certificados = Certificado.objects.filter(voluntario=request.user.voluntario).select_related('oportunidade')
    
    context = {
        'feedbacks_dados': feedbacks_dados,
        'feedbacks_recebidos': feedbacks_recebidos,
        'certificados': certificados
    }
    return render(request, 'core/certificados.html', context)
