# Política de Commits e Branches

## Padrão de Mensagens (Conventional Commits)
Utilizamos o padrão **Conventional Commits** para manter o histórico legível e facilitar a geração de changelogs.

**Estrutura:**
`tipo: descrição`

**Tipos permitidos:**

- `feat`: Nova funcionalidade

- `fix`: Correção de bug

- `docs`: Mudanças na documentação

- `style`: Formatação, ponto-e-vírgula, etc (sem alteração de código)

- `refactor`: Refatoração de código

- `test`: Adição ou correção de testes

- `chore`: Atualização de tarefas de build, pacotes, etc.

**Exemplo:**
`feat: adiciona endpoint para fechamento de conta`

## Política de Branches
- `main`: Código em produção. Apenas recebe merges via Pull Request.
- `develop`: Integração contínua. Base para novas funcionalidades.
- `feature/*`: Criação de novas funcionalidades a partir da `develop`.