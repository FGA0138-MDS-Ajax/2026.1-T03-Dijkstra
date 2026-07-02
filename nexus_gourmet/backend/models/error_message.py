class UserErrorMessages:
    NOME_INVALIDO = "O nome deve conter apenas letras."
    NOME_OBRIGATORIO = "Nome do usuário é obrigatório."
    NOME_TAMANHO = "O nome deve ter entre 3 e 50 caracteres."
        
    CPF_INVALIDO = "O CPF informado é inválido."
    CPF_OBRIGATORIO = "CPF é obrigatório."
    CPF_DUPLICADO = "Este CPF já está cadastrado no sistema."
    CPF_OUTRO_USUARIO = "Este CPF já está cadastrado para outro usuário."
    
    SENHA_INVALIDA = "A senha deve conter pelo menos uma letra maiúscula, uma letra minúscula, um número e um caractere especial."
    SENHA_OBRIGATORIA = "Senha é obrigatória."
    SENHA_TAMANHO = "A senha deve ter entre 6 e 20 caracteres."
    SENHA_LETRA_MAISCUULA = "A senha deve conter pelo menos uma letra maiúscula."
    SENHA_LETRA_MINUSCULA = "A senha deve conter pelo menos uma letra minúscula."
    SENHA_NUMERO = "A senha deve conter pelo menos um número."
    SENHA_CARACTERE_ESPECIAL = "A senha deve conter pelo menos um caractere especial."

    CARGO_INVALIDO = "Cargo inválido."
    CARGO_OBRIGATORIO = "Cargo é obrigatório."

    FOTO_INVALIDA = "A foto enviada é inválida."
    FOTO_OBRIGATORIA = "Foto é obrigatória."
    FOTO_TAMANHO = "A foto deve ter no máximo 2MB."
    FOTO_FORMATO_INVALIDO = "Formato de foto inválido. Use PNG, JPG, ou JPEG."
    
    ACESSO_NEGADO = "Acesso negado. Apenas administradores podem criar usuários."
    ADMIN_SENHA_INCORRETA = "Senha do administrador incorreta. Alteração não autorizada."
    ADMIN_AUTOEXCLUSAO_NAO_PERMITIDA = "Você não pode excluir sua própria conta de administrador."
    ADMIN_JA_EXISTENTE = "Já existe um administrador cadastrado. Não é permitido criar outro."

    LOGIN_MAL_SUCEDIDO = "Login mal-sucedido."
    DADOS_INCORRETOS = "Dados incorretos. Verifique seu CPF e senha."
    USUARIO_NAO_ENCONTRADO = "Usuário não encontrado."

class OrderErrorMessages:
    COMANDA_NAO_ENCONTRADA = "Comanda não encontrada."
    COMANDA_JA_FECHADA = "Comanda já está fechada."
    COMANDA_JA_CANCELADA = "Comanda já está cancelada."
    COMANDA_SEM_ITENS = "Não é possível enviar uma comanda sem itens."
    COMANDA_NAO_PODE_SER_FECHADA = "Comanda não pode ser fechada. Verifique se todos os itens foram entregues ou cancelados."
    COMANDA_NAO_PODE_SER_CANCELADA = "Comanda não pode ser cancelada. Verifique se todos os itens foram entregues ou cancelados."
    
    ERRO_ABRIR_COMANDA = "Erro ao abrir comanda."
    ERRO_FECHAR_COMANDA = "Erro ao fechar comanda."
    ERRO_CANCELAR_COMANDA = "Erro ao cancelar comanda."
    ERRO_EDITAR_COMANDA = "Erro ao editar comanda."

    SEM_PERMISSAO = "Sem permissão para realizar esta ação."

    QUANTIDADE_MINIMA = "Quantidade muito baixa. Deve ser um número inteiro maior que zero."
    QUANTIDADE_INVALIDA = "Quantidade inválida."

class TableErrorMessages:
    MESA_JA_EXISTE = "Número de mesa já existe."
    MESA_NAO_ENCONTRADA = "Mesa não encontrada."
    MESA_COM_COMANDAS = "Mesa possui comandas abertas."

    ERRO_ATUALIZAR_MESA = "Erro ao atualizar mesa."

    CAPACIDADE_INVALIDA = "Capacidade da mesa deve ser maior que zero."
    CAPACIDADE_EXCEDIDA = "Capacidade da mesa deve ser menor ou igual a 20."
    
