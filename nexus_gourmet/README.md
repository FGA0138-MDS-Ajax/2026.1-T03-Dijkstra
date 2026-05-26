# Nexus Gourmet

Repositório oficial do projeto **Nexus Gourmet**, desenvolvido pela equipe Dijkstra para a disciplina de **Métodos de Desenvolvimento de Software (MDS)**, lecionada pelo professor Ricardo Ajax.

## 🌿 Estrutura de Branches
O repositório foi planejado e estruturado com as seguintes branches principais:
* **`main`**: Branch usada exclusivamente para a versão de produção do software da equipe.
* **`developer`**: Usada como um intermediário antes do código chegar realmente para produção. É o ambiente ideal para realizar os últimos testes antes das apresentações.
* **`docs`**: Usada para armazenar a documentação do projeto.
* **`gh-pages`**: Local dos arquivos estáticos de deploy da documentação.

## 📚 Documentação (MkDocs)
Este repositório é estruturado para que sejam realizadas as documentações de software. 
* Utilizamos a ferramenta **MkDocs** para gerar a documentação baseada em arquivos Markdown.
* A estilização é feita utilizando o **Material Theme**.
* O repositório conta com uma pipeline de automação de deploy. A cada commit feito, a pipeline gera uma versão atualizada da documentação no GitPages em minutos.

## 💻 Sobre a Aplicação (Nexus Gourmet)
O Nexus Gourmet utiliza o microframework **Bottle** em Python, focado em fornecer uma base simples, extensível e didática orientada a objetos (Arquitetura MVC). A persistência de dados é feita de forma leve através de arquivos JSON.

### Estrutura de Pastas
```text
nexus_gourmet/
 ├── .sessions/         # Ponto de persistência de dados de sessão de cada usuário
 ├── app.py             # Configuração e ponto de entrada da aplicação
 ├── config.py          # Configurações globais e caminhos do projeto
 ├── main.py            # Inicialização da aplicação web
 ├── requirements.txt   # Dependências do projeto (bottle, pylint, werkzeug, beaker)
 ├── Makefile           # Atalhos de comandos para gerenciamento e linting
 ├── controllers/       # Controladores e rotas da aplicação (ex: auth_controller.py)
 ├── models/            # Definição das entidades do sistema
 ├── services/          # Regras de negócio e lógica de persistência
 ├── views/             # Arquivos de template HTML (.tpl)
 ├── static/            # Arquivos estáticos como CSS, JS e imagens
 └── data/              # Arquivos .json simulando o banco de dados
 
## ▶️ Como Executar

1. Clone o repositório:
```bash
git clone <url-do-seu-repositorio>
cd nexus_gourmet
```

2. Crie o ambiente virtual na pasta fora do seu projeto:
```bash
python -m venv venv
source venv/bin/activate  # No Linux/Mac
venv\Scripts\activate     # No Windows
```

3. Entre dentro do seu projeto criado a partir do template e instale as dependências:
```bash
pip install -r requirements.txt
```

4. Rode a aplicação:
```bash
python main.py
```

5. Accese sua aplicação no navegador em: [http://localhost:1422](http://localhost:1422)

---

## 🧠 Autor e Licença
