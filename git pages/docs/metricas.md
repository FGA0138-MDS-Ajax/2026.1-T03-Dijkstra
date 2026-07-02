# Relatório de Métricas

Este relatório consolida as métricas de acompanhamento do projeto Nexus Gourmet, baseado no **Goal Question Metrics (GQM)** definido no Documento de Visão (versão 1.4).

As métricas foram definidas com base em:

1. **Expectativas dos Stakeholders:** Entrega de testes intermediários e produto funcional.
2. **Riscos do projeto:** Comunicação da equipe, cumprimento de prazos e qualidade do código.

---

## Resumo Geral

| Métrica | Valor Atual | Status |
|---------|-------------|--------|
| Obediência ao período das sprints | 2 sprints com atraso | Atenção |
| Densidade de commits de correção | 22% | Atenção |
| Densidade de prorrogações de musts | Sprint 7: 16% | Atenção |
| Densidade de feedback negativo | 25% | Melhorar |
| Avaliação de utilidade | 8 | OK |
| Taxa de recomendação | 100% | Excelente |

---

## Métricas Detalhadas (GQM)

### 1. Validação da Sprint

**Objetivo:** Validar taxa de conclusão da sprint  
**Pergunta:** A sprint foi finalizada no período previsto?  
**Métrica:** Obediência ao período das sprints  
**Cálculo:** Número de atraso da entrega de todo o planejado em relação à sprint  
**Escala:** Unitária  
**Valor esperado:** 0  
**Forma de análise:** Implementação de Sprint Reviews e Sprint Meetings

**Resultados:**

| Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Sprint 5 | Sprint 6 | Sprint 7 | Sprint 8 | Sprint 9 |
|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |

> **Análise:** As sprints 7 e 8 apresentaram atraso de 1 período cada.

---

### 2. Qualidade de Implementação

**Objetivo:** Validar qualidade de implementação  
**Pergunta:** O software está bem implementado?  
**Métrica:** Densidade de commits de correção de erros  
**Cálculo:** (Total de commits para correção) / (Total de commits) x 100%  
**Escala:** Porcentagem  
**Valor esperado:** 40%  
**Forma de análise:** Realização de testes

**Resultado:** 22%

> **Análise:** A densidade de commits de correção está abaixo do esperado (22% < 40%). Isso indica que há espaço para melhorar a qualidade do código antes dos commits.

---

### 3. Obediência às Sprints (Musts)

**Objetivo:** Obediência às sprints  
**Pergunta:** Os sprints estão entregando todos os musts?  
**Métrica:** Densidade de prorrogações de musts  
**Cálculo:** (Quantidade de musts prorrogados) / (Total de Musts da Sprint) x 100%  
**Escala:** Porcentagem  
**Valor esperado:** ≤ 0%  
**Forma de análise:** Realizada em Sprint Reviews e Sprint Meetings

**Resultados:**

| Sprint 5 | Sprint 6 | Sprint 7 | Sprint 8 | Sprint 9 |
|----------|----------|----------|----------|----------|
| 0% | 0% | 16% | - | - |

> **Análise:** A Sprint 7 teve 16% de musts prorrogados, o que indica necessidade de melhor planejamento para sprints futuras.

---

### 4. Usabilidade da Interface

**Objetivo:** Usabilidade da Interface de usuário  
**Pergunta:** A interface é intuitiva e perfeitamente utilizável?  
**Métrica:** Densidade de feedback negativo  
**Cálculo:** (Reports negativos) / (Total de Reports) x 100%  
**Escala:** Porcentagem  
**Valor esperado:** ≤ 2%  
**Forma de análise:** Reuniões de alinhamento de requisitos e avaliação do cliente

**Resultado:** 25%

> **Análise:** A densidade de feedback negativo está muito acima do esperado (25% > 2%). Isso indica problemas significativos de usabilidade que precisam ser corrigidos.

---

### 5. Utilidade do Programa

**Objetivo:** Verificar usabilidade  
**Pergunta:** O programa é útil?  
**Métrica:** Avaliação de utilidade  
**Cálculo:** Média aritmética de avaliações  
**Escala:** -  
**Valor esperado:** ≥ 8  
**Forma de análise:** Demonstração e Feedback do cliente

**Resultado:** 8

> **Análise:** A avaliação de utilidade atingiu a nota mínima esperada (8). Os usuários consideram o programa útil.

---

### 6. Recomendação

**Objetivo:** Verificar possível recomendação  
**Pergunta:** Recomendaria o software?  
**Métrica:** Nível de recomendação binária (recomendo/não-recomendo)  
**Cálculo:** Taxa de recomendações (%)  
**Escala:** Porcentagem  
**Valor esperado:** ≥ 80%  
**Forma de análise:** Feedback do cliente

**Resultado:** 100%

> **Análise:** Todos os usuários entrevistados recomendariam o software, o que é um excelente indicador de satisfação.

---

## Visualização das Métricas

| Métrica | Valor Atual | Meta | Status |
|---------|-------------|------|--------|
| Obediência ao período das sprints | 2 atrasos | 0 | Atenção |
| Densidade de commits de correção | 22% | ≤ 40% | Atenção |
| Densidade de prorrogações de musts (Sprint 7) | 16% | 0% | Melhorar |
| Densidade de feedback negativo | 25% | ≤ 2% | Melhorar |
| Avaliação de utilidade | 8 | ≥ 8 | Ok |
| Taxa de recomendação | 100% | ≥ 80% | Ok |

---

## Ações Recomendadas

Com base nos resultados das métricas, recomenda-se:

| Problema | Ação Sugerida |
|----------|---------------|
| Atraso nas Sprints 7 e 8 | Revisar planejamento e estimativas para sprints futuras |
| Baixa qualidade de código (22%) | Aumentar testes automatizados e revisões de código |
| Musts prorrogados (16%) | Priorizar melhor as funcionalidades Must em cada sprint |
| Feedback negativo alto (25%) | Realizar testes de usabilidade com usuários reais |

---

*Última atualização: 01/07/2026*