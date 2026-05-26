# Esta camada concentra as regras de negócio complexas 
# (a inteligência central do sistema), 
# atuando como uma ponte entre os dados e o que o usuário solicitou nas telas.


# from bottle import request
# from models.user import UserModel, User
# from datetime import datetime, timedelta    
# import uuid

# class UserService:
#     def __init__(self):
#         self.user_model = UserModel()

#     def get_all(self):
#         return self.user_model.get_all()

#     def get_by_id(self, user_id):
#         return self.user_model.get_by_id(user_id)

#     def get_by_email(self, email):
#         return self.user_model.get_by_email(email)

#     def add_user(self, name, email, birthdate, password):
#         """Cria um novo usuário com senha. Todos os novos usuários são 'Padrao'."""
#         all_users = self.get_all()
#         last_id = max([u.id for u in all_users if u.id is not None], default=0)
#         new_id = last_id + 1

#         user_type = 'Padrao'

#         user = User(
#             id=new_id,
#             name=name,
#             birthdate=birthdate,
#             email=email,
#             password_hash='',
#             user_type=user_type
#         )
#         user.set_password(password)

#         self.user_model.add_user(user)
#         return user
    
#     def authenticate_user(self, email, password):
#         """Autentica um usuário, verificando email e senha."""
#         user = self.get_by_email(email)
#         if user and user.check_password(password):
#             return user
#         return None
    
#     def edit_user(self, user: User):
#         user.name = request.forms.get('name')
#         user.email = request.forms.get('email')
#         user.birthdate = request.forms.get('birthdate')

#     def delete_user(self, user_id: int):
#         self.user_model.delete_user(user_id)

#     def generate_reset_token(self, user: User):
#         """Gera e salva um token de redefinição de senha para o usuário."""
#         expiry_time = datetime.now() + timedelta(hours=1)
#         user.reset_token = str(uuid.uuid4())
#         user.reset_token_expiry = expiry_time.isoformat()
#         self.user_model.update_user(user)
#         return user.reset_token

#     def get_user_by_reset_token(self, token: str):
#         """Encontra um usuário pelo token e verifica se não expirou."""
#         if not token:
#             return None
            
#         all_users = self.get_all()
#         user = next((u for u in all_users if u.reset_token == token), None)

#         if user and user.reset_token_expiry:
#             expiry_date = datetime.fromisoformat(user.reset_token_expiry)
#             if datetime.now() > expiry_date:
#                 return None
#             return user
#         return None

#     def update_password(self, user: User, new_password: str):
#         """Atualiza a senha do usuário e invalida o token de redefinição."""
#         user.set_password(new_password)
#         user.reset_token = None
#         user.reset_token_expiry = None
#         self.user_model.update_user(user)
#         return True

#     def change_user_type(self, user_id: int, new_type: str):
#         """Altera o tipo de um usuário (ex: Padrao -> Admin ou Admin -> Padrao)."""

#         if new_type == 'Dono':
#             return False, "Não é possível promover um usuário a Dono."

#         user = self.get_by_id(user_id)
#         if user and user.user_type != 'Dono':
#             user.user_type = new_type
#             self.user_model.update_user(user)
#             return True, f"Usuário {user.name} agora é {new_type}."
        
#         if user and user.user_type == 'Dono':
#              return False, "A permissão do Dono não pode ser alterada."

#         return False, "Usuário não encontrado."
    
#     def add_to_wishlist(self, user_id: int, livro_id: str):
#         """Adiciona um livro à lista de desejos do usuário."""
#         user = self.get_by_id(user_id)
#         if user and livro_id not in user.wishlist:
#             user.wishlist.append(livro_id)
#             self.user_model.update_user(user)
#             return True, "Livro adicionado à sua lista de desejos!"
#         elif not user:
#             return False, "Usuário não encontrado."
#         else:
#             return False, "Este livro já está na sua lista de desejos."
            
#     def remove_from_wishlist(self, user_id: int, livro_id: str):
#         """Remove um livro da lista de desejos do usuário."""
#         user = self.get_by_id(user_id)
#         if user and livro_id in user.wishlist:
#             user.wishlist.remove(livro_id)
#             self.user_model.update_user(user)
#             return True, "Livro removido da sua lista de desejos."
#         elif not user:
#             return False, "Usuário não encontrado."
#         else:
#             return False, "Este livro não está na sua lista de desejos."
    
#     def transferir_propriedade(self, new_owner_id: int, current_owner_id: int):
#         """Transfere a propriedade do sistema para outro usuário."""
#         new_owner = self.get_by_id(new_owner_id)
#         current_owner = self.get_by_id(current_owner_id)

#         if not new_owner or not current_owner:
#             return False, "Usuário não encontrado."

#         if current_owner.user_type != 'Dono':
#             return False, "Apenas o Dono atual pode transferir a propriedade."

#         new_owner.user_type = 'Dono'
#         current_owner.user_type = 'Admin'
        
#         self.user_model.update_user(new_owner)
#         self.user_model.update_user(current_owner)

#         return True, f"Propriedade transferida com sucesso para {new_owner.name}."