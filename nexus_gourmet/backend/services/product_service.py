import os
import uuid
from flask import current_app
from backend.models.models import db, Product
from backend.models.enums import ProductCategory, Role

class ProductService:     
    def listar_produtos(self):
        return Product.query.all()  
 
    def listar_por_categoria(self, categoria):
        try:
            if isinstance(categoria, str):
                categoria = ProductCategory(categoria)
        except ValueError:
            return []
        return Product.query.filter_by(categoria=categoria).all()
 
    def cadastrar_produto(self, nome, categoria, preco, tempo_preparacao=15, foto_produto=None, user_role=None):
        if user_role and user_role != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem cadastrar produtos."

        if not nome or not nome.strip():
            return False, "Nome do produto é obrigatório."
        
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            return False, "Preço inválido."
            
        if preco <= 0:
            return False, "Preço deve ser maior que zero."
            
        try:
            categoria = ProductCategory(categoria)
        except ValueError:
            return False, f"Categoria inválida: {categoria}."
 
        foto_url = None
        if foto_produto is not None:
            if hasattr(foto_produto, 'filename') and foto_produto.filename != '':
                extensao = foto_produto.filename.rsplit('.', 1)[-1].lower()
                extensoes_permitidas = {'png', 'jpg', 'jpeg', 'webp'}
                if extensao not in extensoes_permitidas:
                    return False, "Formato de foto inválido. Use PNG, JPG, JPEG ou WEBP."
                
                novo_nome = f"{uuid.uuid4().hex}.{extensao}"
                caminho_pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'produtos')
                caminho = os.path.join(caminho_pasta, novo_nome)
                foto_produto.save(caminho)
                foto_url = f"/static/uploads/produtos/{novo_nome}"
            elif isinstance(foto_produto, str) and foto_produto.strip():
                foto_url = foto_produto.strip()

        try:
            produto = Product(
                nome=nome.strip(), 
                categoria=categoria, 
                preco=preco, 
                tempo_preparacao=int(tempo_preparacao),
                foto_prato=foto_url
            )
            db.session.add(produto)
            db.session.commit()
            return True, "Produto cadastrado com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao salvar no banco de dados: {str(e)}"
 
    def editar_produto(self, product_id, nome, categoria, preco, tempo_preparacao=15, foto_produto=None, user_role=None):
        if user_role and user_role != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem editar produtos."

        produto = self.get_product_by_id(product_id)
        if not produto:
            return False, "Produto não encontrado."
            
        if not nome or not nome.strip():
            return False, "Nome do produto é obrigatório."
            
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            return False, "Preço inválido."
            
        if preco <= 0:
            return False, "Preço deve ser maior que zero."
            
        try:
            categoria = ProductCategory(categoria)
        except ValueError:
            return False, f"Categoria inválida: {categoria}."
 
        try:
            produto.nome = nome.strip()
            produto.categoria = categoria
            produto.preco = preco
            produto.tempo_preparacao = int(tempo_preparacao)
            
            if foto_produto is not None:
                if hasattr(foto_produto, 'filename') and foto_produto.filename != '':
                    extensao = foto_produto.filename.rsplit('.', 1)[-1].lower()
                    if extensao in {'png', 'jpg', 'jpeg', 'webp'}:
                        novo_nome = f"{uuid.uuid4().hex}.{extensao}"
                        caminho_pasta = os.path.join(current_app.config['UPLOAD_FOLDER'], 'produtos')
                        caminho = os.path.join(caminho_pasta, novo_nome)
                        foto_produto.save(caminho)
                        produto.foto_prato = f"/static/uploads/produtos/{novo_nome}"
                elif isinstance(foto_produto, str) and foto_produto.strip():
                    produto.foto_prato = foto_produto.strip()

            db.session.commit()
            return True, "Produto atualizado com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao atualizar no banco de dados: {str(e)}"
 
    def deletar_produto(self, product_id, user_role=None):
        if user_role and user_role != Role.ADMINISTRADOR:
            return False, "Acesso negado. Apenas administradores podem deletar produtos."

        produto = self.get_product_by_id(product_id)
        if not produto:
            return False, "Produto não encontrado."
            
        try:
            db.session.delete(produto)
            db.session.commit()
            return True, "Produto excluído com sucesso."
        except Exception as e:
            db.session.rollback()
            return False, f"Erro ao excluir do banco de dados: {str(e)}"

    def get_product_by_id(self, product_id):
        return db.session.get(Product, product_id)