from flask import render_template

class BaseController:
    def __init__(self, app):
        self.app = app

    def render(self, template_name, **context):
        # Centraliza a renderização de templates do Flask.
        # Garante que o contexto e as variáveis sejam repassados corretamente para as views.

        if not template_name.endswith(('.html', '.tpl')):
            template_name += '.html'
        return render_template(template_name, **context)