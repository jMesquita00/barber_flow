from app import db, create_app
from app.models import Booking

app = create_app()
with app.app_context():
    # Dicionário com os nomes EXATOS que você usa no formulário
    precos = {
        "Corte Degradê": 45.0,
        "Barba Completa": 30.0,
        "Combo (Cabelo + Barba)": 65.0,
        "Corte": 45.0 # Caso tenha salvo apenas como "Corte"
    }
    
    agendamentos = Booking.query.all()
    for a in agendamentos:
        if a.valor == 0 or a.valor is None:
            # Busca o preço ou define 45.0 como padrão se não achar o nome
            a.valor = precos.get(a.servico, 45.0)
    
    db.session.commit()
    print("✅ Preços atualizados no banco de dados!")