# Classe base que contém funcionalidades úteis reaproveitadas 
# pelos outros controladores, como a capacidade de exibir arquivos estáticos 
# e jogar dados de sessão para as telas.


# import os
# from bottle import static_file, template, redirect, request

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# class BaseController:
#     def __init__(self, app):
#         self.app = app

#     def setup_routes(self):
#         """Configura as rotas base."""
#         self.app.route('/static/<filename:path>', callback=self.serve_static)
#         self.app.route('/helper', method=['GET'], callback=self.helper)

#     def serve_static(self, filename):
#         """Serve ficheiros estáticos usando o caminho absoluto."""
#         return static_file(filename, root=STATIC_ROOT)
    
#     def helper(self):
#         """Renderiza a página de ajuda."""
#         return self.render('helper-final')

#     def render(self, template_name, **context):
#         """Renderiza um template e passa a sessão para ele."""
#         session = request.environ.get('beaker.session')
#         context['session'] = session
#         return template(template_name, **context)

#     def redirect(self, path):
#         """Redireciona para um novo URL."""
#         return redirect(path)