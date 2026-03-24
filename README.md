# 💈 BarberFlow - Gestão Inteligente para Barbearias

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D?style=for-the-badge&logo=chart.js&logoColor=white)

O **BarberFlow** é uma aplicação Full Stack desenvolvida para modernizar a operação de barbearias. O sistema resolve dois problemas centrais: a conveniência do agendamento para o cliente e o controle financeiro preciso para o gestor.

---

## 🎯 Desafios Resolvidos

Durante o desenvolvimento, foquei em resolver problemas reais de integração:
- **Persistência Dinâmica:** Implementação de lógica para garantir que serviços antigos sem valor atribuído não quebrassem o cálculo de faturamento (tratamento de `Null/None`).
- **Data Visualization:** Integração do **Chart.js** com Jinja2 para transformar dados brutos do banco SQL em insights visuais (Gráficos de Barra).
- **UX/UI Premium:** Criação de uma interface com tema escuro (*Dark Mode*) e detalhes em dourado, utilizando CSS moderno e animações para elevar a percepção de valor da marca.

---

## 🚀 Funcionalidades

### 👤 Área do Cliente
- **Agendamento Intuitivo:** Interface para escolha de serviços (Corte, Barba, Combo) com validação de data e hora.
- **Design Responsivo:** Adaptável para qualquer tamanho de tela (Mobile First).

### 🔐 Painel Administrativo
- **Gestão de Status:** Controle total sobre agendamentos (Pendentes vs. Concluídos).
- **Módulo Financeiro:** - Dashboard com Faturamento Bruto total.
    - Gráfico dinâmico de receita distribuída por categoria de serviço.
    - Histórico de fluxo de caixa com ordenação cronológica inversa.

---

## 🛠️ Tecnologias e Bibliotecas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask
- **Banco de Dados:** SQLAlchemy (SQLite)
- **Frontend:** HTML5, CSS3 (Custom Styles), Bootstrap 5
- **Gráficos:** Chart.js (Integração via JSON Safe)
- **Iconografia:** FontAwesome 6

---

## 📂 Estrutura do Projeto

```text
├── app/
│   ├── static/          # CSS customizado, Scripts JS e Ativos
│   ├── templates/       # Páginas HTML (Herança de templates com Jinja2)
│   ├── models.py        # Definição das classes de Banco de Dados (ORM)
│   ├── routes.py        # Controladores e Lógica de Negócio
│   └── __init__.py      # Inicialização da App e Contexto do Flask
├── run.py               # Arquivo principal para execução
├── requirements.txt     # Dependências para reprodução do ambiente
└── README.md            # Documentação técnica
```
## 📦 Como Instalar e Rodar
Clonar o Repositório:git clone [https://github.com/seu-usuario/barberflow.git](https://github.com/seu-usuario/barberflow.git)
cd barberflow


## Configurar Ambiente Virtual

```text
python -m venv venv
# Ativar (Windows):
venv\Scripts\activate
# Ativar (Linux/Mac):
source venv/bin/activate
```

## Instalar as dependências 
```text
pip install -r requirements.txt
```
## Executar a aplicação
```text
python run.py
```


##👨‍💻 Autor
Desenvolvido por João Marcos Vieira de Mesquita.

📍 Disponível para novos desafios e colaborações.
