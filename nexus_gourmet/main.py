from app import create_app

# Cria a instância da aplicação configurada no app.py
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*50)
    print("✅ Servidor do Nexus Gourmet iniciado com sucesso!")
    print("➡️  Acesse: http://127.0.0.1:5000")
    print("🔄 Pressione Ctrl+C para parar o servidor.")
    print("="*50 + "\n")
    
    # Roda a aplicação Flask
    # debug=True permite que o servidor reinicie sozinho ao salvar arquivos
    app.run(host='127.0.0.1', port=5000, debug=True)