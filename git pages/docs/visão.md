<h1 id="documento-de-visao">Documento de Visão</h1>

<p><strong>Nexus Gourmet</strong></p>

<p>Versão 1.1</p>

## Integrantes do Grupo

<table class="doc-table doc-table--md">
  <thead>
    <tr>
      <th>Matrícula</th>
      <th>Nome</th>
      <th>Função (responsabilidade)</th>
      <th>Pontos de participação</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>242004457</td><td>Alexandre Henrique Almeida Valadares Sousa</td><td>Banco de dados</td><td>10</td></tr>
    <tr><td>242028655</td><td>Davi Kenichi Watanabe Sakai</td><td>Frontend</td><td>10</td></tr>
    <tr><td>241025953</td><td>Igor Lima Carneiro</td><td>Backend</td><td>10</td></tr>
    <tr><td>242005329</td><td>Jhonatan William Araújo de Almeida</td><td>Banco de dados</td><td>10</td></tr>
    <tr><td>242015432</td><td>João Gabriel Rolim Veiga</td><td>Backend</td><td>10</td></tr>
    <tr><td>241039322</td><td>João Paulo Jacomini Batista</td><td>Frontend</td><td>10</td></tr>
    <tr><td>241039304</td><td>João Victor Amorim Kurihara</td><td>Frontend</td><td>10</td></tr>
    <tr><td>242024253</td><td>Lucas Ferreira Santana</td><td>Backend</td><td>10</td></tr>
    <tr><td>242024271</td><td>Lucas Peixoto Rodrigues</td><td>Backend</td><td>10</td></tr>
    <tr><td>242005006</td><td>Rafael de Aquino Marinho</td><td>Frontend</td><td>10</td></tr>
  </tbody>
</table>

## Histórico de Revisões

<table class="doc-table">
  <thead>
    <tr>
      <th>Data</th>
      <th>Versão</th>
      <th>Descrição</th>
      <th>Autor</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>30/04/2026</td><td>1.0</td><td>Criação da primeira versão do documento</td><td>Grupo Dijkstra</td></tr>
    <tr><td>02/06/2026</td><td>1.1</td><td>Adicionado menções diretas às fontes bibliográficas usadas no corpo do documento e atualização dos sprints</td><td>Grupo Dijkstra</td></tr>
  </tbody>
</table>

<hr />

## Sumário

<ul>
  <li><a href="#1-visao-geral-do-produto">1 VISÃO GERAL DO PRODUTO</a>
    <ul>
      <li><a href="#11-problema">1.1 Problema</a></li>
      <li><a href="#12-declaracao-de-posicao-do-produto">1.2 Declaração de posição do produto</a></li>
      <li><a href="#13-objetivos-do-produto">1.3 Objetivos do Produto</a></li>
      <li><a href="#14-tecnologias-a-serem-utilizadas">1.4 Tecnologias a Serem Utilizadas</a></li>
    </ul>
  </li>
  <li><a href="#2-visao-geral-do-projeto">2 VISÃO GERAL DO PROJETO</a>
    <ul>
      <li><a href="#21-ciclo-de-vida-do-projeto">2.1 Ciclo de vida do projeto de desenvolvimento de software</a></li>
      <li><a href="#22-organizacao-do-projeto">2.2 Organização do Projeto</a></li>
      <li><a href="#23-planejamento-das-fases">2.3 Planejamento das Fases e/ou Iterações do Projeto</a></li>
      <li><a href="#24-matriz-de-comunicacao">2.4 Matriz de Comunicação</a></li>
      <li><a href="#25-gerenciamento-de-riscos">2.5 Gerenciamento de Riscos</a></li>
      <li><a href="#26-criterios-de-replanejamento">2.6 Critérios de Replanejamento</a></li>
    </ul>
  </li>
  <li><a href="#3-processo-de-desenvolvimento-de-software">3 PROCESSO DE DESENVOLVIMENTO DE SOFTWARE</a>
    <ul>
      <li><a href="#31-principais-praticas-adotadas">3.1 Principais Práticas Adotadas</a></li>
      <li><a href="#32-ferramentas-de-suporte">3.2 Ferramentas de Suporte</a></li>
    </ul>
  </li>
  <li><a href="#4-declaracao-de-escopo-do-projeto">4 DECLARAÇÃO DE ESCOPO DO PROJETO</a>
    <ul>
      <li><a href="#41-backlog-do-produto">4.1 Backlog do produto</a></li>
      <li><a href="#42-perfis">4.2 Perfis</a></li>
      <li><a href="#43-cenarios">4.3 Cenários</a></li>
      <li><a href="#44-tabela-de-backlog-do-produto">4.4 Tabela de Backlog do Produto</a></li>
    </ul>
  </li>
  <li><a href="#5-metricas-e-medicoes">5 MÉTRICAS E MEDIÇÕES</a>
    <ul>
      <li><a href="#51-gqm-de-medicoes">5.1 GQM de medições</a></li>
    </ul>
  </li>
  <li><a href="#6-testes-de-software">6 TESTES DE SOFTWARE</a>
    <ul>
      <li><a href="#61-estrategia-de-testes-contendo">6.1 Estratégia de testes contendo:</a></li>
      <li><a href="#62-roteiro-de-teste">6.2 Roteiro de teste:</a></li>
    </ul>
  </li>
  <li><a href="#7-referencias-bibliograficas">7. REFERÊNCIAS BIBLIOGRÁFICAS</a></li>
</ul>

<hr />

## 1. VISÃO GERAL DO PRODUTO

<h2 id="11-problema">1.1 Problema</h2>

<p>Segundo a Associação Brasileira de Bares e Restaurantes (ABRASEL, 2018), aproximadamente 50% dos estabelecimentos do setor encerram suas atividades em menos de dois anos de operação. A causa raiz desse declínio raramente está ligada à qualidade da comida, e sim decorrente de falhas na gestão de pedidos, descontrole de estoque e ineficiência na comunicação interna.</p>

<p>O gerenciamento manual de pedidos, baseado em comandas de papel e interações verbais, está fadado ao erro (ALELO, 2024). O fluxo de informações em um restaurante é dinâmico e demanda alta carga cognitiva, onde a perda de um único pedaço de papel pode significar a interrupção de toda a experiência do cliente e a perda direta de receita (CLOUDFY, 2025).</p>

<p>A anotação em papel é uma interface de entrada de dados de baixíssima fidelidade, sujeita a ambiguidades de caligrafia, falta de padronização em observações e total ausência de dados temporais. Sem o registro exato do momento em que o pedido foi feito, a cozinha perde a capacidade de medir o tempo médio de preparo, informação vital para a eficiência operacional do restaurante uma vez que a agilidade é um dos fatores mais valorizados pelos consumidores modernos.</p>

<p>Focando na falta de rastreabilidade, falhas de comunicação entre salão e cozinha e desorganização logística, conforme ilustrado na Figura 1, revela-se a necessidade de desenvolver um software que solucione a problemática do registro e acompanhamento de pedidos.</p>

<p>O sistema deve permitir a entrada de pedidos via dispositivos móveis (garçons) e enviá-los imediatamente para telas na cozinha, organizando-os por prioridade e tempo de preparo, eliminando a necessidade de impressoras, além de possuir interfaces intuitivas que exijam o mínimo de treinamento possível para a equipe, considerando a alta rotatividade de funcionários no setor de <em>foodservice</em>.</p>
Figura 1 - Ineficiência no registro e acompanhamento de pedidos
![Figura 1 - Ineficiência no registro e acompanhamento de pedidos](img/ishikawa.jpg)

<p><em>Fonte: realizado pelo autor (2026)</em></p>

<h2 id="12-declaracao-de-posicao-do-produto">1.2 Declaração de posição do produto</h2>

<p>A tabela 1 condensa o posicionamento estratégico do Nexus Gourmet, apresentando seu público-alvo, necessidade no ambiente, sua categoria e vantagens em relação às alternativas existentes.</p>

<p><strong>Tabela 1 - Posicionamento estratégico do produto</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th class="col-narrow">Item</th>
      <th>Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr><td><strong>Para</strong></td><td>Proprietários e funcionários de restaurantes de qualquer porte</td></tr>
    <tr><td><strong>Necessidade</strong></td><td>Registrar, acompanhar e gerenciar pedidos de forma centralizada, ágil e sem erros</td></tr>
    <tr><td><strong>O Nexus Gourmet</strong></td><td>É uma aplicação WEB - mobile denominada Nexus Gourmet</td></tr>
    <tr><td><strong>Que</strong></td><td>Permite o registro digital de pedidos por mesa, o acompanhamento do status em tempo real pela cozinha e o fechamento de conta pelos garçons</td></tr>
    <tr><td><strong>Ao contrário</strong></td><td>Do registro manual em papel e da comunicação verbal entre garçons e cozinha, que estão sujeitos a erros, perdas de informação e ausência de rastreabilidade</td></tr>
    <tr><td><strong>Nosso produto</strong></td><td>Integra o fluxo completo do pedido — do salão à cozinha — com atualização em tempo real, dispensando qualquer infraestrutura adicional além de um navegador web</td></tr>
  </tbody>
</table>

<p><em>Fonte: realizado pelo autor (2026)</em></p>

<h2 id="13-objetivos-do-produto">1.3 Objetivos do Produto</h2>

<p><strong>Objetivo Principal</strong></p>

<p>O Nexus Gourmet objetiva, principalmente, desenvolver um software que centralize o processo de registro, acompanhamento e gerenciamento de pedidos de restaurantes, eliminando a dependência de anotações manuais.</p>

<p><strong>Objetivos Secundários</strong></p>

<ul>
<li>Melhorar o gerenciamento de insumos consumidos pelo cliente.</li>
<li>Oferecer visibilidade em tempo real do status de cada pedido (NOX, 2025; OLITECNICA, 2025).</li>
<li>Facilitar o gerenciamento de mesas (THEFORKMANAGER, 2025).</li>
<li>Automatizar o cálculo e a geração da conta ao final do atendimento.</li>
</ul>

<h2 id="14-tecnologias-a-serem-utilizadas">1.4 Tecnologias a Serem Utilizadas</h2>

<p><strong>Frontend:</strong> HTML, CSS &amp; JavaScript</p>

<p><strong>Backend:</strong> Python;</p>

<p><strong>Banco de Dados:</strong> MySQL;</p>

<p><strong>Frameworks/Bibliotecas:</strong> Flask;</p>

<p><strong>Ferramentas adicionais:</strong> GitHub, Microsoft Word, Visual Studio Code.</p>

<hr />

## 2. VISÃO GERAL DO PROJETO

<h2 id="21-ciclo-de-vida-do-projeto">2.1 Ciclo de vida do projeto de desenvolvimento de software</h2>

<p>Para o desenvolvimento do sistema de gerenciamento de pedidos, adotamos uma abordagem embasada nas práticas ágeis. Essa escolha se justifica pela necessidade de entregas contínuas, validação constante com os usuários finais e a capacidade de adaptação a requisitos dinâmicos característicos do setor de <em>foodservice</em>. A seguir, detalhamos a instanciação do ciclo de vida do projeto com base na arquitetura de metodologias:</p>

<h3 id="211-metodologia-metodologia-agil">2.1.1 Metodologia: Metodologia Ágil.</h3>

<p>A escolha pela agilidade se dá pelo foco na entrega de valor e pela flexibilidade. Como o ambiente de restaurantes exige alta usabilidade e eficiência operacional, uma abordagem ágil permite que o grupo ajuste prioridades no Backlog do Produto e planeje o escopo conforme os riscos são identificados e mitigados, sem engessar o desenvolvimento.</p>

<h3 id="212-processo">2.1.2 Processo:</h3>

<p>Utilizaremos um processo orientado pelo <strong>Scrumban</strong> (uma abordagem híbrida que combina a estrutura do Scrum com o fluxo contínuo do Kanban), apoiado por práticas de engenharia do <strong>XP</strong> (<em>Extreme Programming</em>). O Scrumban nos permite manter os papéis definidos (Dono do Produto, Desenvolvedores e Analistas de Qualidade) e o planejamento em ciclos curtos de uma semana (Sprints), mas com a adoção de um fluxo contínuo (sistema pull) e limites de trabalho em andamento (WIP – <em>Work in Progress</em>) para evitar gargalos na equipe.</p>

<h3 id="213-procedimentos">2.1.3 Procedimentos:</h3>

<p>O trabalho fluirá através de iterações baseadas em Sprints, iniciando com uma <em>Sprint Planning</em> para puxar as tarefas prioritárias (como as funcionalidades <em>Must</em>) para o quadro de desenvolvimento. O acompanhamento diário e o gerenciamento de riscos serão guiados visualmente pelo quadro Kanban, garantindo transparência do que está a fazer, em andamento e concluído. Ao final do ciclo, as entregas passarão por avaliações de qualidade baseadas nas métricas do GQM.</p>

<h3 id="214-metodos">2.1.4 Métodos:</h3>

<ul>
<li><strong>Quadro Kanban e Limites de WIP:</strong> Gestão visual do fluxo de tarefas para identificar rapidamente impedimentos e limitar a quantidade de itens em desenvolvimento simultâneo, garantindo foco na conclusão.</li>
<li><strong>Histórias de usuário:</strong> Utilizadas para mapear o Backlog do produto de forma focada (Administrador, Garçom, Cozinheiro).</li>
<li><strong>Testes de Software:</strong> Implementação de testes para mitigar riscos de comunicação entre interfaces, buscando manter a densidade de erros de programa em níveis mínimos (≤ 0.5%).</li>
<li><strong>Refatoração Contínua:</strong> Prática do XP para manter o código limpo e otimizado, assegurando os tempos de execução e de comunicação em tempo real esperados pelo sistema.</li>
</ul>

<h3 id="215-ferramentas">2.1.5 Ferramentas:</h3>

<ul>
<li><strong>Codificação:</strong> Visual Studio Code utilizando HTML, CSS, JavaScript para o <em>frontend</em> e Python com Flask e MySQL para o <em>Backend</em>.</li>
<li><strong>Design e Prototipagem</strong>: Figma, para desenhar interfaces intuitivas e responsivas.</li>
<li><strong>Versionamento e Gestão:</strong> Git, centralizando o código no GitHub, que também poderá ser utilizado para a gestão visual do Kanban.</li>
<li><strong>Comunicação da Equipe:</strong> Teams, Discord e WhatsApp.</li>
</ul>

<h2 id="22-organizacao-do-projeto">2.2 Organização do Projeto</h2>

<p>A tabela 2 apresenta as atribuições e deveres de cada membro do grupo, ou seja, as responsabilidades escolhidas pelos membros participantes.</p>

<p><strong>Tabela 2 - Divisão de funções</strong></p>

<table class="doc-table doc-table--md">
  <thead>
    <tr>
      <th>Papel</th>
      <th>Atribuições</th>
      <th>Responsável</th>
      <th>Participantes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Desenvolvedor</td><td>Esses membros ficam responsáveis por fazer com que o projeto funcione através das iterações de código e banco de dados</td><td>Igor, Davi Sakai, João Gabriel, Jhonatan William</td><td>Igor, Davi Sakai, João Gabriel, João Amorim, Jhonatan William</td></tr>
    <tr><td>Dono do Produto</td><td>Esse membro(s) fica responsável por validar os requisitos e backlog do produto seria como um representante do cliente na equipe</td><td>Rafael de Aquino</td><td>Rafael de Aquino</td></tr>
    <tr><td>Analista de Qualidade</td><td>Esses membros ficam responsáveis por avaliar a qualidade do produto e decidir se a iteração está pronta para implementação, de acordo com conceito de pronto do time.</td><td>Lucas Peixoto, Alexandre, Lucas Ferreira</td><td>Lucas Peixoto, Alexandre, Lucas Ferreira</td></tr>
    <tr><td>Cliente (monitor)</td><td>Avaliar se o projeto está de acordo com os requisitos e proposta inicial</td><td>Lucas Ferreira</td><td>Lucas Ferreira</td></tr>
  </tbody>
</table>

<p><em>Fonte: realizado pelo autor (2026)</em></p>

<h2 id="23-planejamento-das-fases">2.3 Planejamento das Fases e/ou Iterações do Projeto</h2>

<p>O planejamento de Fases tem como objetivo demonstrar o que foi feito em cada sprint, o período que ela durou e as entregas feitas durante ou ao final da iteração. O planejamento também deixa claro qual o grau de conclusão do projeto. A tabela 3 abaixo apresenta esses dados.</p>

<p><strong>Tabela 3 - Planejamento das fases</strong></p>

<table class="doc-table doc-table--sm">
  <thead>
    <tr>
      <th>Sprint</th>
      <th>Produto (Entrega)</th>
      <th>Data Início</th>
      <th>Data Fim</th>
      <th>Entregável(eis)</th>
      <th>Responsáveis</th>
      <th>% conclusão</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Sprint 1</td><td>Definição geral do produto</td><td>09/04/2026</td><td>16/04/2026</td><td>-</td><td>Todos</td><td>2%</td></tr>
    <tr><td>Sprint 2</td><td>Planejamento do projeto e DV</td><td>23/04/2026</td><td>30/04/2026</td><td>1ª versão do Documento de Visão</td><td>Todos</td><td>7%</td></tr>
    <tr><td>Sprint 3</td><td>Documento de arquitetura</td><td>30/04/2026</td><td>14/05/2026</td><td>1ª versão do Documento de arquitetura</td><td>Todos</td><td>13%</td></tr>
    <tr><td>Sprint 4</td><td>Preparação do Github</td><td>20/05/2026</td><td>28/05/2026</td><td>Pastas e documentos no git</td><td>Todos</td><td>18%</td></tr>
    <tr><td>Sprint 5</td><td>Início do Desenvolvimento</td><td>28/05/2026</td><td>04/06/2026</td><td>Models, Controllers e Services; atualização dos documentos</td><td>Igor Lima, João Gabriel, Lucas Ferreira, Lucas Peixoto</td><td>20%</td></tr>
    <tr><td>Sprint 6</td><td>Integração dos models, services e controllers; desenvolvimento do banco de dados</td><td>04/06/2026</td><td>11/06/2026</td><td>Banco de dados + atualizações do backend</td><td>Alexandre, Igor Lima, Jhonatan, João Gabriel, Lucas Ferreira, Lucas Peixoto</td><td>45%</td></tr>
    <tr><td>Sprint 7</td><td>Integração das camadas e desenvolvimento Frontend</td><td>11/05/2026</td><td>18/06/2026</td><td>Entrega da view de login e do administrador</td><td>Davi, João Paulo, João Victor, Rafael</td><td>65%</td></tr>
    <tr><td>Sprint 8</td><td></td><td></td><td></td><td></td><td></td><td>?</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<h2 id="24-matriz-de-comunicacao">2.4 Matriz de Comunicação</h2>

<p>A tabela 4 apresenta como serão feitas as comunicações entre o grupo e a monitora. Além disso, mostrará quais são as fontes de informação geradas pelo grupo, sobre o projeto, e onde elas estarão disponíveis para a consulta das iterações.</p>

<p><strong>Tabela 4 - Matriz de comunicação</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Descrição</th>
      <th>Área/Envolvidos</th>
      <th>Periodicidade</th>
      <th>Produtos Gerados</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Acompanhamento das atividades em andamento via Teams, WhatsApp e Acompanhamento dos riscos, compromissos, ações pendentes via github</td><td>Equipe do Projeto</td><td>Semanal</td><td>Ata de reunião, Relatório de situação do projeto</td></tr>
    <tr><td>Acompanhamento dos riscos, compromissos, ações pendentes via github</td><td>Equipe do Projeto</td><td>Quinzenal</td><td>Ata de reunião, Relatório de situação do projeto</td></tr>
    <tr><td>Comunicar a situação do projeto</td><td>Equipe do Projeto + monitor</td><td>Semanal</td><td>Ata de reunião, e Relatório de situação do projeto</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<h2 id="25-gerenciamento-de-riscos">2.5 Gerenciamento de Riscos</h2>

<p>O Gerenciamento de Riscos consiste na identificação, avaliação, priorização, tratamento e monitoramento de possíveis ameaças tanto internas quanto externas. O objetivo de aplicar o gerenciamento de riscos no projeto é promover a continuidade, a segurança no trabalho, a tomada de decisões e a redução de custos.</p>

<p>A tabela 5 logo a seguir mostra os principais riscos que podemos vir a enfrentar durante as etapas do projeto, a tabela classifica os riscos em alto, médio ou baixo, além de propor estratégias de mitigação e plano de contingência.</p>

<p><strong>Tabela 5 - Gerenciamento de riscos</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Risco</th>
      <th>Grão de exposição</th>
      <th>Mitigação</th>
      <th>Plano de contingência</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Alteração de requisitos do backlog do produto após o início da sprint</td><td>Alto</td><td>Aumentando o período de refinamento do backlog do produto</td><td>Reunir os requisitos que já estão acordados e aumentar o grau de prioridade</td></tr>
    <tr><td>Falta de comunicação entre as interfaces do sistema</td><td>Alto</td><td>Implementação de Testes de Software para garantir a redução de atrasos</td><td>Revisão completa de todos as unidades do código em larga escala para solução do problema</td></tr>
    <tr><td>Dificuldades com as tecnologias usadas no projeto (SQL, Flask, etc.)</td><td>Médio</td><td>Preparação rápida para a implementação básica dessas tecnologias</td><td>Solicitar ajuda externa para o auxílio das atividades (monitores, professores, tutores etc.)</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<h2 id="26-criterios-de-replanejamento">2.6 Critérios de Replanejamento</h2>

<p>A seguir, a tabela 6 apresenta os critérios de replanejamento e as ações que serão tomadas para replanejar os seguimentos afetados:</p>

<p><strong>Tabela 6 - Critérios de replanejamento</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Risco</th>
      <th>Critério de Replanejamento</th>
      <th>Ação de Replanejamento</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Atraso na entrega de funcionalidades</td><td>Atraso, igual ou superior a 1 sprint, na entrega de uma funcionalidade em relação ao cronograma</td><td>Alterar as prioridades de entrega e ajustar o backlog</td></tr>
    <tr><td>Necessidade de alterar o escopo</td><td>Funcionalidades Must não estão sendo realizadas de acordo com o cronograma planejado</td><td>Replanejar as funcionalidades que seriam trabalhadas em sprints futuras</td></tr>
    <tr><td>Falta de comunicação entre os membros do projeto</td><td>Dificuldade de comunicação com um membro por 3 dias</td><td>Ajustes na divisão e nas responsabilidades atribuídas aos membros</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<hr />

## 3. PROCESSO DE DESENVOLVIMENTO DE SOFTWARE

<p>Conforme apresentado na Seção 2.1, o desenvolvimento do sistema Nexus Gourmet será conduzido com base na metodologia ágil, por meio da abordagem híbrida Scrumban, complementada por práticas de engenharia de software oriundas do Extreme Programming (XP). Essa combinação visa proporcionar flexibilidade, organização e melhoria contínua ao longo de todo o ciclo de vida do projeto.</p>

<h2 id="31-principais-praticas-adotadas">3.1 Principais Práticas Adotadas</h2>

<p>Para garantir a agilidade e a qualidade do software, a equipe adotou as seguintes práticas:</p>

<ul>
<li><strong>Sprint Planning:</strong> Reunião realizada no início de cada Sprint com o objetivo de selecionar, priorizar e detalhar as funcionalidades a serem desenvolvidas, definindo metas e responsabilidades para a equipe.</li>
<li><strong>Sprint Review:</strong> Encontro ao término de cada Sprint para apresentação das funcionalidades implementadas e validação junto ao cliente ou monitor.</li>
<li><strong>Sprint Retrospective:</strong> Reunião destinada à reflexão sobre o processo de desenvolvimento, identificando pontos de melhoria e oportunidades de aperfeiçoamento.</li>
<li><strong>Gestão Visual com Kanban:</strong> Utilização de quadro Kanban para monitoramento contínuo das tarefas, organizadas em colunas que representam o fluxo de trabalho (a fazer, em andamento, em validação e concluído).</li>
<li><strong>Limitação de WIP (Work in Progress):</strong> Estabelecimento de limites para o número de tarefas em andamento simultaneamente, a fim de reduzir sobrecarga e evitar gargalos.</li>
<li><strong>Pair Programming (XP):</strong> Prática aplicada em funcionalidades críticas ou de maior complexidade, promovendo colaboração, compartilhamento de conhecimento e redução de defeitos.</li>
<li><strong>Code Review (XP):</strong> Revisão sistemática do código desenvolvido, garantindo conformidade com padrões de qualidade, legibilidade e manutenção.</li>
<li><strong>Testes Contínuos (XP):</strong> Execução de testes unitários, de integração e testes manuais durante todo o desenvolvimento, assegurando a qualidade incremental do produto.</li>
<li><strong>Refinamento Contínuo do Backlog:</strong> Atualização periódica do Backlog do Nexus Gourmet com base no feedback do cliente, nas prioridades de negócio e nas necessidades identificadas pela equipe.</li>
</ul>

<h2 id="32-ferramentas-de-suporte">3.2 Ferramentas de Suporte</h2>

<p>Para apoiar a execução do processo, serão utilizadas ferramentas de colaboração, comunicação, versionamento e documentação:</p>

<ul>
<li><strong>Versionamento:</strong> Git + GitHub</li>
<li><strong>Documentação:</strong> GitHub Pages</li>
<li><strong>Prototipagem:</strong> Figma</li>
<li><strong>Comunicação:</strong> Teams, Discord e WhatsApp</li>
</ul>

<p>A tabela 7 a seguir detalha as responsabilidades de cada papel dentro do projeto, adaptada para o formato de gestão profissional do sistema.</p>

<p><strong>Tabela 7 - Papéis</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Papel</th>
      <th>Responsabilidades</th>
      <th>Integrantes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Dono do produto</td><td>Responsável por validar os requisitos e o backlog do produto, atuando como representante do cliente na equipe</td><td>Rafael de Aquino</td></tr>
    <tr><td>Desenvolvedores</td><td>Responsáveis pela implementação técnica do sistema, incluindo código, banco de dados e iterações de desenvolvimento</td><td>Davi Sakai, Igor Lima, Jhonatan William, João Gabriel, João Amorim e João Paulo</td></tr>
    <tr><td>Analistas de Qualidade</td><td>Responsáveis por avaliar a qualidade do produto e validar se as iterações estão prontas para implementação conforme o conceito de "pronto" do time</td><td>Alexandre Sousa, Lucas Peixoto e Lucas Ferreira</td></tr>
    <tr><td>Cliente</td><td>Responsável por avaliar se o projeto está de acordo com os requisitos e a proposta inicial do Nexus Gourmet</td><td>Lucas Ferreira</td></tr>
  </tbody>
</table>

<p>A figura 2 abaixo apresenta o ciclo de vida de desenvolvimento adotado para o projeto <strong>Nexus Gourmet</strong>, representando as fases principais de planejamento, desenvolvimento, revisão, retrospectiva e refinamento do backlog.</p>

Figura 2 – Ciclo de vida adotado no Nexus Gourmet
![Figura 2 – Ciclo de vida adotado no Nexus Gourmet](img/ciclo de vida.png)

<p><em>Fonte: Elaborada pelos autores (2026)</em></p>

<hr />

## 4. DECLARAÇÃO DE ESCOPO DO PROJETO

<h2 id="41-backlog-do-produto">4.1 Backlog do produto</h2>

<p>A Tabela 8 apresenta o backlog do produto, composto pelo conjunto de funcionalidades identificadas para o sistema. Cada funcionalidade está descrita de forma objetiva e classificada por nível de prioridade, servindo como base para o planejamento das sprints e para o acompanhamento do desenvolvimento ao longo do projeto.</p>

<p><strong>Tabela 8 - Backlog</strong></p>

<table class="doc-table doc-table--sm">
  <thead>
    <tr>
      <th>ID</th>
      <th>Funcionalidade</th>
      <th>Descrição</th>
      <th>Prioridade</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>F01</td><td>Abrir pedido</td><td>O garçom deve poder abrir um pedido vinculado a uma mesa</td><td>Alta</td></tr>
    <tr><td>F02</td><td>Adicionar item ao pedido</td><td>O garçom deve poder adicionar itens do cardápio a um pedido em aberto</td><td>Alta</td></tr>
    <tr><td>F03</td><td>Remover item do pedido</td><td>O garçom deve poder remover itens de um pedido em aberto</td><td>Alta</td></tr>
    <tr><td>F04</td><td>Enviar pedido para a cozinha</td><td>O garçom deve poder enviar o pedido, alterando seu status para "em preparo"</td><td>Alta</td></tr>
    <tr><td>F05</td><td>Visualizar pedidos na cozinha</td><td>O cozinheiro deve poder visualizar todos os pedidos ativos organizados por status</td><td>Alta</td></tr>
    <tr><td>F06</td><td>Visualizar tempo de espera</td><td>O cozinheiro deve poder visualizar o tempo decorrido desde a abertura de cada pedido</td><td>Alta</td></tr>
    <tr><td>F07</td><td>Atualizar status do pedido</td><td>O cozinheiro deve poder marcar um pedido como "em preparo" ou "pronto"</td><td>Alta</td></tr>
    <tr><td>F08</td><td>Fechar conta</td><td>O garçom deve poder fechar a conta de uma mesa, gerando o total e liberando a mesa</td><td>Alta</td></tr>
    <tr><td>F09</td><td>Calcular total do pedido</td><td>O sistema deve calcular automaticamente o valor total do pedido com base nos itens e quantidades</td><td>Média</td></tr>
    <tr><td>F10</td><td>Visualizar mesas</td><td>O sistema deve exibir todas as mesas do restaurante com seus respectivos status</td><td>Média</td></tr>
    <tr><td>F11</td><td>Cadastrar produtos</td><td>O administrador deve poder cadastrar novos produtos no cardápio, informando nome, categoria e preço</td><td>Alta</td></tr>
    <tr><td>F12</td><td>Editar produto</td><td>O administrador deve poder editar as informações de um produto já cadastrado</td><td>Média</td></tr>
    <tr><td>F13</td><td>Remover produto</td><td>O administrador deve poder remover um produto do cardápio</td><td>Média</td></tr>
    <tr><td>F14</td><td>Cadastrar mesa</td><td>O administrador deve poder cadastrar novas mesas, informando número e capacidade</td><td>Alta</td></tr>
    <tr><td>F15</td><td>Editar mesa</td><td>O administrador deve poder editar as informações de uma mesa já cadastrado</td><td>Média</td></tr>
    <tr><td>F16</td><td>Remover mesa</td><td>O administrador deve poder remover uma mesa do sistema</td><td>Média</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<h2 id="42-perfis">4.2 Perfis</h2>

<p>A Tabela 9 apresenta os perfis de usuário do sistema, descrevendo o papel de cada ator no contexto do restaurante e as responsabilidades atribuídas dentro da aplicação. A definição dos perfis orienta a construção das <em>user stories</em> e dos casos de uso detalhados nas seções seguintes.</p>

<p><strong>Tabela 9: Perfis de acesso</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Nome do perfil</th>
      <th>Características do perfil</th>
      <th>Permissões de acesso</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>P01</td><td>Administrador</td><td>Responsável pela gestão operacional do sistema</td><td>Cadastrar, editar e remover produtos do cardápio e mesas do restaurante</td></tr>
    <tr><td>P02</td><td>Garçom</td><td>Funcionário responsável pelo atendimento no salão</td><td>Abrir pedidos, registrar itens, enviar pedidos para a cozinha e fechar contas</td></tr>
    <tr><td>P03</td><td>Cozinheiro</td><td>Funcionário responsável pelo preparo dos pedidos</td><td>Visualizar pedidos ativos, acompanhar tempo de espera e atualizar status dos pedidos</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<h2 id="43-cenarios">4.3 Cenários</h2>

<p>A Tabela 10 organiza exemplos práticos de como os usuários interagem com o sistema, conectando requisitos a situações reais de uso. Ela orienta o desenvolvimento das funcionalidades e evita desvios do escopo. Os itens não possuem sprint definida, pois foram deixados para planejamentos futuros, reduzindo expectativas irreais. A tabela seguinte apresenta esses cenários, com ator, contexto, passos e resultado esperado:</p>

<p><strong>Tabela 10: Cenários funcionais</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>#</th>
      <th>Ator</th>
      <th>Contexto</th>
      <th>Passos</th>
      <th>Sprints</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>Administrador</td><td>Deseja registrar uma nova mesa</td><td>Acessar "Cadastro de Mesas", preencher número, capacidade e salvar.</td><td></td></tr>
    <tr><td>2</td><td>Garçom</td><td>Deseja receber o pedido de uma mesa</td><td>Selecionar a mesa desejada, clicar em "abrir pedido" e selecionar os itens desejados</td><td></td></tr>
    <tr><td>3</td><td>Cozinha</td><td>Deseja despachar um pedido finalizado</td><td>Selecionar o pedido e clicar em "pronto", para que o garçom venha retirar</td><td></td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<h2 id="44-tabela-de-backlog-do-produto">4.4 Tabela de Backlog do Produto</h2>

<p><strong>Tabela 11: Backlog do produto</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Numeração (Cenário / requisito)</th>
      <th>Sprint</th>
      <th>Nome do requisito</th>
      <th>Tipo de requisito (Funcional / não funcional)</th>
      <th>Priorização do requisito Must, Should, Could</th>
      <th>Descrição sucinta do requisito</th>
      <th>User histories (U.S.) associadas</th>
    </tr>
  </thead>
  <tbody>
    <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
  </tbody>
</table>

<hr />

## 5 MÉTRICAS E MEDIÇÕES

<h2 id="51-gqm-de-medicoes">5.1 GQM de medições</h2>

<p>O <em>Goal Question Metrics</em> (GQM) foi elaborado com o intuito de estabelecer, através da tabela 12, as métricas do projeto, seguindo seu objetivo principal: desenvolver um software que centralize o processo de registro, acompanhamento e gerenciamento de pedidos de restaurantes.</p>

<p>As métricas foram definidas com base em:</p>

<ol>
<li>Expectativas dos Stakeholders: Entrega de testes intermediários e produto funcional.</li>
<li>Riscos do projeto: Comunicação da equipe, cumprimento de prazos e qualidade do código.</li>
</ol>

<p><strong>Tabela 12 - GQM do produto</strong></p>

<table class="doc-table doc-table--xs">
  <thead>
    <tr>
      <th>Objetivo</th>
      <th>Pergunta</th>
      <th>Métrica</th>
      <th>Cálculo</th>
      <th>Escala</th>
      <th>Valor esperado</th>
      <th>Forma de análise</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Validar qualidade de implementação</td><td>O software está bem implementado?</td><td>Densidade de erros de programa</td><td>(Linhas com erro)/(total de linhas) x 100%</td><td>%</td><td>≤ 0.5%</td><td>Implementação de Testes de Software e Refatoração</td></tr>
    <tr><td>Eficácia dos alertas visuais</td><td>Os alertas estão funcionando corretamente?</td><td>Quantidade de falsos positivos</td><td>(Alertas falsos)/(Total de alertas) x 100%</td><td>%</td><td>≤ 0.2%</td><td>Por testes de software, registrando a média de alertas falsos</td></tr>
    <tr><td>Obediência ao período dos sprints</td><td>Os sprints estão entregando todos os musts?</td><td>Densidade de prorrogações de musts</td><td>(Quantidade de musts prorrogados)/(Total de Musts do Sprint) x 100%</td><td>%</td><td>100%</td><td>Implementação de Sprint Reviews e Sprint Meetings</td></tr>
    <tr><td>Usabilidade da Interface de usuário</td><td>A interface é intuitiva e perfeitamente utilizável?</td><td>Densidade de feedback negativo</td><td>(Reports negativos)/(Total de Reports) x 100%</td><td>%</td><td>≤ 2%</td><td>Reuniões de alinhamento de requisitos e contato com o usuário</td></tr>
    <tr><td>Verificar quantidade de pedido por garçom</td><td>Qual garçom faz mais pedidos?</td><td>Densidade de pedidos por garçom</td><td>(Pedidos realizados para cada um)/(Pedidos totais)x100%</td><td>%</td><td>≥(Quantidade de pedidos particulares)/(Pedidos totais)</td><td>A quantidade de contas abertas por garçom</td></tr>
    <tr><td>Verificar tempo médio de preparo por produto</td><td>Qual o tempo médio que um produto é entregue?</td><td>Tempo de entrega</td><td>(Horário que foi entregue)-(Horário que foi pedido)</td><td>min</td><td>≤(Média de entrega do produto)</td><td>O tempo gasto entre a abertura da conta e a entrega desde na mesa</td></tr>
    <tr><td>Verificar saída de produto</td><td>Qual a porcentagem de saída de cada produto?</td><td>Densidade de pedidos do produto</td><td>(Pedido do produto)/(Pedidos totais)x100%</td><td>%</td><td>(Pedidos totais)/(Quantidade de produtos)</td><td>Quantidade de vezes que o pedido foi feito</td></tr>
    <tr><td>Verificar a quantidade de comandas</td><td>Quantas comandas foram abertas?</td><td>Quantidade de comandas abertas</td><td>-</td><td>-</td><td>-</td><td>-</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<hr />

## 6. TESTES DE SOFTWARE

<h2 id="61-estrategia-de-testes-contendo">6.1 Estratégia de testes contendo:</h2>

<h3 id="611-testes-implementados-em-niveis">6.1.1 Testes implementados em níveis</h3>

<p>Os testes implementados no projeto permitem uma maior confiabilidade do código, e podem ser entendidos em níveis:</p>

<ul>
<li><strong>Testes Unitários:</strong> Testam o código de forma isolada, validando a menor unidade funcional do mesmo, garantindo que cada componente da implementação responda corretamente às entradas fornecidas e eliminam custos de manutenção ao prevenir que bugs pequenos cheguem à produção.</li>
<li><strong>Testes de Integração:</strong> Verificam como diferentes partes do programa trabalham em conjunto para compor uma funcionalidade inteira, validam a comunicação e a interface entre dois ou mais módulos do sistema, investigam a existência de bugs que surgem apenas quando componentes isoladas são conectados entre si e testam a interação com elementos externos, como bancos de dados.</li>
<li><strong>Testes de Sistema:</strong> Testam e validam o software como um todo, garantindo que o produto final atende a todos os requisitos funcionais e técnicos do projeto. Eles garantem que o produto pronto seja meticulosamente o que foi planejado no escopo e avaliam não só as funções de um sistema, mas o desempenho, estabilidade e segurança.</li>
</ul>

<h3 id="612-testes-funcionais">6.1.2 Testes Funcionais</h3>

<p>Testes de software funcionais são fundamentais para validação e análise usabilidade de uma aplicação.</p>

<ul>
<li><strong>Testes Funcionais:</strong> Trata-se de testes que verificam as funcionalidades de uma aplicação, é onde são testadas as regras de negócio: login funcional, bloqueio de sistema, registro de pedidos, execução de tarefas</li>
</ul>

<h3 id="613-ambientes-de-teste-e-politica-de-branches-e-commits">6.1.3 Ambientes de Teste e Política de Branches e Commits</h3>

<p>O projeto adota uma estrutura organizada de ambientes de teste integrada à sua política de versionamento de código, utilizando Git e GitHub como ferramentas principais.</p>

<h4 id="6131-ambientes-de-teste">6.1.3.1 Ambientes de Teste</h4>

<p>São definidos três ambientes principais ao longo do ciclo de desenvolvimento:</p>

<ul>
<li><strong>Ambiente de Desenvolvimento (Dev):</strong> Utilizado para implementação e testes iniciais das funcionalidades. Os desenvolvedores trabalham localmente com as tecnologias do projeto, incluindo HTML, CSS e JavaScript no frontend, Python com Flask no backend e MySQL como banco de dados.</li>
<li><strong>Ambiente de Homologação (QA):</strong> Responsável pela validação das funcionalidades integradas. Neste ambiente, são realizados testes funcionais e não funcionais para garantir que o sistema atenda aos requisitos especificados.</li>
<li><strong>Ambiente de Produção (Prod):</strong> Ambiente final onde a aplicação é disponibilizada aos usuários. A documentação do sistema é publicada por meio do GitHub Pages.</li>
</ul>

<h4 id="6132-politica-de-branches">6.1.3.2 Política de Branches</h4>

<p>A organização das branches segue uma estrutura baseada em fluxo contínuo de integração:</p>

<ul>
<li><strong>main:</strong> Representa o ambiente de produção. Apenas código validado e estável é integrado a esta branch.</li>
<li><strong>develop:</strong> Representa o ambiente de homologação (QA), contendo funcionalidades já integradas e prontas para validação.</li>
<li><strong>feature/*:</strong> Branches destinadas ao desenvolvimento de novas funcionalidades, derivadas da branch develop.</li>
</ul>

<h4 id="6133-politica-de-commits-e-integracao">6.1.3.3 Política de Commits e Integração</h4>

<ul>
<li>Cada nova funcionalidade é desenvolvida em uma branch do tipo feature/*, com commits frequentes e descritivos.</li>
<li>Após conclusão, a feature é integrada à branch develop por meio de pull requests, passando por revisão de código.</li>
<li>A branch develop é utilizada para testes no ambiente de homologação.</li>
<li>Quando validado, o código é promovido para a branch main, sendo então disponibilizado em produção.</li>
</ul>

<h3 id="614-analise-dos-testes">6.1.4 Análise dos Testes</h3>

<p>A análise de teste será baseada na comparação entre os resultados esperados do teste e o resultado do teste em si. Com base nessa comparação, no caso de resultados não esperados ou insatisfatórios, haverá uma investigação de falhas, correção de erros, medição de desempenho, retestagem e então documentação dos resultados.</p>

<p>Ainda não foi obtido nenhum teste, pois o desenvolvimento do projeto está em suas fases iniciais.</p>

<h2 id="62-roteiro-de-teste">6.2 Roteiro de teste:</h2>

<p>Para minimizar os riscos no ambiente de teste e preservar a integridade do projeto, todos os testes planejados serão realizados em uma branch dedicada. Essa estratégia garante que possíveis erros ou modificações durante os testes não impactem o código principal do projeto.</p>

<p><strong>Pré-condição para testes</strong>: fica determinado fazer na ordem dos códigos, assim, tudo estará pronto para o próximo passo.</p>

<p><strong>Tabela 13 - Teste Unitário 1</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Campo</th>
      <th>Conteúdo</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Código</td><td>TU01</td></tr>
    <tr><td>Nome</td><td>Login com credenciais</td></tr>
    <tr><td>Objetivo</td><td>Verificar se a função de autenticação retorna sucesso com credenciais válidas</td></tr>
    <tr><td>Nível</td><td>Unitário</td></tr>
    <tr><td>Tipo</td><td>Funcional</td></tr>
    <tr><td>Precondições</td><td>Método de login implementado e usuário válido cadastrado</td></tr>
    <tr><td>Estado</td><td>n/a</td></tr>
    <tr><td>Resultados</td><td>Previsto: autenticação bem-sucedida / Realizado: n/a</td></tr>
    <tr><td>Reparos</td><td>n/a</td></tr>
    <tr><td>Ciclos</td><td>n/a</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<p><strong>Tabela 14 - Teste Integrado 1</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Campo</th>
      <th>Conteúdo</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Código</td><td>TI01</td></tr>
    <tr><td>Nome</td><td>Integração entre backend e banco de dados</td></tr>
    <tr><td>Objetivo</td><td>Verificar se o sistema armazena corretamente dados do banco</td></tr>
    <tr><td>Nível</td><td>Integração</td></tr>
    <tr><td>Tipo</td><td>Funcional</td></tr>
    <tr><td>Precondições</td><td>Banco de dados ativo e conexão configurada</td></tr>
    <tr><td>Estado</td><td>n/a</td></tr>
    <tr><td>Resultados</td><td>Previsto: autenticação bem-sucedida / Realizado: n/a</td></tr>
    <tr><td>Reparos</td><td>n/a</td></tr>
    <tr><td>Ciclos</td><td>n/a</td></tr>
  </tbody>
</table>

<p><em>Fonte: Elaborado pelo autor (2026)</em></p>

<hr />

## 7. REFERÊNCIAS BIBLIOGRÁFICAS

<p>ABRASEL. <strong>Solução KDS: ferramenta inovadora para auxiliar restaurantes</strong>. Disponível em: <a href="https://abrasel.com.br/noticias/noticias/solucao-kds-ferramenta-inovadora-para-auxiliar-restaurantes/">https://abrasel.com.br/noticias/noticias/solucao-kds-ferramenta-inovadora-para-auxiliar-restaurantes/</a>.</p>

<p>ALELO. <strong>Qual o melhor tipo de comanda para restaurante?</strong>. Disponível em: <a href="https://www.alelo.com.br/blog/estabelecimentos-comerciais/qual-o-melhor-tipo-de-comanda-para-restaurante">https://www.alelo.com.br/blog/estabelecimentos-comerciais/qual-o-melhor-tipo-de-comanda-para-restaurante</a>.</p>

<p>CLOUDFY. <strong>Os desafios na gestão de pedidos em bares e restaurantes</strong>. Disponível em: <a href="https://www.cloudfy.net.br/blog/os-desafios-na-gestao-de-pedidos-em-bares-e-restaurantes.html">https://www.cloudfy.net.br/blog/os-desafios-na-gestao-de-pedidos-em-bares-e-restaurantes.html</a>.</p>

<p>ECLETICA. <strong>E-Garçom: Transformando o Atendimento em Restaurantes</strong>. Disponível em: <a href="https://ecletica.com.br/e-garcom-transformando-o-atendimento-restaurantes/">https://ecletica.com.br/e-garcom-transformando-o-atendimento-restaurantes/</a>.</p>

<p>NOX. <strong>Sistema KDS: O que é, para que serve e como otimiza sua cozinha e cafeteria?</strong>. Disponível em: <a href="https://nox.com.br/o-que-e-sistema-kds/?utm_medium=desktop">https://nox.com.br/o-que-e-sistema-kds/?utm_medium=desktop</a>.</p>

<p>OLITECNICA. <strong>KDS: A revolução na gestão de pedidos para restaurantes e delivery</strong>. Disponível em: <a href="https://www.olitecnica.com.br/post/kds-a-revolucao-na-gestao-de-pedidos-para-restaurantes-e-delivery">https://www.olitecnica.com.br/post/kds-a-revolucao-na-gestao-de-pedidos-para-restaurantes-e-delivery</a>.</p>

<p>THEFORKMANAGER. <strong>Restaurant Table Turnover Rate Optimization</strong>. Disponível em: <a href="https://www.theforkmanager.com/en/blog/restaurant-management/restaurant-table-turnover-tips-efficiency">https://www.theforkmanager.com/en/blog/restaurant-management/restaurant-table-turnover-tips-efficiency</a>.</p>