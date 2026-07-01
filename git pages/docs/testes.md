# Testes de Software

Este documento consolida todos os testes unitários e integrados realizados no sistema Nexus Gourmet, conforme documentado no Documento de Visão (versão 1.4).

---

## Testes Unitários

### TU01 – Editar comanda

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU01                                                                      |
| Nome           | Editar comanda                                                            |
| Objetivo       | Remover e adicionar itens                                                 |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Método de comanda criado                                                  |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Autenticação bem-sucedida / Realizado: Autenticação bem-sucedida |

---

### TU02 – Abrir comanda com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU02                                                                      |
| Nome           | Abrir comanda com sucesso                                                 |
| Objetivo       | Verificar se a função abrir comanda está funcionando como o esperado      |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Método de abrir comanda implementado                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Abertura da comanda / Realizado: -                              |

---

### TU03 – Abrir múltiplas comandas na mesma mesa

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU03                                                                      |
| Nome           | Abrir múltiplas comandas na mesma mesa                                    |
| Objetivo       | Verificar se é possível abrir múltiplas comandas na mesma mesa            |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | -                                                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Abrir diferentes comandas em uma mesma mesa / Realizado: Abre diferentes comandas em uma mesma mesa |

---

### TU04 – Listar todas as comandas

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU04                                                                      |
| Nome           | Listar todas as comandas                                                  |
| Objetivo       | Verificar se a função de listar todas as comandas dá os dados das comandas abertas |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de listar todas as comandas                                        |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Fornecer os dados das comandas abertas / Realizado: Fornecer os dados das comandas abertas |

---

### TU05 – Adicionar item com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU05                                                                      |
| Nome           | Adicionar item com sucesso                                                |
| Objetivo       | Verificar se a função adicionar item à comanda está funcionando           |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de adicionar item na comanda implementada                          |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Adicionar item na comanda / Realizado: Adiciona item na comanda |

---

### TU06 – Adicionar item - quantidade inválida

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU06                                                                      |
| Nome           | Adicionar item - quantidade inválida                                      |
| Objetivo       | Verificar o bloqueio de entrada de dados incorretos (quantidades menores ou iguais a zero) |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de adicionar item na comanda implementada                          |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir adicionar item se a quantidade não existir / Realizado: Não permite realizar item se a quantidade não existe |

---

### TU07 – Calcular total

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU07                                                                      |
| Nome           | Calcular total                                                            |
| Objetivo       | Verificar se a função calcular total fornece o valor total da comanda     |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação de itens na comanda                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Fornecer o valor da comanda / Realizado: Fornece o valor da comanda |

---

### TU08 – Enviar comanda com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU08                                                                      |
| Nome           | Enviar comanda com sucesso                                                |
| Objetivo       | Verificar se é possível enviar comanda                                    |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função de enviar comanda                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Enviar comanda para a cozinha / Realizado: Envia comanda para a cozinha |

---

### TU09 – Enviar comanda sem itens falha

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU09                                                                      |
| Nome           | Enviar comanda sem itens falha                                            |
| Objetivo       | Verificar se dá falha ao tentar enviar uma comanda vazia                  |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de enviar comanda                                                  |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Falhar ao enviar comanda vazia / Realizado: Falhar ao enviar comanda vazia |

---

### TU10 – Fechar comanda - sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU10                                                                      |
| Nome           | Fechar comanda - sucesso                                                  |
| Objetivo       | Verificar se a função de fechar comanda cumpre seu papel de fechar a comanda |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de fechar comanda                                                  |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Fechar comanda / Realizado: Fecha a comanda                     |

---

### TU11 – Alterar status

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU11                                                                      |
| Nome           | Alterar status                                                            |
| Objetivo       | Verificar se os status da comanda são alterados ao utilizar a função de alterar status |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função de alterar status                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Alterar os dados de status da comanda / Realizado: Altera o dado de status da comanda |

---

### TU12 – Cadastrar produto com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU12                                                                      |
| Nome           | Cadastrar produto com sucesso                                             |
| Objetivo       | Verificar se é possível cadastrar produtos                                |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de cadastrar produto                                               |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cadastrar um produto / Realizado: Cadastra produto              |

---

### TU13 – Cadastrar produto - campos faltando

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU13                                                                      |
| Nome           | Cadastrar produto - campos faltando                                       |
| Objetivo       | Verificar se há dados faltando no produto                                 |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de cadastrar produto                                               |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir o cadastro de produtos com dados faltando / Realizado: Não permitir o cadastro de produtos com dados faltando |

---

### TU14 – Editar produto com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU14                                                                      |
| Nome           | Editar produto com sucesso                                                |
| Objetivo       | Verificar se os dados do produto são alterados ao usar a função de editar produto |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Existência da função de editar produto                                    |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Alterar dados do produto / Realizado: Altera dados do produto   |

---

### TU15 – Deletar produto com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU15                                                                      |
| Nome           | Deletar produto com sucesso                                               |
| Objetivo       | Verificar se os dados do produto são excluídos ao usar a função de excluir produto |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de excluir produto                                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Excluir dados do produto / Realizado: Excluir dados do produto  |

---

### TU16 – Listar produtos

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU16                                                                      |
| Nome           | Listar produtos                                                           |
| Objetivo       | Verificar se a função de listar produtos retorna os dados de todos os produtos |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de listar produtos                                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Listar os dados de todos os produtos / Realizado: Lista os dados de todos os produtos |

---

### TU17 – Listar produtos por categoria

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU17                                                                      |
| Nome           | Listar produtos por categoria                                             |
| Objetivo       | Verificar se a função de listar por categoria retorna os dados dos produtos da categoria desejada |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de listar por categoria                                            |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Listar os dados dos produtos da categoria / Realizado: Lista os dados dos produtos da categoria |

---

### TU18 – Criar mesa com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU18                                                                      |
| Nome           | Criar mesa com sucesso                                                    |
| Objetivo       | Verificar se a mesa foi criada corretamente                               |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função criar mesa                                        |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Criar uma mesa com número de capacidade determinado / Realizado: Criar uma mesa com número de capacidade determinado |

---

### TU19 – Editar mesa com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU19                                                                      |
| Nome           | Editar mesa com sucesso                                                   |
| Objetivo       | Verificar se as características da mesa estão sendo editadas              |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função editar mesa                                       |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Permitir a alteração das características da mesa / Realizado: Permitir a alteração das características da mesa |

---

### TU20 – Editar mesa com capacidade inválida

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU20                                                                      |
| Nome           | Editar mesa com capacidade inválida                                       |
| Objetivo       | Verificar se o sistema reconhece que a capacidade da mesa não é válida    |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função editar mesa                                       |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Falhar ao adicionar um valor inválido ao campo capacidade / Realizado: Falhar ao adicionar um valor inválido ao campo capacidade |

---

### TU21 – Editar mesa - usuário comum não pode editar mesa

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU21                                                                      |
| Nome           | Editar mesa - usuário comum não pode editar mesa                          |
| Objetivo       | Verificar se o sistema impede a edição de uma mesa feita por um usuário comum |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função editar mesa                                       |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir que uma mesa seja editada por um usuário comum / Realizado: Não permitir que uma mesa seja editada por um usuário comum |

---

### TU22 – Deletar mesa com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU22                                                                      |
| Nome           | Deletar mesa com sucesso                                                  |
| Objetivo       | Verificar se o programa deleta as mesas quando requisitado                |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função deletar mesa                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Permitir que uma mesa seja deletada / Realizado: Permitir que uma mesa seja deletada |

---

### TU23 – Deletar mesa - usuário comum não pode deletar mesa

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU23                                                                      |
| Nome           | Deletar mesa - usuário comum não pode deletar mesa                        |
| Objetivo       | Verificar se o sistema impede que um usuário comum delete uma mesa        |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função deletar mesa                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Falha quando um usuário comum tenta deletar uma mesa / Realizado: Falha quando um usuário comum tenta deletar uma mesa |

---

### TU24 – Listar mesas

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU24                                                                      |
| Nome           | Listar mesas                                                              |
| Objetivo       | Verificar se o sistema lista as mesas ativas no salão                     |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função listar mesas                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: As mesas criadas devem aparecer na tela / Realizado: As mesas criadas devem aparecer na tela |

---

### TU25 – Listar comandas - mesa com comandas

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU25                                                                      |
| Nome           | Listar comandas - mesa com comandas                                       |
| Objetivo       | Verificar se o programa consegue listar mesas com comandas ativas         |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função listar mesas                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: As mesas com comandas abertas são listadas para o usuário / Realizado: As mesas com comandas abertas são listadas para o usuário |

---

### TU26 – Listar comandas - mesa sem comandas

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU26                                                                      |
| Nome           | Listar comandas - mesa sem comandas                                       |
| Objetivo       | Verificar se o programa consegue listar mesas sem comandas ativas         |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função listar mesas                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: As mesas sem comandas abertas são listadas para o usuário / Realizado: As mesas sem comandas abertas são listadas para o usuário |

---

### TU27 – Liberar mesa - com comandas

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU27                                                                      |
| Nome           | Liberar mesa - com comandas                                               |
| Objetivo       | Verificar se o programa impede a liberação de uma mesa com comandas abertas |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função liberar mesa                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Se a mesa possui comandas abertas ela não é liberada / Realizado: Se a mesa possui comandas abertas ela não é liberada |

---

### TU28 – Liberar mesa com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU28                                                                      |
| Nome           | Liberar mesa com sucesso                                                  |
| Objetivo       | Verificar se o sistema consegue liberar mesas com sucesso                 |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função liberar mesa                                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Se a mesa não possui comandas abertas ela é liberada / Realizado: Se a mesa não possui comandas abertas ela é liberada |

---

### TU29 – Cadastrar usuário com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU29                                                                      |
| Nome           | Cadastrar usuário com sucesso                                             |
| Objetivo       | Verificar se o sistema pode cadastrar um usuário                          |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função cadastrar usuário                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cadastrar um usuário com sucesso / Realizado: Cadastrar um usuário com sucesso |

---

### TU30 – Cadastrar usuário - campos inválidos

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU30                                                                      |
| Nome           | Cadastrar usuário - campos inválidos                                      |
| Objetivo       | Verificar se o sistema pode determinar se os campos foram preenchidos corretamente, enviando mensagem de aviso ao usuário |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função cadastrar usuário                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Falha ao cadastrar um usuário / Realizado: Falha ao cadastrar um usuário |

---

### TU31 – Autenticar login com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU31                                                                      |
| Nome           | Autenticar login com sucesso                                              |
| Objetivo       | Verificar se os dados inseridos correspondem aos dados cadastrados, direcionando o usuário à página desejada |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função autenticar usuário                                |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Autentique os dados do usuário / Realizado: Autentique os dados do usuário |

---

### TU32 – Autenticar login - dados incorretos

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU32                                                                      |
| Nome           | Autenticar login - dados incorretos                                       |
| Objetivo       | Verificar que os dados inseridos não correspondem aos dados cadastrados, enviando mensagem de erro ao usuário |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função autenticar usuário                                |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Falha ao autenticar / Realizado: Falha ao autenticar            |

---

### TU33 – Logout com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU33                                                                      |
| Nome           | Logout com sucesso                                                        |
| Objetivo       | Verificar que o logout pode ser realizado pelo usuário                    |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função logout do usuário                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Usuário pode logout de seu perfil / Realizado: Usuário pode logout de seu perfil |

---

### TU34 – Editar usuário com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU34                                                                      |
| Nome           | Editar usuário com sucesso                                                |
| Objetivo       | Verificar se o usuário pode ser editado                                   |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função editar usuário                                    |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Dados do usuário foram editados / Realizado: Dados do usuário foram editados |

---

### TU35 – Editar usuário - campos inválidos

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU35                                                                      |
| Nome           | Editar usuário - campos inválidos                                         |
| Objetivo       | Verificar se o sistema pode determinar se os campos editados foram preenchidos corretamente |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função editar usuário                                    |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Dados do usuário não puderam ser editados / Realizado: Dados do usuário não puderam ser editados |

---

### TU36 – Deletar usuário com sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU36                                                                      |
| Nome           | Deletar usuário com sucesso                                               |
| Objetivo       | Verificar se o sistema pode deletar um usuário quando solicitado          |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função deletar usuário                                   |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: O usuário foi deletado / Realizado: O usuário foi deletado      |

---

### TU37 – Listar usuários

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU37                                                                      |
| Nome           | Listar usuários                                                           |
| Objetivo       | Verificar se o sistema consegue listar os usuários                        |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função listar usuários                                   |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Listar usuários / Realizado: Lista usuários                     |

---

### TU38 – Visualizar usuário

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU38                                                                      |
| Nome           | Visualizar usuário                                                        |
| Objetivo       | Verificar se o sistema pode visualizar o usuário                          |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função visualizar usuário                                |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Visualização do usuário / Realizado: Visualização do usuário    |

---

### TU39 – Listar Comandas Independentemente

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU39                                                                      |
| Nome           | Listar Comandas Independentemente                                         |
| Objetivo       | Listar comandas independentemente da situação de status da comanda        |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Método de criação de comandas                                             |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Lista todas as comandas independente de status / Realizado: Lista todas as comandas independente de status |

---

### TU40 – Cadastro de segundo administrador impedido

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU40                                                                      |
| Nome           | Cadastro de segundo administrador impedido                                |
| Objetivo       | Impede a criação de um segundo administrador                              |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da criação do tipo "administrador"                          |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Impedir a criação de um segundo administrador / Realizado: Impedir a criação de um segundo administrador |

---

### TU41 – Usuário comum impedido de cadastrar usuário

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU41                                                                      |
| Nome           | Usuário comum impedido de cadastrar usuário                               |
| Objetivo       | Impedir que um usuário comum cadastre um novo usuário válido              |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação de função para cadastro de novo usuário                     |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Impedir a criação de um novo usuário por um usuário não administrador / Realizado: Impedir a criação de um novo usuário |

---

### TU42 – Editar usuário - promoção para admin não permitida

*(Nota: TU42 foi renomeado no PDF, mas mantive a sequência conforme documento)*

---

### TU43 – Editar próprio admin - rebaixar cargo não permitido

---

### TU44 – Deletar usuário - senha admin incorreta

---

### TU45 – Usuário comum não pode deletar usuário

---

### TU46 – Admin tentar se auto deletar - não permitido

---

### TU47 – Validar CPF

---

### TU48 – Contra fluxo - status comanda

---

### TU49 – Tempo decorrido

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU49                                                                      |
| Nome           | Tempo decorrido                                                           |
| Objetivo       | Verificar a precisão do cálculo cronológico (subtração e fuso horário) do tempo de cozinha |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Comanda com registro de tempo de entrada (timezone-aware/naive)           |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Diferença temporal calculada e formatada corretamente em minutos e segundos / Realizado: Conforme previsto |

---

### TU50 – Cancelar comanda via edição

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU50                                                                      |
| Nome           | Cancelar comanda via edição                                               |
| Objetivo       | Cancelar comanda por edição dela                                          |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função de editar comanda                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Conseguir cancelar comanda na edição / Realizado: Consegue      |

---

### TU51 – Estatísticas diárias

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU51                                                                      |
| Nome           | Estatísticas diárias                                                      |
| Objetivo       | Verificar a filtragem precisa de dados financeiros e operacionais isolados para o dia atual |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Existência de comandas ativas, canceladas e de datas anteriores para contraste |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cálculo exato ignorando dias anteriores e isolando itens não cancelados no faturamento / Realizado: Conforme previsto |

---

### TU52 – Comanda cancelada - faturamento zero

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU52                                                                      |
| Nome           | Comanda cancelada - faturamento zero                                      |
| Objetivo       | Não gerar fatura ao cancelar comanda                                      |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação de cancelar comanda                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não gerar fatura ao cancelar comanda / Realizado: Não gera fatura ao cancelar comanda |

---

### TU53 – Fechamento de muitas comandas na mesma mesa

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU53                                                                      |
| Nome           | Fechamento de muitas comandas na mesma mesa                               |
| Objetivo       | Conseguir fechar diversas comandas na mesma mesa                          |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função de fechar comanda                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Conseguir fechar diversas comandas na mesma mesa / Realizado: Consegue fechar diversas comandas na mesma mesa |

---

### TU54 – Abrir comanda por cozinha deve falhar

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU54                                                                      |
| Nome           | Abrir comanda por cozinha deve falhar                                     |
| Objetivo       | Não permitir que a cozinha consiga gerar uma comanda                      |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de abrir comanda devidamente implementada                          |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cozinha não consegue abrir comanda / Realizado: Cozinha não consegue abrir comanda |

---

### TU55 – Adicionar item por cozinheiro deve falhar

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU55                                                                      |
| Nome           | Adicionar item por cozinheiro deve falhar                                 |
| Objetivo       | Não permitir que o usuário cozinha não consiga adicionar itens na comanda |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de adicionar item devidamente implementada                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cozinha não consegue adicionar item / Realizado: Cozinha não consegue adicionar item |

---

### TU56 – Editar comanda - edição por cozinheiro

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU56                                                                      |
| Nome           | Editar comanda - edição por cozinheiro                                    |
| Objetivo       | Verificar se o programa impede que o cozinheiro edite uma comanda         |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função editar comanda                                    |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Usuário cozinha não conseguiria editar uma comanda / Realizado: Usuário cozinha não consegue editar uma comanda |

---

### TU57 – Enviar comanda por cozinheiro deve falhar

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU57                                                                      |
| Nome           | Enviar comanda por cozinheiro deve falhar                                 |
| Objetivo       | Cozinha não consegue enviar comanda                                       |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de enviar comanda bem implementada                                 |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cozinha não conseguir enviar comanda / Realizado: Cozinha não consegue enviar comanda |

---

### TU58 – Fechar comanda por cozinheiro deve falhar

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU58                                                                      |
| Nome           | Fechar comanda por cozinheiro deve falhar                                 |
| Objetivo       | Cozinha não consegue fechar comanda                                       |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de fechar comanda devidamente implementada                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Cozinha não conseguir fechar comanda / Realizado: Cozinha não consegue fechar comanda |

---

### TU59 – Status finalizado bloqueia alteração

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU59                                                                      |
| Nome           | Status finalizado bloqueia alteração                                      |
| Objetivo       | Não permitir alteração na comanda com status finalizado                   |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação do status finalizado                                        |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Bloquear alteração de comanda finalizada / Realizado: Bloqueia alteração de comanda finalizada |

---

### TU60 – Cadastrar produto - negado para garçom

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU60                                                                      |
| Nome           | Cadastrar produto - negado para garçom                                    |
| Objetivo       | Garçom não consegue cadastrar produto                                     |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de cadastrar produto devidamente implementada                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir que garçom cadastre produto / Realizado: Não permite que garçom cadastre produto |

---

### TU61 – Cadastrar produto - negado para cozinha

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU61                                                                      |
| Nome           | Cadastrar produto - negado para cozinha                                   |
| Objetivo       | Cozinha não consegue cadastrar produto                                    |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de cadastrar produto devidamente implementada                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir que cozinha cadastre produto / Realizado: Não permite que cozinha cadastre produto |

---

### TU62 – Editar produto - negado

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU62                                                                      |
| Nome           | Editar produto - negado                                                   |
| Objetivo       | Negar edição do produto por usuários diferentes do administrador          |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de editar produto devidamente implementada                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Negar edição de produto por usuários que não sejam administradores / Realizado: Nega edição de produto por usuários que não são administradores |

---

### TU63 – Deletar produto - negado

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU63                                                                      |
| Nome           | Deletar produto - negado                                                  |
| Objetivo       | Não permitir que usuários que não são administradores consigam deletar produtos |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de deletar produto devidamente implementada                        |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Negar deletar produto para não administradores / Realizado: Nega deletar produto para não administradores |

---

### TU64 – Criar mesa com capacidade inválida

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU64                                                                      |
| Nome           | Criar mesa com capacidade inválida                                        |
| Objetivo       | Não permitir a criação de uma mesa com capacidade inválida                |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de criar mesa devidamente implementada                             |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir criar mesas com capacidade inválida / Realizado: Não permite criar mesas com capacidade inválida |

---

### TU65 – Comanda fantasma (inexistente) - fechamento zerado

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU65                                                                      |
| Nome           | Comanda fantasma (inexistente) - fechamento zerado                        |
| Objetivo       | Ignorar comandas canceladas nas estatísticas diárias                      |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de estatísticas diárias devidamente implementada                   |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Ignorar comandas canceladas no cálculo de estatísticas diárias / Realizado: Ignora comandas canceladas no cálculo de estatísticas diárias |

---

### TU66 – Editar usuário - promover para admin não permitido

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU66                                                                      |
| Nome           | Editar usuário - promover para admin não permitido                        |
| Objetivo       | Não permite promover usuário à administrador                              |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação de verificação de usuário                                   |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não ter como promover usuários comuns como admins / Realizado:  |

---

### TU67 – Editar próprio admin - rebaixar cargo não permitido

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU67                                                                      |
| Nome           | Editar próprio admin - rebaixar cargo não permitido                       |
| Objetivo       | Não é permitido rebaixar o cargo de administrador                         |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de editar usuário devidamente implementada                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir rebaixar admin / Realizado: Não permite rebaixar admin |

---

### TU68 – Deletar usuário - senha admin incorreta

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU68                                                                      |
| Nome           | Deletar usuário - senha admin incorreta                                   |
| Objetivo       | Não permitir administrador deletar usuário se a senha estiver incorreta   |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de deletar usuário devidamente implementada                        |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Administrador não conseguir deletar usuário se a senha estiver incorreta / Realizado: Administrador não consegue deletar usuário se a senha está incorreta |

---

### TU69 – Usuário comum não pode deletar usuário

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU69                                                                      |
| Nome           | Usuário comum não pode deletar usuário                                    |
| Objetivo       | Verificar se um usuário comum não pode deletar outros                     |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Função de deletar usuário devidamente implementada                        |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Usuário comum não conseguir deletar usuário / Realizado: Usuário comum não deleta usuário |

---

### TU70 – Admin tentar se auto deletar - não permitido

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU70                                                                      |
| Nome           | Admin tentar se auto deletar - não permitido                              |
| Objetivo       | Não permitir que administrador se delete                                  |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica do administrador bem implementada                                  |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Não permitir que administrador se delete / Realizado: Não permite que administrador se delete |

---

### TU71 – Validar CPF

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU71                                                                      |
| Nome           | Validar CPF                                                               |
| Objetivo       | Verificar se é possível validar o CPF                                     |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Implementação da função de validar CPF                                    |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Conseguir validar CPF / Realizado: Consegue validar CPF         |

---

### TU72 – Contra fluxo - status comanda

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TU72                                                                      |
| Nome           | Contra fluxo - status comanda                                             |
| Objetivo       | Verificar se é possível voltar o status de um pedido                      |
| Nível          | Unitário                                                                  |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica de fluxo bem implementada                                          |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Conseguir voltar status do pedido / Realizado: Consegue voltar status do pedido |

---

## Testes Integrados

### TI01 – Integração entre backend e banco de dados

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI01                                                                      |
| Nome           | Integração entre backend e banco de dados                                 |
| Objetivo       | Verificar se o sistema armazena corretamente dados do banco               |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Banco de dados ativo e conexão configurada                                |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: autenticação bem-sucedida / Realizado: autenticação foi bem-sucedida |

---

### TI02 – Integração entre backend e frontend

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI02                                                                      |
| Nome           | Integração entre backend e frontend                                       |
| Objetivo       | Verificar se a interface consegue enviar e receber dados do programa      |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Interface funcional e conectado à lógica do programa                      |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: autenticação bem-sucedida / Realizado: autenticação foi bem-sucedida |

---

### TI03 – Integração entre abertura de comanda e banco de dados

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI03                                                                      |
| Nome           | Integração entre abertura de comanda e banco de dados                     |
| Objetivo       | Verificar se o ato de abrir a comanda está integrado com o banco de dados |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao abrir comanda / Realizado: Sucesso ao abrir comanda  |

---

### TI04 – Adicionar Item na Comanda

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI04                                                                      |
| Nome           | Adicionar Item na Comanda                                                 |
| Objetivo       | Verificar se a função de adicionar item à comanda está de acordo          |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao adicionar um item à comanda / Realizado: Sucesso ao adicionar um item à comanda |

---

### TI05 – Listar a fila da cozinha com o cozinheiro

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI05                                                                      |
| Nome           | Listar a fila da cozinha com o cozinheiro                                 |
| Objetivo       | Verificar se o cozinheiro consegue listar a fila da cozinha               |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao listar a fila da cozinha como cozinheiro / Realizado: Sucesso ao listar a fila da cozinha como cozinheiro |

---

### TI06 – Listar a fila da cozinha com o garçom

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI06                                                                      |
| Nome           | Listar a fila da cozinha com o garçom                                     |
| Objetivo       | Verificar se o garçom consegue listar a fila da cozinha                   |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao listar a fila da cozinha como garçom / Realizado: Sucesso ao listar a fila da cozinha como garçom |

---

### TI07 – Fluxo completo da Comanda

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI07                                                                      |
| Nome           | Fluxo completo da Comanda                                                 |
| Objetivo       | Verificar se todas as funções que abrangem a comanda estão integradas e funcionando |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Todas as lógicas necessárias perfeitamente implementadas                   |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso na depuração das funções / Realizado: Sucesso na depuração das funções |

---

### TI08 – Contrafluxo Status Comanda

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI08                                                                      |
| Nome           | Contrafluxo Status Comanda                                                |
| Objetivo       | Verifica se o garçom consegue restaurar um status acidentalmente alterado |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao restaurar status / Realizado: Sucesso ao restaurar status |

---

### TI09 – Tentar alterar status após finalizado (falha)

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI09                                                                      |
| Nome           | Tentar alterar status após finalizado (falha)                             |
| Objetivo       | Verificar se após a comanda estar com status de finalizada, é possível alterar o status ainda (esperado é não conseguir) |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir alterar o status da comanda finalizada / Realizado: Sucesso ao não conseguir alterar o status da comanda finalizada |

---

### TI10 – Banco de Dados Fantasma - Comanda

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI10                                                                      |
| Nome           | Banco de Dados Fantasma - Comanda                                         |
| Objetivo       | Verificar se é possível modificar as informações de uma comanda fantasma  |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao modificar as informações de uma comanda fantasma / Realizado: Sucesso ao modificar as informações de uma comanda fantasma |

---

### TI11 – Alteração do Preço do Produto com Comanda Aberta mantém o preço

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI11                                                                      |
| Nome           | Alteração do Preço do Produto com Comanda Aberta mantém o preço           |
| Objetivo       | Verificar se o preço do produto na comanda aberta não é alterado quando o preço do produto é modificado |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Preço mantido na comanda / Realizado: Preço mantido na comanda  |

---

### TI12 – Listar Produtos com Sucesso

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI12                                                                      |
| Nome           | Listar Produtos com Sucesso                                               |
| Objetivo       | Verificar se a função de listar todos os produtos está funcionando perfeitamente |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao listar os produtos / Realizado: Sucesso ao listar os produtos |

---

### TI13 – Cadastrar Produto como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI13                                                                      |
| Nome           | Cadastrar Produto como Administrador                                      |
| Objetivo       | Verificar se o administrador consegue cadastrar um produto normalmente    |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao cadastrar um produto como administrador / Realizado: Sucesso ao cadastrar um produto como administrador |

---

### TI14 – Deletar Produto como Garçom (Acesso Negado)

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI14                                                                      |
| Nome           | Deletar Produto como Garçom (Acesso Negado)                               |
| Objetivo       | Verificar se um garçom é capaz de deletar um produto (o esperado é não conseguir) |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir deletar um produto como garçom / Realizado: Sucesso ao não conseguir deletar um produto como garçom |

---

### TI15 – Listar Produtos por Categoria

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI15                                                                      |
| Nome           | Listar Produtos por Categoria                                             |
| Objetivo       | Verificar se a função de listar produtos por categoria está funcionando normalmente |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao listar produtos por categoria / Realizado: Sucesso ao listar produtos por categoria |

---

### TI16 – Editar Produto como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI16                                                                      |
| Nome           | Editar Produto como Administrador                                         |
| Objetivo       | Verificar se o administrador consegue editar um produto normalmente       |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao editar um produto como administrador / Realizado: Sucesso ao editar um produto como administrador |

---

### TI17 – Deletar Produto como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI17                                                                      |
| Nome           | Deletar Produto como Administrador                                        |
| Objetivo       | Verificar se o administrador consegue deletar um produto normalmente      |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao deletar um produto como administrador / Realizado: Sucesso ao deletar um produto como administrador |

---

### TI18 – Listar Mesas como Garçom

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI18                                                                      |
| Nome           | Listar Mesas como Garçom                                                  |
| Objetivo       | Verificar se o garçom é capaz de listar as mesas                          |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao listar mesas como garçom / Realizado: Sucesso ao listar mesas como garçom |

---

### TI19 – Criar Mesa como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI19                                                                      |
| Nome           | Criar Mesa como Administrador                                             |
| Objetivo       | Verificar se o administrador consegue criar mesas normalmente             |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao criar mesa como administrador / Realizado: Sucesso ao criar mesa como administrador |

---

### TI20 – Criar Mesa como Garçom (Acesso Negado)

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI20                                                                      |
| Nome           | Criar Mesa como Garçom (Acesso Negado)                                    |
| Objetivo       | Verificar se o garçom consegue criar mesas (o esperado é não conseguir)   |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir criar uma mesa como garçom / Realizado: Sucesso ao não conseguir criar uma mesa como garçom |

---

### TI21 – Editar Mesa como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI21                                                                      |
| Nome           | Editar Mesa como Administrador                                            |
| Objetivo       | Verificar se o administrador consegue editar mesas normalmente            |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao editar mesa como administrador / Realizado: Sucesso ao editar mesa como administrador |

---

### TI22 – Deletar Mesa com Comanda Ativa Deve Falhar

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI22                                                                      |
| Nome           | Deletar Mesa com Comanda Ativa Deve Falhar                                |
| Objetivo       | Verificar se é possível deletar uma mesa com comanda ativa (o esperado é não conseguir) |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir deletar uma mesa com comanda ativa / Realizado: Sucesso ao não conseguir deletar uma mesa com comanda ativa |

---

### TI23 – Tolerância de Dados Inválidos de Capacidade da Mesa

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI23                                                                      |
| Nome           | Tolerância de Dados Inválidos de Capacidade da Mesa                       |
| Objetivo       | Verificar se a tolerância de dados inválidos atribuídos à capacidade de uma mesa está sendo atendida |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao atender a tolerância de dados inválidos de uma mesa / Realizado: Sucesso ao atender a tolerância de dados inválidos de uma mesa |

---

### TI24 – Login Bem Sucedido Retorna Dados do Usuário

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI24                                                                      |
| Nome           | Login Bem Sucedido Retorna Dados do Usuário                               |
| Objetivo       | Verificar se os dados do usuário estão retornando corretamente após um login bem sucedido |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso retornar os dados do usuário após um login bem-sucedido / Realizado: Sucesso retornar os dados do usuário após um login |

---

### TI25 – Acesso Negado Sem Login

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI25                                                                      |
| Nome           | Acesso Negado Sem Login                                                   |
| Objetivo       | Verificar se caso o login não seja bem sucedido, o acesso será negado     |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir acessar o sistema após um login falho / Realizado: Sucesso ao não conseguir acessar o sistema após um login falho |

---

### TI26 – Logout Limpa Sessão

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI26                                                                      |
| Nome           | Logout Limpa Sessão                                                       |
| Objetivo       | Verificar se após um logout, a sessão é automaticamente limpa             |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sessão limpa após logout / Realizado: Sessão limpa após logout  |

---

### TI27 – Listar Usuários como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI27                                                                      |
| Nome           | Listar Usuários como Administrador                                        |
| Objetivo       | Verificar se o administrador consegue listar todos os usuários do sistema normalmente |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao listar usuários como administrador / Realizado: Sucesso ao listar usuários como administrador |

---

### TI28 – Listar Usuários como Garçom (Acesso Negado)

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI28                                                                      |
| Nome           | Listar Usuários como Garçom (Acesso Negado)                               |
| Objetivo       | Verificar se o garçom consegue listar os usuários do sistema (o esperado é não conseguir) |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir listar usuários como garçom / Realizado: Sucesso ao não conseguir listar usuários como garçom |

---

### TI29 – Cadastrar Usuário

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI29                                                                      |
| Nome           | Cadastrar Usuário                                                         |
| Objetivo       | Verificar se a função de cadastro de usuário está funcionando normalmente |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao cadastrar um usuário / Realizado: Sucesso ao cadastrar um usuário |

---

### TI30 – Editar Usuário como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI30                                                                      |
| Nome           | Editar Usuário como Administrador                                         |
| Objetivo       | Verificar se o administrador consegue editar um usuário normalmente       |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao editar um usuário como administrador / Realizado: Sucesso ao editar um usuário como administrador |

---

### TI31 – Deletar o Próprio Usuário de Administrador (Bloqueado)

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI31                                                                      |
| Nome           | Deletar o Próprio Usuário de Administrador (Bloqueado)                    |
| Objetivo       | Verificar se o administrador consegue deletar a si mesmo do sistema (o esperado é não conseguir) |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao não conseguir deletar a si mesmo / Realizado: Sucesso ao não conseguir deletar a si mesmo |

---

### TI32 – Finalizar Dia como Administrador

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI32                                                                      |
| Nome           | Finalizar Dia como Administrador                                          |
| Objetivo       | Verificar se o administrador é capaz de encerrar o fluxo diário normalmente |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao finalizar o dia como administrador / Realizado: Sucesso ao finalizar o dia como administrador |

---

### TI33 – Banco de Dados Fantasma - Usuário

| Campo          | Conteúdo                                                                  |
|----------------|---------------------------------------------------------------------------|
| Código         | TI33                                                                      |
| Nome           | Banco de Dados Fantasma - Usuário                                         |
| Objetivo       | Verificar se o usuário consegue operar com um banco de dados fantasma     |
| Nível          | Integração                                                                |
| Tipo           | Funcional                                                                 |
| Precondições   | Lógica perfeitamente implementada                                         |
| Estado         | Aprovado                                                                  |
| Resultados     | Previsto: Sucesso ao conseguir operar um usuário com um banco de dados fantasma / Realizado: Sucesso ao conseguir operar um usuário com um banco de dados fantasma |