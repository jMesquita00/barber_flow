from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from .models import Booking, User, Barbearia
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

# --- ROTA PRINCIPAL (CLIENTE) ---
@main.route('/')
@login_required
def index():
    meus_agendamentos = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', nome=current_user.nome, agendamentos=meus_agendamentos)

# --- SELEÇÃO DE SALÃO ---
@main.route('/selecionar_salao')
@login_required
def selecionar_salao():
    saloes = Barbearia.query.all()
    return render_template('selecionar_salao.html', saloes=saloes)

# --- AGENDAMENTO DETALHADO ---
@main.route('/agendar/<int:salao_id>', methods=['GET', 'POST'])
@login_required
def agendar(salao_id):
    salao = Barbearia.query.get_or_404(salao_id)
    
    if request.method == 'POST':
        data_str = request.form.get('data_hora')
        servico = request.form.get('servico')
        data_dt = datetime.strptime(data_str, '%Y-%m-%dT%H:%M')
        
        if data_dt < datetime.now():
            flash('Você não pode agendar um horário que já passou!', 'warning')
            return render_template('agendar_detalhes.html', salao=salao)

        # 1. Tabela de preços (deve ser igual à do seu agendar_detalhes.html)
        precos = {
            "Corte Degradê": 45.0,
            "Barba Completa": 30.0,
            "Combo (Cabelo + Barba)": 65.0
        }
        valor_servico = precos.get(servico, 0.0)

        # 2. Verifica conflito APENAS para horários que não foram cancelados
        conflito = Booking.query.filter_by(
            data_hora=data_dt, 
            barbearia_id=salao_id
        ).filter(Booking.status != 'cancelado').first()
        
        if conflito:
            flash('Este horário já está ocupado nesta unidade.', 'danger')
        else:
            # 3. Cria o agendamento incluindo Valor e Status
            novo_agendamento = Booking(
                data_hora=data_dt,
                servico=servico,
                valor=valor_servico,     # Novo campo
                status='pendente',       # Novo campo
                user_id=current_user.id,
                barbearia_id=salao_id
            )
            try:
                db.session.add(novo_agendamento)
                db.session.commit()
                flash(f'Sucesso! Horário marcado na {salao.nome}.', 'success')
                return redirect(url_for('main.index'))
            except Exception as e:
                db.session.rollback()
                flash('Erro ao salvar agendamento.', 'danger')
                
    return render_template('agendar_detalhes.html', salao=salao)

# --- LOGIN ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.query.filter_by(email=email).first()

        if user and user.senha == senha:
            login_user(user) 
            return redirect(url_for('main.admin_panel' if user.is_admin else 'main.index'))
        
        flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')

# --- CADASTRO ---
@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Verifica se e-mail já existe
        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está cadastrado!', 'warning')
            return redirect(url_for('main.cadastro'))

        nome = request.form.get('nome')
        senha = request.form.get('senha')
        is_admin = True if request.form.get('is_admin') else False
        
        novo_usuario = User(nome=nome, email=email, senha=senha, is_admin=is_admin)
        db.session.add(novo_usuario)
        db.session.commit()
        if is_admin:
            nome_b = request.form.get('nome_barbearia')
            end_b = request.form.get('endereco_barbearia')
            # Adicionamos dono_id=novo_usuario.id
            nova_barbearia = Barbearia(nome=nome_b, endereco=end_b, dono_id=novo_usuario.id)
            db.session.add(nova_barbearia)
            db.session.commit()
        flash('Conta criada com sucesso!', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('cadastro.html')

# --- LOGOUT ---
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# --- PAINEL ADMIN (MELHORADO) ---

@main.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    
    minha_barbearia = Barbearia.query.filter_by(dono_id=current_user.id).first()
    
    if minha_barbearia:
        # Mostra apenas os PENDENTES para o barbeiro trabalhar
        agendamentos = Booking.query.filter_by(
            barbearia_id=minha_barbearia.id, 
            status='pendente'
        ).order_by(Booking.data_hora.asc()).all()
    else:
        agendamentos = []

    return render_template('admin.html', agendamentos=agendamentos)


@main.route('/concluir_agendamento/<int:id>', methods=['POST'])
@login_required
def concluir_agendamento(id):
    agendamento = Booking.query.get_or_404(id)
    
    # Garantia extra: se o valor for 0, tenta atribuir antes de somar
    if not agendamento.valor or agendamento.valor == 0:
        precos = {"Corte Degradê": 45.0, "Barba Completa": 30.0, "Combo (Cabelo + Barba)": 65.0}
        agendamento.valor = precos.get(agendamento.servico, 45.0)

    agendamento.status = 'concluido'
    db.session.commit()
    flash('Atendimento concluído e valor registrado!', 'success')
    return redirect(url_for('main.admin_panel'))



@main.route('/cancelar_agendamento/<int:id>', methods=['POST'])
@login_required
def cancelar_agendamento(id):
    agendamento = Booking.query.get_or_404(id)
    agendamento.status = 'cancelado' # Em vez de deletar, marcamos como cancelado
    db.session.commit()
    flash('Agendamento marcado como cancelado.', 'warning')
    return redirect(url_for('main.admin_panel'))


@main.route('/financeiro')
@login_required
def financeiro():
    if not current_user.is_admin:
        flash('Acesso restrito!', 'danger')
        return redirect(url_for('main.index'))
    
    minha_barbearia = Barbearia.query.filter_by(dono_id=current_user.id).first()
    
    if not minha_barbearia:
        flash('Nenhuma barbearia vinculada ao seu usuário.', 'warning')
        return redirect(url_for('main.index'))

    # 1. Busca atendimentos concluídos
    atendimentos = Booking.query.filter_by(
        barbearia_id=minha_barbearia.id, 
        status='concluido'
    ).all()
    
    # 2. Calcula o total garantindo que valores vazios virem 0.0
    total_faturado = sum((atendimento.valor or 0.0) for atendimento in atendimentos)
    
    # 3. Lógica para o Gráfico (Flexível para nomes diferentes)
    contagem_servicos = {
        "Corte": 0.0,
        "Barba": 0.0,
        "Combo": 0.0
    }
    
    for a in atendimentos:
        valor_atendimento = a.valor or 0.0
        servico_nome = a.servico.lower() # Padroniza para minúsculo para comparar
        
        # Procura palavras-chave no nome do serviço
        if "corte" in servico_nome:
            contagem_servicos["Corte"] += valor_atendimento
        elif "barba" in servico_nome:
            contagem_servicos["Barba"] += valor_atendimento
        elif "combo" in servico_nome:
            contagem_servicos["Combo"] += valor_atendimento
        else:
            # Caso o nome seja algo totalmente diferente, soma no Corte ou cria um 'Outros'
            contagem_servicos["Corte"] += valor_atendimento

    return render_template(
        'financeiro.html', 
        total=total_faturado, 
        atendimentos=atendimentos,
        dados_grafico=list(contagem_servicos.values())
    )