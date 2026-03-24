from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///barbearia.db'

    db.init_app(app)

    login_manager = LoginManager()
    # login_manager.login_view = 'routes.login'
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all() # Cria o banco de dados automaticamente

    return app