from app import create_app
from backend.models.models import db, User
from backend.models.enums import Role
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    # Defina aqui o CPF e a Senha que você quer usar para o Admin
    cpf_admin = "12345678901"  # Importante: Deve ser um CPF válido pelo algoritmo ou mude a validação
    senha_admin = "Admin@123"  # Atende aos requisitos: Maiúscula, minúscula, número e caracter especial
    
    # Se quiser testar com um CPF fictício sem validação, vamos direto ao banco:
    senha_hash = generate_password_hash(senha_admin)
    
    # Verifica se já não existe
    if not User.query.filter_by(cpf=cpf_admin).first():
        admin = User(
            nome="Admin Principal",
            cpf=cpf_admin,
            senha=senha_hash,
            cargo=Role.ADMINISTRADOR
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Administrador criado com sucesso!")
        print(f"CPF: {cpf_admin}")
        print(f"Senha: {senha_admin}")
    else:
        print("⚠️ O administrador com este CPF já existe.")