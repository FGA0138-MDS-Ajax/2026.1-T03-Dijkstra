from app import create_app
from backend.models.models import db, User
from backend.models.enums import Role
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Cria o admin padrão
    admin = User(
        nome="Admin Principal",
        senha=generate_password_hash("admin123"), # Altere a senha aqui
        cargo=Role.ADMINISTRADOR
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Usuário Administrador criado com sucesso!")
    print("Login: (Use o ID gerado automaticamente, geralmente 1)")
    print("Senha: admin123")