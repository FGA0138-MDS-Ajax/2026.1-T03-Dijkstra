#Classe base que contém funcionalidades úteis reaproveitadas 
#pelos outros controladores, como a capacidade de exibir arquivos estáticos 
#e jogar dados de sessão para as telas.


import os
from flask import render_template, session, redirect, send_from_directory, request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

class BaseController:
    def __init__(self, app):
        self.app = app

    def setup_routes(self):
        """Configura as rotas base."""
        #se nn me engano no flask arquivos /static sao servidos automaticamente
        #essa rota vai ser para os aquivos que fogem do padrao
        self.app.add_url_rule('/static/<path:filename>',endpoint='serve_static',
            view_func=self.serve_static)
        self.app.add_url_rule('/helper',endpoint='helper',
            view_func=self.helper,methods=['GET'])

    def serve_static(self, filename):
        """Serve ficheiros estáticos usando o caminho absoluto."""
        return send_from_directory(STATIC_ROOT, filename)
    
    def helper(self):
        """Renderiza a página de ajuda."""
        return self.render('helper-final.html')

    def render(self, template_name: str, **context):
        """Renderiza um template e passa a sessão para ele."""
        #session = request.environ.get('beaker.session')
        context['session'] = dict(session)
        return render_template(template_name, **context)

    def redirect(self, path):
        """Redireciona para um novo URL."""
        return redirect(path)