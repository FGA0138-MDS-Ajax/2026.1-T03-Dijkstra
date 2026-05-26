# É o ponto principal de entrada da aplicação. 
# Ele é o arquivo que você executa (python main.py) para iniciar o servidor web 
# e mostrar o projeto no navegador.


# import os
# from bottle import run
# from app import create_app
# from config import Config

# if __name__ == '__main__':
#     app = create_app()

#     if os.environ.get('BOTTLE_CHILD') != 'true':
#         print(f"✅ Servidor da Biblioteca iniciado!")
#         print(f"➡️  Acesse http://{Config.HOST}:{Config.PORT} para ver o projeto.")
#         print("🔄 Pressione Ctrl+C para parar o servidor.")

#     run(
#         app=app,
#         host=Config.HOST,
#         port=Config.PORT,
#         debug=Config.DEBUG,
#         reloader=Config.RELOADER,
#         quiet=True
#     )