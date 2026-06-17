# Grupo Dijkstra - Nexus Gourmet 
## VISÃO DO PRODUTO E DO PROJETO 

 **Versão:** 1.1 [cite: 291]

###  Tabela - Integrantes do Grupo: [cite: 292]

| Matrícula | Nome | Função (responsabilidade) | Pontos de participação na elaboração |
| :--- | :--- | :--- | :--- |
| 242004457 | Alexandre Henrique Almeida Valadares Sousa | Banco de dados |  10 [cite: 293] |
| 242028655 | Davi Kenichi Watanabe Sakai | Frontend |  10 [cite: 293] |
| 241025953 | Igor Lima Carneiro | Backend |  10 [cite: 293] |
| 242005329 | Jhonatan William Araújo de Almeida | Banco de dados |  10 [cite: 293] |
| 242015432 | João Gabriel Rolim Veiga | Backend |  10 [cite: 293] |
| 241039322 | João Paulo Jacomini Batista | Frontend |  10 [cite: 293] |
| 241039304 | João Victor Amorim Kurihara | Frontend | 10 [cite: 293] |
| 242024253 | Lucas Ferreira Santana | Backend |  10 [cite: 293] |
| 242024271 | Lucas Peixoto Rodrigues | Backend |  10 [cite: 293] |
| 242005006 | Rafael de Aquino Marinho | Frontend |  10 [cite: 293] |

###  Histórico de Revisões [cite: 294]

| Data | Versão | Descrição | Autor |
| :--- | :--- | :--- | :--- |
| 30/04/2026 | 1.0 | Criação da primeira versão do documento |  Grupo Dijkstra [cite: 295] |
| 02/06/2026 | 1.1 | Adicionado menções diretas às fontes bibliográficas usadas no corpo do documento e atualização dos sprints |  Grupo Dijkstra [cite: 295] |

---

##  1. VISÃO GERAL DO PRODUTO [cite: 297, 335]

###  1.1 Problema [cite: 298, 336]
 Segundo a Associação Brasileira de Bares e Restaurantes (ABRASEL, 2018), aproximadamente 50% dos estabelecimentos do setor encerram suas atividades em menos de dois anos de operação[cite: 337].  A causa raiz desse declínio raramente está ligada à qualidade da comida, e sim decorrente de falhas na gestão de pedidos, descontrole de estoque e ineficiência na comunicação interna[cite: 338].  O gerenciamento manual de pedidos, baseado em comandas de papel e interações verbais, está fadado ao erro (ALELO, 2024)[cite: 339]. 

 O fluxo de informações em um restaurante é dinâmico e demanda alta carga cognitiva, onde a perda de um único pedaço de papel pode significar a interrupção de toda a experiência do cliente e a perda direta de receita (CLOUDFY, 2025)[cite: 340].  A anotação em papel é uma interface de entrada de dados de baixíssima fidelidade, sujeita a ambiguidades de caligrafia, falta de padronização em observações e total ausência de dados temporais[cite: 341]. 

 Sem o registro exato do momento em que o pedido foi feito, a cozinha perde a capacidade de medir o tempo médio de preparo, informação vital para a eficiência operacional do restaurante uma vez que a agilidade é um dos fatores mais valorizados pelos consumidores modernos[cite: 342].  Focando na falta de rastreabilidade, falhas de comunicação entre salão e cozinha e desorganização logística, revela-se a necessidade de desenvolver um software que solucione a problemática do registro e acompanhamento de pedidos[cite: 343]. 

 O sistema deve permitir a entrada de pedidos via dispositivos móveis (garçons) e enviá-los imediatamente para telas na cozinha, organizando-os por prioridade e tempo de preparo, eliminando a necessidade de impressoras, além de possuir interfaces intuitivas que exijam o mínimo de treinamento possível para a equipe, considerando a alta rotatividade de funcionários no setor de foodservice[cite: 344].

 *Figura 1 - Ineficiência no registro e acompanhamento de pedidos (Diagrama de Causa-Efeito / Ishikawa)* [cite: 345, 346]

###  1.2 Declaração de posição do produto [cite: 299, 347]
 A tabela 1 condensa o posicionamento estratégico do Nexus Gourmet, apresentando seu público-alvo, necessidade no ambiente, sua categoria e vantagens em relação às alternativas existentes[cite: 348].

####  Tabela 1 – Posicionamento estratégico do produto [cite: 300, 349]

| Diretriz | Definição |
| :--- | :--- |
| **Para:** |  Proprietários e funcionários de restaurantes de qualquer porte [cite: 350] |
| **Necessidade:** |  Registrar, acompanhar e gerenciar pedidos de forma centralizada, ágil e sem erros [cite: 350] |
| **O Nexus Gourmet:** |  É uma aplicação WEB - mobile denominada Nexus Gourmet [cite: 350] |
| **Que:** |  Permite o registro digital de pedidos por mesa, o acompanhamento do status em tempo real pela cozinha e o fechamento de conta pelos garçons [cite: 350] |
| **Ao contrário:** |  Do registro manual em papel e da comunicação verbal entre garçom e cozinha, que estão sujeitos a erros, perdas de informação e ausência de rastreabilidade [cite: 350] |
| **Nosso produto:** |  Integra o fluxo completo do pedido — do salão à cozinha — com atualização em tempo real, dispensando qualquer infraestrutura adicional além de um navegador web [cite: 350] |

 **Fonte:** realizado pelo autor (2026) [cite: 301, 351]

###  1.3 Objetivos do Produto [cite: 302, 352]

####  Objetivo Principal [cite: 353]
*  O Nexus Gourmet objetiva, principalmente, desenvolver um software que centralize o processo de registro, acompanhamento e gerenciamento de pedidos de restaurantes, eliminando a dependência de anotações manuais[cite: 354].

####  Objetivos Secundários [cite: 355]
*  Melhorar o gerenciamento de insumos consumidos pelo cliente[cite: 356].
*  Oferecer visibilidade em tempo real do status de cada pedido (NOX, 2025; OLITECNICA, 2025)[cite: 357].
*  Facilitar o gerenciamento de mesas (THEFORKMANAGER, 2025)[cite: 358].
*  Automatizar o cálculo e a geração da conta ao final do atendimento[cite: 359].

###  1.4 Tecnologias a Serem Utilizadas [cite: 303, 360]
*  **Frontend:** HTML, CSS & JavaScript [cite: 361]
*  **Backend:** Python [cite: 362]
*  **Banco de Dados:** MySQL [cite: 363]
*  **Frameworks/Bibliotecas:** Flask [cite: 364]
*  **Ferramentas adicionais:** GitHub, Microsoft Word, Visual Studio Code [cite: 365]

---

##  2. VISÃO GERAL DO PROJETO [cite: 304, 366]

###  2.1 Ciclo de vida do projeto de desenvolvimento de software [cite: 305, 367]
 Para o desenvolvimento do sistema de gerenciamento de pedidos, adotamos uma abordagem embasada nas práticas ágeis[cite: 368].  Essa escolha se justifica pela necessidade de entregas contínuas, validação constante com os usuários finais e a capacidade de adaptação a requisitos dinâmicos característicos do setor de foodservice[cite: 369].  A seguir, detalhamos a instanciação do ciclo de vida do projeto com base na arquitetura de metodologias[cite: 370]:

####  2.1.1 Metodologia: Metodologia Ágil [cite: 306, 371]
 A escolha pela agilidade se dá pelo foco na entrega de valor e pela flexibilidade[cite: 372].  Como o ambiente de restaurantes exige alta usabilidade e eficiência operacional, uma abordagem ágil permite que o grupo ajuste prioridades no Backlog do Produto e planeje o escopo conforme os riscos são identificados e mitigados, sem engessar o desenvolvimento[cite: 373].

####  2.1.2 Processo [cite: 307, 374]
 Utilizaremos um processo orientado pelo Scrumban (uma abordagem híbrida que combina a estrutura do Scrum com o fluxo contínuo do Kanban), apoiado por práticas de engenharia do XP (Extreme Programming)[cite: 375].  O Scrumban nos permite manter os papéis definidos (Dono do Produto, Desenvolvedores e Analistas de Qualidade) e o planejamento em ciclos curtos de uma semana (Sprints), mas com a adoção de um fluxo contínuo (sistema pull) e limites de trabalho em andamento (WIP – Work in Progress) para evitar gargalos na equipe[cite: 376].

####  2.1.3 Procedimentos [cite: 377]
 O trabalho fluirá através de iterações baseadas em Sprints, iniciando com uma Sprint Planning para puxar as tarefas prioritárias (como as funcionalidades Must) para o quadro de desenvolvimento[cite: 378].  O acompanhamento diário e o gerenciamento de riscos serão guiados visualmente pelo quadro Kanban, garantindo transparência do que está a fazer, em haven e concluído[cite: 379].  Ao final do ciclo, as entregas passarão por avaliações de qualidade baseadas nas métricas do GQM[cite: 380].

####  2.1.4 Métodos [cite: 308, 381]
*  **Quadro Kanban e Limites de WIP:** Gestão visual do fluxo de tarefas para identificar rapidamente impedimentos e limitar a quantidade de itens em desenvolvimento simultâneo, garantindo foco na conclusão[cite: 382].
*  **Histórias de usuário:** Utilizadas para mapear o Backlog do produto de forma focada (Administrador, Garçom, Cozinheiro)[cite: 383].
*  **Testes de Software:** Implementação de testes para mitigar riscos de comunicação entre interfaces, buscando manter a densidade de erros de programa em níveis mínimos (≤ 0.5%)[cite: 384].
*  **Refatoração Contínua:** Prática do XP para manter o código limpo e otimizado, assegurando os tempos de execução e de comunicação em tempo real esperados pelo sistema[cite: 385].

####  2.1.5 Ferramentas [cite: 309, 386]
*  **Codificação:** Visual Studio Code utilizando HTML, CSS, JavaScript para o frontend e Python com Flask e MySQL para o Backend[cite: 387].
*  **Design e Prototipagem:** Figma, para desenhar interfaces intuitivas e responsivas[cite: 388].
*  **Versionamento e Gestão:** Git, centralizando o código no GitHub, que também poderá ser utilizado para a gestão visual do Kanban[cite: 389].
*  **Comunicação da Equipe:** Teams, Discord e WhatsApp[cite: 390].

###  2.2 Organização do Projeto [cite: 310, 391]
 A tabela 2 apresenta as atribuições e deveres de cada membro do grupo, ou seja, as responsabilidades escolhidas pelos membros participantes[cite: 392].

####  Tabela 2 - Divisão de funções [cite: 393]

| Papel | Atribuições | Responsável | Participantes |
| :--- | :--- | :--- | :--- |
| **Desenvolvedor** | Esses membros ficam responsáveis por fazer com que o projeto funcione através das iterações de código e banco de dados | Igor, Davi Sakai, João Gabriel, Jhonatan William |  Igor, Davi Sakai, João Gabriel, João Amorim, Jhonatan William [cite: 394] |
| **Dono do Produto** | Esse membro(s) fica responsável por validar os requisitos e backlog do produto seria como um representante do cliente na equipe | Rafael de Aquino |  Rafael de Aquino [cite: 394] |
| **Analista de Qualidade** | Esses membros ficam responsáveis por avaliar a qualidade do produto e decidir se a iteração está pronta para implementação, de acordo com conceito de pronto do time. | Lucas Peixoto, Alexandre, Lucas Ferreira |  Lucas Peixoto, Alexandre, Lucas Ferreira [cite: 394] |
| **Cliente (monitor)** | Avaliar se o projeto está de acordo com os requisitos e proposta inicial | Lucas Ferreira |  Lucas Ferreira [cite: 394] |

 **Fonte:** realizado pelo autor (2026) [cite: 395]

###  2.3 Planejamento das Fases e/ou Iterações do Projeto [cite: 311, 396]
 O planejamento de Fases tem como objetivo demonstrar o que foi feito em cada sprint, o período que ela durou e as entregas feitas durante ou ao final da iteração[cite: 397]. O planejamento também deixa claro qual o grau de conclusão do projeto.  A tabela 3 abaixo apresenta esses dados[cite: 398].

####  Tabela 3 - Planejamento das fases [cite: 399]

| Sprint | Produto (Entrega) | Data Início | Data Fim | Entregável(eis) | Responsáveis | % conclusão |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Sprint 1** | Definição geral do produto | 09/04/2026 | 16/04/2026 | - | Todos |  2% [cite: 400] |
| **Sprint 2** | Planejamento do projeto e DV | 23/04/2026 | 30/04/2026 | 1ª versão do Documento de Visão | Todos |  7% [cite: 400] |
| **Sprint 3** | Documento de arquitetura | 30/04/2026 | 14/05/2026 | 1ª versão do Documento de arquitetura | Todos |  13% [cite: 400] |
| **Sprint 4** | Preparação do Github | 20/05/2026 | 28/05/2026 | Pastas e documentos no git | Todos |  18% [cite: 400] |
| **Sprint 5** | Início do Desenvolvimento | 28/05/2026 | 04/06/2026 | Models, Controllers e Services; atualização dos documentos | Igor Lima, João Gabriel, Lucas Ferreira, Lucas Peixoto |  20% [cite: 400] |
| **Sprint 6** | Integração dos models, services e controllers; desenvolvimento do banco de dados | 04/06/2026 | 11/06/2026 | Banco de dados + atualizações do backend | Alexandre, Igor Lima, Jhonatan, João Gabriel, Lucas Ferreira, Lucas Peixoto |  45% [cite: 400] |
| **Sprint 7** | Integração entre o backend e o frontend; | 11/05/2026 | 18/06/2026 | Entrega da view de login e do administrador | Davi, João Paulo, João Victor, Rafael |  65% [cite: 400] |
| **Sprint 8** | - | - | - | - | - |  ? [cite: 400] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 401]

###  2.4 Matriz de Comunicação [cite: 312, 402]
 A tabela 4 apresenta como serão feitas as comunicações entre o grupo e a monitora[cite: 403].  Além disso, mostrará quais são as fontes de informação geradas pelo grupo, sobre o projeto, e onde elas estarão disponíveis para a consulta das iterações[cite: 404].

####  Tabela 4 - Matriz de comunicação [cite: 405]

| Descrição | Área/Envolvidos | Periodicidade | Produtos Gerados |
| :--- | :--- | :--- | :--- |
| Acompanhamento das atividades em andamento via Teams, WhatsApp e acompanhamento dos riscos, compromissos, ações pendentes via GitHub. | Equipe do Projeto | Semanal / Quinzenal |  Ata de reunião, Relatório de situação do projeto [cite: 406] |
| Comunicar a situação do projeto | Equipe do Projeto + monitor | Semanal |  Ata de reunião, Relatório de situação do projeto [cite: 406] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 407]

###  2.5 Gerenciamento de Riscos [cite: 313, 408]
 O Gerenciamento de Riscos consiste na identificação, avaliação, priorização, tratamento e monitoramento de possíveis ameaças tanto internas quanto externas[cite: 409].  O objetivo é promover a continuidade, a segurança no trabalho, a tomada de decisões e a redução de custos[cite: 410].

####  Tabela 5 - Gerenciamento de riscos [cite: 412]

| Risco | Grau de exposição | Mitigação | Plano de contingência |
| :--- | :--- | :--- | :--- |
| Alteração de requisitos do backlog do produto após o início da sprint | Alto | Aumentando o período de refinamento do backlog do produto |  Reunir os requisitos que já estão acordados e aumentar o grau de prioridade [cite: 413] |
| Falta de comunicação entre as interfaces do sistema | Alto | Implementação de Testes de Software para garantir a redução de atrasos |  Revisão completa de todos as unidades do código em larga escala para solução do problema [cite: 413] |
| Dificuldades com as tecnologias usadas no projeto (SQL, Flask, etc.) | Médio | Preparação rápida para a implementação básica dessas tecnologias |  Solicitar ajuda externa para o auxílio das atividades (monitores, professores, tutores etc.) [cite: 413] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 414]

###  2.6 Critérios de Replanejamento [cite: 314, 415]
 A seguir, a tabela 6 apresenta os critérios de replanejamento e as ações que serão tomadas para replanejar os seguimentos afetados[cite: 416]:

####  Tabela 6 - Critérios de replanejamento [cite: 417]

| Risco | Critério de Replanejamento | Ação de Replanejamento |
| :--- | :--- | :--- |
| Atraso na entrega de funcionalidades | Atraso, igual ou superior a 1 sprint, na entrega de uma funcionalidade em relação ao cronograma |  Alterar as prioridades de entrega e ajustar o backlog [cite: 418] |
| Necessity de alterar o escopo | Funcionalidades Must não estão sendo realizadas de acordo com o cronograma planejado |  Replanejar as funcionalidades que seriam trabalhadas em sprints futuras [cite: 418] |
| Falta de comunicação entre os membros do projeto | Dificuldade de comunicação com um membro por 3 dias |  Ajustes na divisão e nas responsabilidades atribuídas aos membros [cite: 418] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 419]

---

##  3. PROCESSO DE DESENVOLVIMENTO DE SOFTWARE [cite: 315, 420]
 O desenvolvimento do sistema Nexus Gourmet será conduzido com base na metodologia ágil, por meio da abordagem híbrida Scrumban, complementada por práticas de engenharia de software oriundas do Extreme Programming (XP)[cite: 421].  Essa combinação visa proporcionar flexibilidade, organização e melhoria contínua ao longo de todo o ciclo de vida do projeto[cite: 422].

###  3.1 Principais Práticas Adotadas [cite: 423]
*  **Sprint Planning:** Reunião realizada no início de cada Sprint com o objetivo de selecionar, priorizar e detalhar as funcionalidades a serem desenvolvidas[cite: 425].
*  **Sprint Review:** Encontro ao término de cada Sprint para apresentação das funcionalidades implementadas e validação[cite: 426].
*  **Sprint Retrospective:** Reunião destinada à reflexão sobre o processo, identificando pontos de melhoria[cite: 427].
*  **Gestão Visual com Kanban:** Utilização de quadro Kanban (a fazer, em andamento, em validação e concluído)[cite: 428].
*  **Limitação de WIP (Work in Progress):** Estabelecimento de limites para o número de tarefas em andamento simultaneamente[cite: 429].
*  **Pair Programming (XP):** Prática aplicada em funcionalidades críticas ou de maior complexidade[cite: 430].
*  **Code Review (XP):** Revisão sistemática do código desenvolvido para garantir padrões de qualidade[cite: 431].
*  **Testes Contínuos (XP):** Execução de testes unitários, de integração e manuais durante todo o desenvolvimento[cite: 432].
*  **Refinamento Contínuo do Backlog:** Atualização periódica com base no feedback do cliente e prioridades de negócio[cite: 433].

###  3.2 Ferramentas de Suporte [cite: 434]
*  **Versionamento:** Git + GitHub [cite: 436]
*  **Documentação:** GitHub Pages [cite: 437]
*  **Prototipagem:** Figma [cite: 438]
*  **Comunicação:** Teams, Discord e WhatsApp [cite: 439]

####  Tabela 7 - Papéis [cite: 441]

| Papéis | Responsabilidades | Integrantes |
| :--- | :--- | :--- |
| **Dono do produto** | Responsável por validar os requisitos e o backlog do produto, atuando como representante do cliente na equipe |  Rafael de Aquino [cite: 442] |
| **Desenvolvedores** | Responsáveis pela implementação técnica do sistema, incluindo código, banco de dados e iterações de desenvolvimento |  Davi Sakai, Igor Lima, Jhonatan William, João Gabriel, João Amorim e João Paulo [cite: 442] |
| **Analistas de Qualidade** | Responsáveis por avaliar a qualidade do produto e validar se as iterações estão prontas para implementação conforme o conceito de "pronto" do time |  Alexandre Sousa, Lucas Peixoto e Lucas Ferreira [cite: 442] |
| **Cliente** | Responsável por avaliar se o projeto está de acordo com os requisitos e a proposta inicial do Nexus Gourmet |  Lucas Ferreira [cite: 442] |

 *Figura 2 – Ciclo de vida adotado no Nexus Gourmet (Planejamento da Sprint -> Desenvolvimento -> Review/Demo -> Retrospectiva -> Refinamento do Backlog).* [cite: 443, 444]

---

##  4. DECLARAÇÃO DE ESCOPO DO PROJETO [cite: 318, 445]

###  4.1 Backlog do produto [cite: 319, 446]
 A Tabela 8 apresenta o backlog do produto, composto pelo conjunto de funcionalidades identificadas para o sistema[cite: 447, 448].

####  Tabela 8 – Backlog [cite: 449]

| ID | Funcionalidade | Descrição | Prioridade |
| :--- | :--- | :--- | :--- |
| F01 | Abrir pedido | O garçom deve poder abrir um pedido vinculado a uma mesa |  Alta [cite: 450] |
| F02 | Adicionar item ao pedido | O garçom deve poder adicionar itens do cardápio a um pedido em aberto |  Alta [cite: 450] |
| F03 | Remove item do pedido | O garçom deve poder remover itens de um pedido em aberto |  Alta [cite: 450] |
| F04 | Enviar pedido para a cozinha | O garçom deve poder enviar o pedido, alterando seu status para "em preparo" |  Alta [cite: 450] |
| F05 | Visualizar pedidos na cozinha | O cozinheiro deve poder visualizar todos os pedidos ativos organizados por status |  Alta [cite: 450] |
| F06 | Visualizar tempo de espera | O cozinheiro deve poder visualizar o tempo decorrido desde a abertura de cada pedido |  Alta [cite: 450] |
| F07 | Atualizar status do pedido | O cozinheiro deve poder marcar um pedido como "em preparo" ou "pronto" |  Alta [cite: 450] |
| F08 | Fechar conta | O garçom deve poder fechar a conta de uma mesa, gerando o total e liberando a mesa |  Alta [cite: 450] |
| F09 | Calcular total do pedido | O sistema deve calcular automaticamente o valor total do pedido com base nos itens e quantidades |  Média [cite: 450] |
| F10 | Visualizar mesas | O sistema deve exibir todas as mesas do restaurante com seus respectivos status |  Média [cite: 450] |
| F11 | Cadastrar produtos | O administrador deve poder cadastrar novos produtos no cardápio, informando nome, categoria e preço |  Alta [cite: 450] |
| F12 | Editar produto | O administrador deve poder editar as informações de um produto já cadastrado |  Média [cite: 450] |
| F13 | Remover produto | O administrador deve poder remover um produto do cardápio |  Média [cite: 450] |
| F14 | Cadastrar mesa | O administrador deve poder cadastrar novas mesas, informando número e capacidade |  Alta [cite: 450] |
| F15 | Editar mesa | O administrador deve poder editar as informações de uma mesa já cadastrado |  Média [cite: 450] |
| F16 | Remover mesa | O administrador deve poder remover uma mesa do sistema |  Média [cite: 450] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 451]

###  4.2 Perfis [cite: 320, 452]
 A Tabela 9 apresenta os perfis de usuário do sistema, descrevendo o papel de cada ator no contexto do restaurante e as responsabilidades[cite: 453, 454].

####  Tabela 9: Perfis de acesso [cite: 455]

| # | Nome do perfil | Características do perfil | Permissões de acesso |
| :--- | :--- | :--- | :--- |
| P01 | Administrador | Responsável pela gestão operacional do sistema |  Cadastrar, editar e remover produtos do cardápio e mesas do restaurante [cite: 456] |
| P02 | Garçom | Funcionário responsável pelo atendimento no salão |  Abrir pedidos, registrar itens, enviar pedidos para a cozinha e fechar contas [cite: 456] |
| P03 | Cozinheiro | Funcionário responsável pelo preparo dos pedidos |  Visualizar pedidos ativos, acompanhar tempo de espera e atualizar status dos pedidos [cite: 456] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 457]

###  4.3 Cenários [cite: 321, 458]
 A Tabela 10 organiza exemplos práticos de como os usuários interagem com o sistema[cite: 459, 460].  Os itens não possuem sprint definida (planeamentos futuros)[cite: 461].

####  Tabela 10: Cenários funcionais [cite: 463]

| N | Ator | Contexto | Passos | Sprints |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Administrador | Deseja registrar uma nova mesa | Acessar "Cadastro de Mesas", preencher número, capacidade e salvar. |  - [cite: 464] |
| 2 | Garçom | Deseja receber o pedido de uma mesa | Selecionar a mesa desejada, clicar em “abrir pedido” e selecionar os itens desejados |  - [cite: 464] |
| 3 | Cozinha | Deseja despachar um pedido finalizado | Selecionar o pedido e clicar em “pronto”, para que o garçom venha retirar |  - [cite: 464] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 465]

###  4.4 Tabela de Backlog do Produto [cite: 466]
####  Tabela 11: Backlog do produto [cite: 467]
 *(Template do sistema para mapeamento de User Stories)* [cite: 468]

| Numeração (Cenário / requisito) | Sprint | Nome do requisito | Tipo de requisito (Funcional / não funcional) | Priorização do requisito (Must, Should, Could) | Descrição sucinta do requisito | User histories (U.S.) associadas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | | | | |

---

##  5. MÉTRICAS E MEDIÇÕES [cite: 322, 469]

###  5.1 GQM de medições [cite: 323, 470]
 O Goal Question Metrics (GQM) foi elaborado com o intuito de estabelecer as métricas do projeto com base nas expectativas dos stakeholders e riscos de comunicação/prazos[cite: 471, 472, 473, 474].

####  Tabela 12 - GQM do produto [cite: 475]

| Objetivo | Pergunta | Métrica | Cálculo | Escala | Valor esperado | Forma de análise |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Validar taxa de conclusão da sprint | As funcionalidades planejadas foram entregues? | Taxa de conclusão da sprint | (Qtd de func planejadas) - (qtd não entregues) | unitária | Número de func entregáveis para a sprint |  Sprint Reviews e Sprint Meetings [cite: 476] |
| Validar qualidade de implementação | O software está bem implementado? | Densidade de erros por sprint | - | - | - |  Refatoração [cite: 476] |
| Obediência ao período dos sprints | Os sprints estão entregando todos os musts? | Densidade de prorrogações de musts | (Qtd musts prorrogados)/(Total Musts do Sprint) x 100 | % | ≤ 0% |  Sprint Reviews e Sprint Meetings [cite: 476] |
| Usabilidade da Interface de usuário | A interface é intuitiva e perfeitamente utilizável? | Densidade de feedback negativo | (Reports negativos)/(Total Reports) x 100 | % | ≤ 2% |  Alinhamento de requisitos e avaliação do cliente [cite: 476] |
| Verificar quantidade de pedido por garçom | Qual garçom faz mais pedidos? | Densidade de pedidos por garçom | (Pedidos por garçom)/(Pedidos totais) x 100 | % | ≥(Qtd pedidos particulares)/(Pedidos totais) |  Quantidade de contas abertas por garçom [cite: 476] |
| Verificar tempo médio de preparo por produto | Qual o tempo médio que um produto é entregue? | Tempo de entrega | (Horário de entrega) - (Horário do pedido) | min | ≤(Média de entrega do produto) |  Tempo gasto entre abertura e entrega na mesa [cite: 476] |
| Verificar saída de produto | Qual a porcentagem de saída de cada produto? | Densidade de pedidos do produto | (Pedido do produto)/(Pedidos totais) x 100 | % | (Pedidos totais)/(Qtd de produtos) |  Quantidade de vezes que o pedido foi feito [cite: 476] |

 **Fonte:** Elaborado pelo autor (2026) [cite: 477]

---

##  6. TESTES DE SOFTWARE [cite: 324, 478]

###  6.1 Estratégia de testes contendo: [cite: 325, 479]

####  6.1.1 Testes implementados em níveis [cite: 326, 480]
*  **Testes Unitários:** Testam o código de forma isolada, validando a menor unidade funcional, prevenindo que bugs pequenos cheguem à produção[cite: 482].
*  **Testes de Integração:** Verificam como diferentes partes do programa trabalham em conjunto, validando a interface entre módulos e bancos de dados[cite: 483].
*  **Testes de Sistema:** Validam o software como um todo, avaliando o desempenho, estabilidade e segurança frente aos requisitos[cite: 484, 485].

####  6.1.2 Testes Funcionais [cite: 327, 486]
Fundamentais para validação e usabilidade.  Verificam regras de negócio como login funcional, bloqueio de sistema e registro de pedidos[cite: 487, 488].

####  6.1.3 Ambientes de Teste e Política de Branches e Commits [cite: 328, 489]
 Uso organizado de ambientes integrados ao Git/GitHub[cite: 490].

#####  6.1.3.1 Ambientes de Teste [cite: 329, 491]
*  **Ambiente de Desenvolvimento (Dev):** Implementação local (HTML, CSS, JS, Python/Flask, MySQL)[cite: 493, 494].
*  **Ambiente de Homologação (QA):** Validação de funcionalidades integradas através de testes funcionais e não funcionais[cite: 495, 496].
*  **Ambiente de Produção (Prod):** Disponibilização final aos usuários (Documentação via GitHub Pages)[cite: 497, 498].

#####  6.1.3.2 Política de Branches [cite: 330, 499]
* `main`: Ambiente de produção.  Apenas código validado e estável[cite: 501].
*  `develop`: Ambiente de homologação (QA)[cite: 502].
*  `feature/*`: Desenvolvimento de novas funcionalidades, derivadas da branch develop[cite: 503].

#####  6.1.3.3 Política de Commits e Integração [cite: 331, 504]
Commits frequentes nas features. Integração com a branch `develop` via Pull Requests com Code Review.  Após validação em QA, promoção para a `main`[cite: 505, 506, 507, 508].

####  6.1.4 Análise dos Testes [cite: 332, 509]
Baseada na comparação entre resultados previstos e reais.  Investigação de falhas e retestagem caso ocorram erros[cite: 510, 511].  *Nota: Ainda não foram obtidos testes por estar em fase inicial*[cite: 512].

###  6.2 Roteiro de teste [cite: 333, 513]
 Realizados em branch dedicada para não impactar o código principal[cite: 514, 515, 516].

####  Tabela 13 - Teste Unitário 1 [cite: 517]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU01 [cite: 518] |
| **Nome** |  Login com credenciais [cite: 518] |
| **Objetivo** |  Verificar se a função de autenticação retorna sucesso com credenciais válidas [cite: 518] |
| **Nível** |  Unitário [cite: 518] |
| **Tipo** |  Funcional [cite: 518] |
| **Precondições** |  Método de login implementado e usuário válido cadastrado [cite: 518] |
| **Estado** |  - [cite: 518] |
| **Resultados** |  Previsto: autenticação bem-sucedida / Realizado: - [cite: 518] |
| **Reparos** |  - [cite: 518] |
| **Ciclos** |  - [cite: 518] |

####  Tabela 14 - Teste Unitário 2 [cite: 520]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU02 [cite: 521] |
| **Nome** |  Abrir comanda / pedido [cite: 521] |
| **Objetivo** |  Verificar se a função abrir comanda está funcionando como o esperado [cite: 521] |
| **Nível** |  Unitário [cite: 521] |
| **Tipo** |  Funcional [cite: 521] |
| **Precondições** |  Método de abrir comanda implementado [cite: 521] |
| **Estado** |  - [cite: 521] |
| **Resultados** |  Previsto: Abertura da comanda / Realizado: - [cite: 521] |

####  Tabela 15 - Teste Unitário 3 [cite: 523]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU03 [cite: 524] |
| **Nome** |  Visualizar comanda [cite: 524] |
| **Objetivo** |  Verificar se a função visualizar comanda retorna os dados da comanda escolhida [cite: 524] |
| **Nível** |  Integração [cite: 524] |
| **Tipo** |  Funcional [cite: 524] |
| **Precondições** |  Função visualizar comanda [cite: 524] |
| **Estado** |  - [cite: 524] |
| **Resultados** |  Previsto: Visualizar os dados da comanda / Realizado: - [cite: 524] |

####  Tabela 16 - Teste Unitário 4 [cite: 526]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU04 [cite: 527] |
| **Nome** |  Listar todas as comandas [cite: 527] |
| **Objetivo** |  Verificar se a função de listar todas as comandas dá os dados das comandas abertas [cite: 527] |
| **Nível** |  Unitário [cite: 527] |
| **Tipo** |  Funcional [cite: 527] |
| **Precondições** |  Função de listar todas as comandas [cite: 527] |
| **Estado** |  - [cite: 527] |
| **Resultados** |  Previsto: Fornecer os dados das comandas abertas / Realizado: - [cite: 527] |

####  Tabelas de Template (Tabelas 17 a 26 - TU05 a TU0X) [cite: 529, 532, 535, 538, 541, 544, 547, 550, 553, 556]
 *(Reservadas para novos casos de uso de adição e listagem de itens)* [cite: 530, 533, 536, 539, 542, 545, 548, 551, 554, 557]

####  Tabela 27 - Teste Unitário 15 [cite: 559]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU03 (Adicional) [cite: 560] |
| **Nome** |  Adicionar produto [cite: 560] |
| **Objetivo** |  Verificar se a função adicionar produto está funcionando [cite: 560] |
| **Nível** |  Unitário [cite: 560] |
| **Tipo** |  Funcional [cite: 560] |
| **Precondições** |  Função de adicionar produto implementada [cite: 560] |
| **Estado** |  - [cite: 560] |
| **Resultados** |  Previsto: Criação de produto funcional / Realizado: - [cite: 560] |

####  Tabela 28 - Teste Unitário 16 [cite: 562]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU04 (Adicional) [cite: 563] |
| **Nome** |  Editar produto [cite: 563] |
| **Objetivo** |  Verificar se os dados do produto são alterados ao usar a função de editar produto [cite: 563] |
| **Nível** |  Unitário [cite: 563] |
| **Tipo** |  Funcional [cite: 563] |
| **Precondições** |  Existência da função editar produto [cite: 563] |
| **Estado** |  - [cite: 563] |
| **Resultados** |  Previsto: Alternar os dados do produto / Realizado: - [cite: 563] |

####  Tabela 29 - Teste Unitário 17 [cite: 565]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU05 (Adicional) [cite: 566] |
| **Nome** |  Excluir produto [cite: 566] |
| **Objetivo** |  Verificar se os dados do produto são excluídos ao usar a função de excluir produto [cite: 566] |
| **Nível** |  Unitário [cite: 566] |
| **Tipo** |  Funcional [cite: 566] |
| **Precondições** |  Função de excluir produto [cite: 566] |
| **Estado** |  - [cite: 566] |
| **Resultados** |  Previsto: Remoção de produto funcional / Realizado: - [cite: 566] |

####  Tabela 30 - Teste Unitário 18 [cite: 568]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TU06 (Adicional) [cite: 569] |
| **Nome** |  Enviar comanda para cozinha [cite: 569] |
| **Objetivo** |  Verificar se os dados da comanda são enviados para a cozinha [cite: 569] |
| **Nível** |  Unitário [cite: 569] |
| **Tipo** |  Funcional [cite: 569] |
| **Precondições** |  Função de enviar comanda [cite: 569] |
| **Estado** |  - [cite: 569] |
| **Resultados** |  Previsto: Envio correto para painel de preparo / Realizado: - [cite: 569] |

####  Tabela 33 - Teste Integrado 1 [cite: 576]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TI01 [cite: 577] |
| **Nome** |  Integração entre backend e banco de dados [cite: 577] |
| **Objetivo** |  Verificar se o sistema armazena corretamente dados do banco [cite: 577] |
| **Nível** |  Integração [cite: 577] |
| **Tipo** |  Funcional [cite: 577] |
| **Precondições** |  Banco de dados ativo e conexão configurada [cite: 577] |
| **Estado** |  - [cite: 577] |
| **Resultados** |  Previsto: armazenamento e autenticação bem-sucedidos / Realizado: - [cite: 577] |

####  Tabela 34 - Teste Integrado 2 [cite: 579]
| Campo | Conteúdo |
| :--- | :--- |
| **Código** |  TI02 [cite: 580] |
| **Nome** |  Integração entre backend e frontend [cite: 580] |
| **Objetivo** |  Verificar se a interface consiga enviar e receber dados do programa [cite: 580] |
| **Nível** |  Integração [cite: 580] |
| **Tipo** |  Funcional [cite: 580] |
| **Precondições** |  Interface funcional e conectado à lógica do programa [cite: 580] |
| **Estado** |  - [cite: 580] |
| **Resultados** |  Previsto: comunicação fluida e renderização bem-sucedida / Realizado: - [cite: 580] |

---

##  7. REFERÊNCIAS BIBLIOGRÁFICAS [cite: 334, 582]
* **ABRASEL.** Solução KDS: ferramenta inovadora para auxiliar restaurantes.  Disponível em: https://abrasel.com.br/noticias/noticias/solucao-kds-ferramenta-innovadora-para-auxiliar-restaurantes/[cite: 583].
* **ALELO.** Qual o melhor tipo de comanda para restaurante?.  Disponível em: https://www.alelo.com.br/blog/estabelecimentos-comerciais/qual-o-melhor-tipo-de-comanda-para-restaurante[cite: 584].
* **CLOUDFY.** Os desafios na gestão de pedidos em bares e restaurantes.  Disponível em: https://www.cloudfy.net.br/blog/os-desafios-na-gestao-de-pedidos-em-bares-e-restaurantes.html[cite: 585].
* **ECLETICA.** E-Garçom: Transformando o Atendimento em Restaurantes.  Disponível em: https://ecletica.com.br/e-garcom-transformando-o-atendimento-restaurantes/[cite: 586].
* **NOX.** Sistema KDS: O que é, para que serve e como otimiza sua cozinha e cafeteria?.  Disponível em: https://nox.com.br/o-que-e-sistema-kds/?utm_medium=desktop[cite: 587].
* **OLITECNICA.** KDS: A revolução na gestão de pedidos para restaurantes e delivery.  Disponível em: https://www.olitecnica.com.br/post/kds-a-revolucao-na-gestao-de-pedidos-para-restaurantes-e-delivery[cite: 588].
* **THE FORKMANAGER.** Restaurant Table Turnover Rate Optimization.  Disponível em: https://www.theforkmanager.com/en/blog/restaurant-management/restaurant-table-turnover-tips-efficiency[cite: 589].