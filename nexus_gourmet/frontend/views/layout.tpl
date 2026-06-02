<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NextBook</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="icon" type="image/png" href="/static/img/FaviconNextBook.png">
</head>
<body>
    <header>
        <nav>
            <div class="nav-left">
                <a href="/"><img id="logoNextBook" src="/static/img/logoNextBook.png" alt="Logo NextBook"></a>
                <a href="/livros">Acervo</a>
                % if session and session.get('user_type') in ['Admin', 'Dono']:
                    <a href="/users">Usuários</a>
                % end
            </div>

            <div class="nav-center">
                <form action="/livros/search" method="get" class="search-form">
                    <input type="text" name="query" placeholder="Pesquisar por título ou autor..." class="search-input">
                    <button type="submit" class="search-button">Pesquisar</button>
                </form>
            </div>

            <div class="nav-right">
                % if not defined('hide_auth_buttons'):
                    % if not session or not session.get('user_id'):
                        <a href="/register" class="button button-success">Registrar</a>
                        <a href="/login" class="button button-primary">Entrar</a>
                    % else:
                        <div class="user-menu">
                            <button class="user-menu-button">
                                <img src="/static/img/perfil.png" alt="User Icon">
                                <span>{{session.get('user_name', 'Usuário')}}</span>
                            </button>
                            <div class="dropdown-content">
                                <a href="/perfil">Perfil</a>
                                <a href="/meus-livros">Meus livros</a>
                                <a href="/minha-lista-desejos">Lista de desejos</a>
                                <a href="/logout">Sair</a>
                            </div>
                        </div>
                    % end
                % end
            </div>
        </nav>
    </header>

    <main class="container">
        {{!base}}
    </main>

    <footer class="site-footer">
        <div class="footer-container">
            <div class="footer-column">
                <h4>Sobre o NextBook</h4>
                <p>O NextBook é um projeto acadêmico da disciplina de Programação Orientada a Objetos, criado para aplicar conceitos da matéria em uma plataforma funcional para amantes de livros.</p>
            </div>

            <div class="footer-column">
                <h4>Navegação</h4>
                <ul>
                    <li><a href="/">Página Inicial</a></li>
                    <li><a href="/livros">Acervo de Livros</a></li>
                    <li><a href="/perfil">Meu Perfil</a></li>
                    % if session and session.get('user_type') in ['Admin', 'Dono']:
                        <li><a href="/users">Gerenciar Usuários</a></li>
                    % end
                </ul>
            </div>

            <div class="footer-column">
                <h4>Desenvolvedores</h4>
                <div class="social-links-improved">
                    <a href="https://www.instagram.com/lucao._ferreira/" target="_blank" rel="noopener noreferrer" class="social-link-item">
                        <img src="/static/img/IconeInstagram.png" alt="Instagram" class="social-icon">
                        <span>Lucas Ferreira Santana</span>
                    </a>
                    <a href="https://www.instagram.com/luc14_pero/" target="_blank" rel="noopener noreferrer" class="social-link-item">
                        <img src="/static/img/IconeInstagram.png" alt="Instagram" class="social-icon">
                        <span>Lucas Peixoto Rodrigues</span>
                    </a>
                </div>
            </div>
        </div>

        <div class="footer-bottom-bar">
            <p>&copy; 2025 NextBook. Todos os direitos reservados.</p>
        </div>
    </footer>
    <script src="/static/js/main.js"></script>
</body>
</html>