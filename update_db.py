# from app import db, create_app
# from sqlalchemy import text

# app = create_app()
# with app.app_context():
#     try:
#         # Este comando adiciona a coluna diretamente no banco de dados
#         db.session.execute(text("ALTER TABLE barbearia ADD COLUMN dono_id INTEGER REFERENCES user(id)"))
#         db.session.commit()
#         print("✅ Coluna 'dono_id' adicionada com sucesso!")
#     except Exception as e:
#         print(f"❌ Erro: {e}")
#         print("Provavelmente a coluna já existe ou o caminho do banco está incorreto.")

#     # Agora vamos ligar os donos existentes às barbearias
#     from app.models import User, Barbearia
#     admins = User.query.filter_by(is_admin=True).all()
#     saloes = Barbearia.query.all()

#     for i, salao in enumerate(saloes):
#         if i < len(admins):
#             salao.dono_id = admins[i].id
#             print(f"🔗 Vinculando: {admins[i].nome} -> {salao.nome}")
    
#     db.session.commit()
#     print("🚀 Banco de dados atualizado!")


# salve como update_status.py e rode: python update_status.py
from app import db, create_app
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE booking ADD COLUMN status VARCHAR(20) DEFAULT 'pendente'"))
        db.session.execute(text("ALTER TABLE booking ADD COLUMN valor FLOAT DEFAULT 0.0"))
        db.session.commit()
        print("✅ Colunas de status e valor adicionadas!")
    except Exception as e:
        print(f"⚠️ Aviso: {e}")