<h1 id="documento-de-arquitetura">Documento de Arquitetura</h1>

<p><strong>Versão 1.1</strong></p>

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
      <th>Autor(es)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>14/05/2026</td><td>1.0</td><td>Primeira versão do documento que define a arquitetura usada no produto</td><td>Grupo Dijkstra</td></tr>
    <tr><td>02/06/2026</td><td>1.1</td><td>Adicionado menções diretas no corpo do documento às fontes bibliográficas usadas</td><td>Grupo Dijkstra</td></tr>
  </tbody>
</table>

<hr />

## Sumário

<ul>
  <li><a href="#1-introducao">1 Introdução</a>
    <ul>
      <li><a href="#11-proposito">1.1 Propósito</a></li>
      <li><a href="#12-escopo">1.2 Escopo</a></li>
    </ul>
  </li>
  <li><a href="#2-representacao-arquitetural">2 Representação Arquitetural</a>
    <ul>
      <li><a href="#21-definicoes">2.1 Definições</a></li>
      <li><a href="#22-justifique-sua-escolha">2.2 Justifique sua escolha</a></li>
      <li><a href="#23-detalhamento">2.3 Detalhamento</a></li>
      <li><a href="#24-metas-e-restricoes-arquiteturais">2.4 Metas e restrições arquiteturais</a></li>
      <li><a href="#25-visoes">2.5 Visões</a>
        <ul>
          <li><a href="#251-visao-de-uso-o-escopo-do-sistema">2.5.1 Visão de uso (o escopo do sistema)</a></li>
          <li><a href="#252-visao-de-organizacao-logica">2.5.2 Visão de organização lógica</a></li>
          <li><a href="#253-visao-estrutural">2.5.3 Visão estrutural</a></li>
        </ul>
      </li>
      <li><a href="#26-visao-de-implantacao">2.6 Visão de Implantação</a></li>
      <li><a href="#27-restricoes-adicionais">2.7 Restrições adicionais</a></li>
    </ul>
  </li>
  <li><a href="#3-bibliografia">3 Bibliografia</a></li>
</ul>

<hr />

## 1. Introdução

### 1.1 Propósito

<p>Este documento descreve a arquitetura do sistema sendo desenvolvido pelo grupo Dijkstra, na disciplina de MDS – Métodos de Desenvolvimento de Software – edição do primeiro semestre de 2026, para o sistema Nexus Gourmet, a fim de fornecer uma visão abrangente do sistema para desenvolvedores, testadores e demais interessados em aspectos relacionados às tecnologias a serem usadas no desenvolvimento.</p>

### 1.2 Escopo

<p>O detalhamento do escopo se encontra no documento de arquitetura, este, juntamente com o documento de Visão do produto e do projeto. Porém, em linhas gerais o escopo do produto compreende o desenvolvimento de um software capaz de registrar e organizar pedidos em restaurantes, como apresentado mais detalhadamente na tabela 1 a seguir:</p>

<p><strong>Tabela 1 - Funcionalidades presentes e não presentes</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>O que ele faz</th>
      <th>O que ele não faz</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Abrir pedido para mesa</td><td>Compra e venda de produtos</td></tr>
    <tr><td>Adicionar item ao pedido</td><td>Adicionar conta de consumidor</td></tr>
    <tr><td>Remover item do pedido</td><td>Permitir acesso direto de consumidores</td></tr>
    <tr><td>Enviar pedido para a cozinha</td><td></td></tr>
    <tr><td>Visualizar pedidos na cozinha</td><td></td></tr>
    <tr><td>Visualizar tempo de espera</td><td></td></tr>
    <tr><td>Atualizar status do pedido</td><td></td></tr>
    <tr><td>Fechar conta</td><td></td></tr>
    <tr><td>Calcular total do pedido</td><td></td></tr>
    <tr><td>Visualizar mesas</td><td></td></tr>
    <tr><td>Cadastrar produtos</td><td></td></tr>
    <tr><td>Editar produto</td><td></td></tr>
  </tbody>
</table>

<p><em>Fonte: elaborado pelo autor (2026)</em></p>

<hr />

## 2. Representação Arquitetural

### 2.1 Definições

<p>O sistema Nexus Gourmet seguirá uma arquitetura Cliente-Servidor Web, organizada internamente segundo o padrão MVC em camadas, com apoio de comunicação assíncrona para atualização do status dos pedidos (SERRANO, 2026).</p>

<p>A escolha da arquitetura Cliente-Servidor ocorre porque o sistema será acessado por diferentes tipos de clientes, como dispositivos móveis utilizados pelos garçons, telas utilizadas pela cozinha e interfaces administrativas (IBM, 2026). Esses clientes consomem os serviços oferecidos por uma aplicação central, responsável por processar as regras de negócio, controlar o fluxo dos pedidos e acessar o banco de dados.</p>

<p>Internamente, o servidor será organizado segundo o padrão MVC (Model-View-Controller). Nesse modelo, a camada View representa as interfaces do sistema; a camada Controller recebe as requisições dos usuários e coordena o fluxo das operações; e a camada Model representa os dados, regras de negócio e persistência relacionados a pedidos, mesas, produtos, usuários e status de atendimento.</p>

<p>Além disso, como o Nexus Gourmet exige atualização rápida entre salão e cozinha, especialmente no envio e acompanhamento dos pedidos, a arquitetura prevê o uso de comunicação assíncrona, como WebSocket ou mecanismo equivalente, para notificar alterações de status sem depender exclusivamente de carregamento manual das páginas.</p>

### 2.2 Justifique sua escolha

<p>A escolha da arquitetura Cliente-Servidor Web com organização interna MVC é adequada ao Nexus Gourmet porque o produto proposto não é um sistema isolado em uma única máquina, mas uma aplicação distribuída entre diferentes usuários e dispositivos. O documento de Visão do Produto define o Nexus Gourmet como uma aplicação web-mobile voltada a proprietários e funcionários de restaurantes, com a finalidade de registrar, acompanhar e gerenciar pedidos de forma centralizada, ágil e sem erros.</p>

<p>O problema central identificado no projeto está relacionado à falha de comunicação entre salão e cozinha, à perda de informações em comandas de papel e à falta de rastreabilidade dos pedidos. Por isso, a arquitetura precisa favorecer a centralização das informações, o acesso simultâneo por múltiplos perfis de usuário e a atualização rápida do estado dos pedidos. A organização Cliente-Servidor atende diretamente a essa necessidade, pois separa os dispositivos consumidores dos serviços da aplicação central, mantendo o processamento e os dados em um servidor comum.</p>

<p>Essa escolha é adequada ao Nexus Gourmet porque o sistema possui características típicas de uma aplicação distribuída e modular, na qual diferentes usuários interagem simultaneamente com uma aplicação centralizada. O modelo Cliente-Servidor permite separar claramente os dispositivos de acesso da camada responsável pelo processamento das regras de negócio e armazenamento dos dados, favorecendo a organização, controle e sincronização das operações realizadas no restaurante.</p>

<p>No contexto do Nexus Gourmet, essa separação é importante porque o sistema será utilizado por diferentes perfis, como garçons, cozinha e administradores, cada um acessando funcionalidades específicas por meio de navegadores ou dispositivos conectados à aplicação principal. Dessa forma, a centralização do processamento e das informações garante maior consistência no gerenciamento de pedidos, mesas, produtos e status de atendimento.</p>

<p>Para complementar essa estrutura, o sistema adotará o padrão MVC (Model-View-Controller) como organização interna da aplicação. Essa abordagem favorece a separação de responsabilidades entre interface, controle do fluxo da aplicação e manipulação dos dados, tornando o sistema mais organizado e compreensível.</p>

<p>A camada View será responsável pela interação com os usuários, apresentando telas e funcionalidades voltadas ao gerenciamento dos pedidos e operações do restaurante. A camada Controller coordenará o fluxo das requisições e regras de negócio, intermediando a comunicação entre interface e persistência. Já a camada Model concentrará as entidades e dados relacionados ao domínio do sistema, como pedidos, mesas, produtos e usuários.</p>

<p>Essa organização contribui diretamente para a manutenção e evolução do software, reduzindo o acoplamento entre partes do sistema e facilitando alterações futuras sem impacto excessivo em outros módulos. Além disso, a divisão clara das responsabilidades melhora o desenvolvimento paralelo entre as equipes de frontend, backend e banco de dados, permitindo maior produtividade e facilidade de integração.</p>

<p>Outro fator relevante é a necessidade de atualização rápida das informações entre salão e cozinha. Como o sistema exige acompanhamento contínuo dos pedidos e alteração dinâmica de status, a arquitetura também prevê comunicação assíncrona entre cliente e servidor, permitindo que mudanças importantes sejam refletidas em tempo próximo ao real. Isso possibilita maior agilidade operacional, reduz atrasos no atendimento e melhora a sincronização entre os diferentes setores do restaurante.</p>

<p>Assim, a combinação entre Cliente-Servidor, MVC e comunicação assíncrona oferece uma solução adequada às necessidades funcionais e estruturais do Nexus Gourmet, equilibrando organização, modularidade, manutenção, escalabilidade e eficiência operacional.</p>

### 2.3 Detalhamento


<p>A arquitetura proposta pode ser representada em quatro partes principais:</p>

<ul>
<li><strong>Clientes Web</strong> - Representam os dispositivos usados pelos perfis do sistema
  <ul>
    <li>Garçom: abre pedidos, adiciona/remove itens, envia pedidos para a cozinha e fecha contas.</li>
    <li>Cozinha: visualiza pedidos ativos, acompanha tempo de espera e atualiza status.</li>
    <li>Administrador: cadastra e edita produtos, mesas e demais dados necessários à operação.</li>
  </ul>
</li>
<li><strong>Camada de Apresentação - View</strong>
  <ul>
    <li>Corresponde às páginas e interfaces desenvolvidas em HTML, CSS e JavaScript. Essa camada é responsável por apresentar as telas ao usuário e capturar suas ações, como clicar em "enviar pedido", "adicionar item" ou "marcar como pronto".</li>
  </ul>
</li>
<li><strong>Camada de Controle e Aplicação - Controller/Service</strong>
  <ul>
    <li>Corresponde ao backend da aplicação, desenvolvido em Python com Flask. Essa camada recebe as requisições das interfaces, valida as operações, coordena o fluxo de dados e aciona as regras de negócio. É nela que ficam os controladores e serviços relacionados a pedidos, mesas, produtos, usuários e status.</li>
  </ul>
</li>
<li><strong>Camada de Modelo e Persistência — Model/Repository/Database</strong>
  <ul>
    <li>Representa os dados e regras centrais do sistema. Inclui as entidades principais, como Pedido, ItemPedido, Mesa, Produto, Usuário e StatusPedido. Também inclui os repositórios responsáveis por acessar o banco de dados MySQL, garantindo que os dados dos pedidos, produtos e mesas sejam armazenados de forma consistente.</li>
  </ul>
</li>
</ul>

<p><strong>Figura 1 - Estilo arquitetural</strong></p>

![Figura 1 - estilo arquitectural](img/estilo-arquitectural.jpg)

<p><em>Fonte: elaborado pelos autores (2026)</em></p>

<p>O fluxo principal começa quando o garçom acessa a interface web/mobile e registra um pedido vinculado a uma mesa. A View envia a solicitação ao Controller por meio de HTTP/HTTPS. O Controller aciona o Service correspondente, que valida as regras de negócio, como existência da mesa, disponibilidade do produto e cálculo dos valores. Em seguida, o Repository persiste os dados no MySQL.</p>

<p>Quando o pedido é enviado para a cozinha, o sistema altera seu status e disponibiliza essa alteração para a tela da cozinha. Para atender a necessidade de atualização em tempo real, a aplicação pode utilizar WebSocket ou outro mecanismo assíncrono, permitindo que a cozinha receba a atualização sem depender de recarregamento manual da página.</p>

<p>Quando o cozinheiro altera o status do pedido para "em preparo" ou "pronto", o fluxo ocorre no sentido inverso: a View da cozinha envia a atualização ao Controller, o Service valida a mudança de estado e o banco de dados é atualizado. A interface do garçom pode então visualizar o novo status do pedido.</p>

<p><strong>Tabela 2 - Responsabilidades por camada</strong></p>

<table class="doc-table">
  <thead>
    <tr>
      <th>Elemento</th>
      <th>Responsabilidade no Nexus Gourmet</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Cliente Web/Mobile</td><td>Permitir interação dos usuários com o sistema em diferentes dispositivos</td></tr>
    <tr><td>View</td><td>Exibir telas, formulários, botões, listas de pedidos, mesas e produtos</td></tr>
    <tr><td>Controller</td><td>Receber requisições, coordenar o fluxo e encaminhar ações aos serviços</td></tr>
    <tr><td>Service</td><td>Aplicar regras de negócio, validações e cálculos</td></tr>
    <tr><td>Model</td><td>Representar as entidades principais do domínio</td></tr>
    <tr><td>Repository</td><td>Isolar o acesso ao banco de dados</td></tr>
    <tr><td>Banco de Dados</td><td>Persistir pedidos, produtos, mesas, usuários e histórico de status</td></tr>
    <tr><td>Comunicação assíncrona</td><td>Atualizar cozinha e salão quando houver mudança relevante no pedido</td></tr>
  </tbody>
</table>

<p><em>Fonte: elaborado pelos autores (2026)</em></p>

### 2.4 Metas e restrições arquiteturais

<p>Esta seção define metas e restrições arquiteturais que o sistema deve seguir.</p>

<ul>
<li><strong>Desempenho de Interface:</strong> As atualizações de status de um pedido devem refletir na tela da cozinha em tempo real.</li>
<li><strong>Confiabilidade de Dados:</strong> O sistema deve garantir que dados de pedidos não sejam perdidos caso haja alguma queda momentânea na conexão de internet.</li>
<li><strong>Restrições de Rede:</strong> O software precisa ser otimizado para operar na rede local do estabelecimento, a fim de minimizar a latência no envio dos pedidos do salão para a cozinha.</li>
<li><strong>Escalabilidade e Concorrência:</strong> O sistema está restrito a operar suportando múltiplos usuários (garçons e cozinheiros) logados de forma simultânea, especialmente em horários de pico.</li>
<li><strong>Restrição de Segurança/Acesso:</strong> É obrigatória a identificação (login) de qualquer funcionário para que o sistema permita a realização de operações de pedido.</li>
<li><strong>Usabilidade Física:</strong> Devido ao contexto dos garçons, o design da interface no dispositivo móvel tem a meta de possibilitar a operação e uso com apenas uma das mãos.</li>
<li><strong>Métrica de Qualidade de Código:</strong> O sistema tem como meta técnica manter uma densidade de erros de programa máxima de 0.5%.</li>
</ul>

### 2.5 Visões

#### 2.5.1 Visão de uso (o escopo do sistema)

<p>O escopo do sistema Nexus Gourmet abrange o desenvolvimento de uma aplicação distribuída, com interfaces web e mobile, destinada à centralização e otimização do registro e gerenciamento de pedidos em ambientes gastronômicos. O fluxo operacional da aplicação engloba o ciclo completo do atendimento: a abertura da mesa e a inserção de itens pelo garçom; o envio simultâneo do pedido para a interface da cozinha, o monitoramento do tempo de preparo e a atualização de status ("em preparo" ou "pronto") pela equipe de cozinheiros, e, por fim, o encerramento da conta da mesa.</p>

<p>A definição do estilo arquitetural Cliente-Servidor Web, aliada ao padrão estrutural Model-View-Controller (MVC), foi fundamentada primordialmente nos requisitos operacionais do ambiente de implantação. A necessidade de mitigar falhas de comunicação históricas entre o salão e a cozinha exigiu uma arquitetura que garantisse a centralização das informações e o acesso simultâneo. Adicionalmente, a pluralidade de perfis de acesso sistêmico caracterizada pelo uso de dispositivos móveis pelos garçons, telas ou tablets na cozinha e interfaces web exclusivas para a administração justificou a separação lógica das interfaces gráficas (camada View) do processamento das regras de negócio e da persistência de dados.</p>

<p>Por fim, o requisito de atualização sistêmica ágil para o acompanhamento dos pedidos determinou a adoção de mecanismos de comunicação assíncrona, a exemplo do protocolo WebSocket, possibilitando que as mudanças de status sejam refletidas nas telas de operação sem a necessidade de recarregamento manual.</p>

<p><strong>Figura 2 - Diagrama de Casos de Uso</strong></p>

![Figura 2 - Diagrama de Casos de Uso](img/casos-de-uso.png)

<p><em>Fonte: Elaborado pelos autores (2026)</em></p>

#### 2.5.2 Visão de organização lógica

<p>O sistema é subdividido nos seguintes módulos.</p>

<ul>
<li><p><strong>Módulo de Apresentação (View):</strong></p>
  <ul>
    <li><strong>Composição:</strong> Desenvolvido com HTML, CSS e JavaScript.</li>
    <li><strong>Razão Lógica:</strong> É responsável unicamente pela interface com o usuário, apresentando as diferentes telas (mobile para garçom, desktop para cozinha) e capturando ações como "enviar pedido" ou "marcar como pronto".</li>
  </ul>
</li>
<li><p><strong>Módulo de Controle e Serviços (Controller/Service):</strong></p>
  <ul>
    <li><strong>Composição:</strong> Desenvolvido em linguagem Python utilizando o framework Flask.</li>
    <li><strong>Razão Lógica:</strong> Coordena todo o fluxo da aplicação. Este módulo recebe as requisições das telas, efetua as devidas validações, aplica regras de negócio (cálculos de contas, existência da mesa) e determina as ações para persistência.</li>
  </ul>
</li>
<li><p><strong>Módulo de Modelo e Persistência (Model/Repository/Database):</strong></p>
  <ul>
    <li><strong>Composição:</strong> Composto pelas entidades fundamentais do sistema e o banco de dados MySQL.</li>
    <li><strong>Razão Lógica:</strong> Este módulo serve para modelar o domínio (Pedido, ItemPedido, Mesa, Produto e Usuário) e garantir a integridade e isolamento na persistência física dos dados.</li>
  </ul>
</li>
</ul>

<p><strong>Como eles se comunicam (Interfaces):</strong></p>

<p>A camada de Apresentação (View) comunica-se com os Controladores (backend) através de API REST utilizando o protocolo HTTP/HTTPS.</p>

<p>Para garantir o fluxo reverso dinâmico e em tempo real (como a cozinha notificando o garçom de que um prato finalizou), utiliza-se conexão assíncrona (WebSockets) entre a camada de Serviço e as Views.</p>

<p>Internamente, o Controller utiliza a camada de Service (regras de negócio) para se comunicar de maneira contínua com o Model e os Repositories, que por sua vez persistem e consultam as informações diretamente no banco de dados MySQL.</p>

<p><strong>Figura 3 - Diagrama de Pacotes</strong></p>

![Figura 3 - Diagrama de Pacotes](img/diagrama-de-pacotes.png)

<p><em>Fonte: Elaborado pelos autores (2026)</em></p>

#### 2.5.3 Visão estrutural

<p><strong>Figura 4 - Diagrama de Classes</strong></p>

![Figura 4 - Diagrama de Classes](img/diagrama-de-classes.png)

<p>A Figura 4 ilustra o Diagrama de Classes, delimitando o escopo do produto e as interações entre os atores externos e as funcionalidades do sistema.</p>

<p><strong>Detalhamento dos Atores e Interações:</strong></p>

<ul>
<li><strong>Atores Primários:</strong> O diagrama identifica três perfis distintos com responsabilidades segregadas: Administrador, Garçom e Cozinheiro. Essa separação é refletida na arquitetura de segurança e controle de acesso do sistema.</li>
<li><strong>Gestão de Pedidos (Garçom/Cozinheiro):</strong> O núcleo operacional do sistema é representado pelos casos de uso "Fazer pedido", "Visualizar pedidos" e "Atualizar status do pedido". A interação entre esses atores através do sistema mitiga falhas de comunicação e agiliza o tempo de atendimento.</li>
<li><strong>Gestão Administrativa (Administrador):</strong> O ator administrador possui permissões exclusivas para a manutenção do ecossistema, incluindo "Gerenciar mesas", "Gerenciar produtos" e "Gerenciar usuários", garantindo a integridade dos dados cadastrais utilizados nas operações de salão.</li>
<li><strong>Fechamento de Ciclo:</strong> O caso de uso "Fechar conta" encerra o fluxo operacional, integrando as seleções feitas pelo garçom com o cálculo financeiro final, conforme as regras de negócio estabelecidas.</li>
</ul>

<p><strong>Relevância Arquitetural:</strong></p>

<p>O mapeamento da Figura 4 serve como base para a definição das rotas da API no backend e para a construção das interfaces no frontend. Cada caso de uso representado foi priorizado para atender aos requisitos funcionais e garantir que a arquitetura lógica suporte a carga de trabalho simultânea de múltiplos atores.</p>

<p><em>Fonte: Elaborado pelos autores (2026)</em></p>

### 2.6 Visão de Implantação

<p>Descreve como o sistema será distribuído fisicamente, focando no modelo Cliente-Servidor para garantir a sincronização em tempo real entre salão e cozinha.</p>

<ul>
<li><strong>Dispositivos Clientes:</strong>
  <ul>
    <li><strong>Interface Mobile:</strong> O processo inicia com a autenticação do usuário. Após o login, o garçom executa as atividades de seleção de mesa e montagem do pedido. A atividade "Confirmar/Enviar" representa o gatilho de integração, onde os dados são despachados via API para o processamento central.</li>
    <li><strong>Interface Desktop:</strong> Esta parte descreve o ciclo de vida operacional na cozinha. O sistema KDS (Kitchen Display System) recebe o pedido e gerencia as atividades de "Preparação" e "Marcar Pronto". Esta transição é crítica para garantir a redução da carga cognitiva e eliminar o uso de papel.</li>
    <li><strong>Entrega &amp; Fechamento:</strong> Descreve as atividades finais do ciclo de atendimento. A "Notificação/Retirada" serve como ponte de retorno para o salão, seguida pela "Entrega na Mesa" e a atividade financeira de "Pagamento/Fim", que culmina na liberação de recursos do sistema.</li>
  </ul>
</li>
<li><strong>Banco de Dados:</strong> O banco de dados será isolado da camada de aplicação para maior segurança, usando um sistema de gerenciamento relacional para garantir a consistência dos produtos cadastrados, além do registro de transações financeiras e pedidos.</li>
<li><strong>Conectores:</strong> A comunicação entre frontend e backend será feita via Protocolo HTTP.</li>
</ul>

<p><strong>Figura 5 - Diagrama de Implantação</strong></p>

![Figura 5 - Diagrama de Implantação](img/diagrama-de-implantacao.png)

<p><em>Fonte: Elaborado pelos autores (2026)</em></p>

### 2.7 Restrições adicionais

<p>Esta seção detalha limitações e requisitos de qualidade que o sistema deve seguir.</p>

<p><strong>Aspectos negociais:</strong></p>

<p>O software será acessível diretamente pela Internet e otimizado para a rede local do estabelecimento para evitar latência no envio de pedidos para cozinha. O produto exigirá obrigatoriamente a identificação e login do usuário (funcionário do restaurante) para qualquer operação de pedido. O sistema estará preparado para atender múltiplos usuários logados simultaneamente durante horários de pico do restaurante.</p>

<p><strong>Característica de Qualidade de Software:</strong></p>

<p><strong>Confiabilidade:</strong> Caso haja uma queda momentânea de conexão, o sistema não deve perder dados de pedidos.</p>
<p><strong>Usabilidade:</strong> A interface seguirá padrões de design que possibilitem o uso com apenas uma mão, no caso dos garçons, facilitando o trabalho deles.</p>

<hr />

## 3. Bibliografia

<p>IBM. Modelo cliente/servidor. IBM Documentation, [s. d.]. Disponível em: <a href="https://www.ibm.com/docs/pt-br/cics-ts/5.6.0?topic=programs-clientserver-model">https://www.ibm.com/docs/pt-br/cics-ts/5.6.0?topic=programs-clientserver-model</a>. Acesso em: 14 maio 2026.</p>

<p>SERRANO, Milene. Arquitetura de Software: Visão Geral. [S.l.]: Engenharia de Software UnB/FGA, 2026. 1 arquivo (70 slides), PDF.</p>