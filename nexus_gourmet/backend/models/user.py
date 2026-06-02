# Arquivos responsáveis por definir 
# as entidades do sistema e manipular a leitura/gravação dos dados nos arquivos JSON.


# import json
# import os
# from datetime import date
# from werkzeug.security import generate_password_hash, check_password_hash

# DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# class User:
#     def __init__(self, id, name, birthdate, email, password_hash, user_type='Padrao', multa=0.0, wishlist=None, reset_token=None, reset_token_expiry=None):
#         self.id = id
#         self.name = name
#         self.birthdate = birthdate
#         self.email = email
#         self.password_hash = password_hash
#         self.user_type = user_type  
#         self.multa = multa
#         self.wishlist = wishlist if wishlist is not None else []
#         self.reset_token = reset_token
#         self.reset_token_expiry = reset_token_expiry
    
#     def set_password(self, password):
#         """Gera e armazena o hash da senha."""
#         self.password_hash = generate_password_hash(password)

#     def check_password(self, password):
#         """Verifica se a senha fornecida corresponde à senha armazenada."""
#         return check_password_hash(self.password_hash, password)
    
#     @staticmethod
#     def is_over_16(birthdate_str: str):
#         """Verifica se o usuário tem mais de 16 anos."""
#         if not birthdate_str:
#             return False
#         try:
#             birthdate = date.fromisoformat(birthdate_str)
#             today = date.today()
#             age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
#             return age >= 16
#         except ValueError:
#             return False    
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'birthdate': self.birthdate,
#             'email': self.email,
#             'password_hash': self.password_hash,
#             'user_type': self.user_type,
#             'multa': self.multa,
#             'wishlist': self.wishlist,
#             'reset_token': self.reset_token,
#             'reset_token_expiry': self.reset_token_expiry
#         }

#     @classmethod
#     def from_dict(cls, data):
#         return cls(
#             id=data.get('id'),
#             name=data.get('name'),
#             birthdate=data.get('birthdate'),
#             email=data.get('email'),
#             password_hash=data.get('password_hash'),
#             user_type=data.get('user_type', 'Padrao'),
#             multa=data.get('multa', 0.0),
#             wishlist=data.get('wishlist', []),
#             reset_token=data.get('reset_token'),
#             reset_token_expiry=data.get('reset_token_expiry')
#         )

# class UserModel:
#     FILE_PATH = os.path.join(DATA_DIR, 'users.json')

#     def __init__(self):
#         self.users = self._load()

#     def _load(self):
#         if not os.path.exists(self.FILE_PATH):
#             return []
#         try:
#             with open(self.FILE_PATH, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
#                 return [User.from_dict(item) for item in data]
#         except (json.JSONDecodeError, IOError):
#             return []

#     def _save(self):
#         with open(self.FILE_PATH, 'w', encoding='utf-8') as f:
#             json.dump([u.to_dict() for u in self.users], f, indent=4, ensure_ascii=False)

#     def get_all(self):
#         return self.users

#     def get_by_id(self, user_id: int):
#         return next((u for u in self.users if u.id == user_id), None)
    
#     def get_by_email(self, email: str):
#         return next((u for u in self.users if u.email and u.email.lower() == email.lower()), None)

#     def add_user(self, user: User):
#         self.users.append(user)
#         self._save()

#     def update_user(self, updated_user: User):
#         for i, user in enumerate(self.users):
#             if user.id == updated_user.id:
#                 self.users[i] = updated_user
#                 self._save()
#                 break

#     def delete_user(self, user_id: int):
#         self.users = [u for u in self.users if u.id != user_id]
#         self._save()