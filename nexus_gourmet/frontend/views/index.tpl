% rebase('layout.tpl', title='Bem-vindo ao NextBook')

<div class="welcome-container">
    <section class="hero-section">
        <h1>Bem-vindo ao NextBook: sua biblioteca, sua paixão, em um só lugar.</h1>
        <p class="subtitle">
            Para todo amante de livros, cada obra é um tesouro, uma porta para um novo mundo. Mas, com o tempo, nossa coleção cresce e a organização pode se tornar um desafio. Onde está aquele livro que você tanto amou? Para quem você emprestou sua edição favorita? Qual o próximo livro da sua lista de desejos?
        </p>
        <p>
            O <strong>NextBook</strong> nasceu para responder a essas perguntas. Somos uma plataforma completa e intuitiva, criada por e para apaixonados por leitura, com um único objetivo: ajudar você a transformar sua coleção de livros em uma biblioteca pessoal perfeitamente organizada e acessível.
        </p>
    </section>

    <section class="features-section">
        <h2>Com o NextBook, você pode:</h2>
        <ul class="features-list">
            <li>
                <span class="emoji">📚</span>
                <div>
                    <strong>Catalogar sua coleção completa:</strong> Adicione seus livros com informações detalhadas como capa, autor, gênero, ano de publicação e até suas anotações pessoais. Tenha todo o seu acervo na palma da sua mão.
                </div>
            </li>
            <li>
                <span class="emoji">🤝</span>
                <div>
                    <strong>Controlar empréstimos com facilidade:</strong> Registre para quem você emprestou um livro e defina uma data de devolução. Nunca mais perca um livro de vista!
                </div>
            </li>
            <li>
                <span class="emoji">✨</span>
                <div>
                    <strong>Criar sua lista de desejos:</strong> Viu um livro interessante? Adicione-o à sua lista de desejos para não esquecer e planejar suas próximas aventuras literárias.
                </div>
            </li>
            <li>
                <span class="emoji">🔍</span>
                <div>
                    <strong>Encontrar qualquer livro em segundos:</strong> Use nossa busca inteligente para localizar títulos em sua estante virtual de forma rápida e precisa.
                </div>
            </li>
        </ul>
    </section>

    <section class="closing-section">
        <p>
            Seja você um leitor casual, um colecionador dedicado ou o responsável por uma pequena biblioteca comunitária, o NextBook é a ferramenta que faltava para você redescobrir o prazer de ter seus livros sempre por perto e em perfeita ordem.
        </p>
        <p class="call-to-action">
            Junte-se a nós e comece a construir sua biblioteca digital hoje mesmo. Sua próxima história começa aqui.
        </p>
    </section>

    <section class="featured-books-section">
        <h2>Livros em Destaque</h2>
            % if livros:
            <div class="book-grid">
                % for livro in livros:
                <div class="book-card">
                    <div class="book-card-img-container">
                        <img src="/static/uploads/{{livro.image_url}}" alt="Capa do livro {{livro.name}}" class="book-card-img">
                    </div>
                    <div class="book-card-body">
                        <h3 class="book-card-title">{{livro.name}}</h3>
                        <p class="book-card-author">{{livro.author}}</p>
                        <p class="book-card-year">{{livro.year}}</p>
                        <div class="book-card-availability {{'available' if livro.is_available else 'unavailable'}}">
                            {{'Disponível' if livro.is_available else 'Indisponível'}}
                        </div>
                    </div>
                </div>
                % end
            </div>
        % else:
            <div style="text-align: center; padding: 2rem 0; color: #6c757d;">
                 <p>Ainda não há livros em destaque.</p>
            </div>
        % end
    </section>
</div>