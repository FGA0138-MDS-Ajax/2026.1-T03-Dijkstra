# config.py: Armazena as configurações globais do sistema, 
# como o endereço e porta do servidor (localhost:1422), 
# a chave secreta e os caminhos (paths) para as pastas de dados e templates.


# import os
# from bottle import TEMPLATE_PATH

# class Config:
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#     HOST = 'localhost'
#     PORT = 1422
#     DEBUG = True
#     RELOADER = True

#     TEMPLATE_PATH.insert(0, os.path.join(BASE_DIR, 'views'))
#     STATIC_PATH = os.path.join(BASE_DIR, 'static')
#     DATA_PATH = os.path.join(BASE_DIR, 'data')

#     SECRET_KEY = 'SUA CHAVE_SECRETA_AQUI'