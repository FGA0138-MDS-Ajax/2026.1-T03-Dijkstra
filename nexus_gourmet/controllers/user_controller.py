#Eles pegam as requisições que chegam da internet, 
#chamam as regras de serviço corretas e mandam a resposta visual para o usuário.


from flask import request, redirect, session
from .base_controller import BaseController
from services.user_service import UserService

class UserController(BaseController):
    def __init__(self, app, user_service: UserService):
        super().__init__(app)
        self.user_service = user_service
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/users',                             endpoint='list_users',        view_func=self.list_users,        methods=['GET'])
        self.app.add_url_rule('/users/view_profile/<int:user_id>',  endpoint='view_user_profile', view_func=self.view_user_profile, methods=['GET'])
        self.app.add_url_rule('/users/delete/<int:user_id>',        endpoint='delete_user',       view_func=self.delete_user,       methods=['POST'])
        self.app.add_url_rule('/users/promote/<int:user_id>',       endpoint='promote_user',      view_func=self.promote_user,      methods=['POST'])
        self.app.add_url_rule('/users/demote/<int:user_id>',        endpoint='demote_user',       view_func=self.demote_user,       methods=['POST'])
        self.app.add_url_rule('/users/transfer_ownership',          endpoint='transfer_ownership',view_func=self.transfer_ownership,methods=['POST'])
        self.app.add_url_rule('/perfil',                            endpoint='perfil',            view_func=self.perfil,            methods=['GET', 'POST'])
        self.app.add_url_rule('/perfil/delete',                     endpoint='delete_my_account', view_func=self.delete_my_account, methods=['POST'])

    def perfil(self):
        user_id = session.get('user_id')
        user = self.user_service.get_by_id(user_id)
    
        if not user:
            return redirect('/logout')

        success_message = request.query.get('success')
        error_message = request.query.get('error')

        if request.method == 'POST':
            user.name = request.forms.get('name')
            user.email = request.forms.get('email')
            user.birthdate = request.forms.get('birthdate')
            self.user_service.user_model.update_user(user)
            success_message = "Perfil atualizado com sucesso!"        
            session['user_name'] = user.name
            session.save()

            current_password = request.forms.get('current_password')
            new_password = request.forms.get('new_password')
            confirm_new_password = request.forms.get('confirm_new_password')

            if new_password:
                if not user.check_password(current_password):
                    error_message = "A senha atual está incorreta."
                elif new_password != confirm_new_password:
                    error_message = "A nova senha e a confirmação não coincidem."
                else:
                    self.user_service.update_password(user, new_password)
                    success_message = "Perfil e senha atualizados com sucesso!"

        return self.render('perfil.html', user=user, success=success_message, error=error_message)

    def delete_my_account(self):
        user_id = session.get('user_id')
        livros_emprestados = self.livro_service.get_livros_emprestados_por_usuario(user_id)

        if livros_emprestados:
            error_msg = "Você não pode apagar sua conta pois possui livros emprestados. Por favor, vá até a página 'Meus Livros' para devolvê-los."
            return redirect(f'/perfil?error={error_msg}')
        else:
            self.user_service.delete_user(user_id)
            session.delete()
            return redirect('/login?message=Sua conta foi permanentemente excluída.')

    def view_user_profile(self, user_id, session):
        user = self.user_service.get_by_id(user_id)
        if not user:
            return "Usuário não encontrado"
        
        livros_emprestados = self.livro_service.get_livros_emprestados_por_usuario(user_id)
        
        return self.render('view_user_profile', user=user, livros=livros_emprestados, user_service=self.user_service)

    def meus_livros(self, session):
        user_id = session.get('user_id')
        livros_emprestados = self.livro_service.get_livros_emprestados_por_usuario(user_id)
        return self.render('meus_livros', livros=livros_emprestados, user_service=self.user_service)
    
    def minha_lista_desejos(self, session):
        user_id = session.get('user_id')
        user = self.user_service.get_by_id(user_id)        
        wishlist_ids = user.wishlist if user else []        
        livros_desejados = [self.livro_service.get_by_id(livro_id) for livro_id in wishlist_ids]        
        livros_desejados = [livro for livro in livros_desejados if livro is not None]
        return self.render('wishlist', livros=livros_desejados, user_service=self.user_service)

    def remove_from_wishlist(self, livro_id, session):
        user_id = session.get('user_id')
        self.user_service.remove_from_wishlist(user_id, livro_id)
        return redirect('/minha-lista-desejos')

    def list_users(self, session):
        users = self.user_service.get_all()
        return self.render('users', users=users, user_service=self.user_service)

    def delete_user(self, user_id, session):
        self.user_service.delete_user(user_id)
        self.redirect('/users')

    def promote_user(self, user_id, session):
        success, message = self.user_service.change_user_type(user_id, 'Admin')
        self.redirect('/users')

    def demote_user(self, user_id, session):
        success, message = self.user_service.change_user_type(user_id, 'Padrao')
        self.redirect('/users')

    def transfer_ownership(self, session):
        current_owner_id = session.get('user_id')
        new_owner_id = int(request.forms.get('new_owner_id'))
        
        success, message = self.user_service.transferir_propriedade(new_owner_id, current_owner_id)

        if success:
            session['user_type'] = 'Admin'
            session.save()

        self.redirect('/users')