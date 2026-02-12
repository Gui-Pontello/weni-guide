# Documentação - Desenvolvimento de Agentes de IA na Plataforma Weni

Este repositório contém toda a documentação necessária para desenvolver agentes de IA via CLI na plataforma Weni.

## � Início Rápido

**Novo desenvolvedor?** Comece aqui: [Guia de Início Rápido](00-guia-inicio-rapido.md)

Crie seu primeiro agente de IA em menos de 30 minutos!

## 📚 Índice de Documentação

### 🎯 Documento Master (NOVO)
- **[📘 Visão 360° - Projeto Weni & Obramax](08-visao-360-projeto-weni-obramax.md)** 🆕🔥
  - **Documentação COMPLETA e consolidada do projeto**
  - Arquitetura end-to-end com diagramas
  - 5 agentes em produção detalhados (Concierge, PDP, Checkout, Order, Orçamax)
  - 11 templates de mensagens Omni para transbordo
  - Integrações críticas VTEX + Weni Flows
  - Guia de especialização (iniciante → expert)
  - KPIs, métricas, troubleshooting
  - **Use este documento para consulta como especialista!**

### 1. Guias Essenciais
- **[🚀 Guia de Início Rápido](00-guia-inicio-rapido.md)** - Seu primeiro agente em 30 minutos
- [Estrutura de Projetos](01-estrutura-projetos.md) - Como organizar seus agentes de IA
- [Padrões e Boas Práticas](02-padroes-boas-praticas.md) - Convenções e recomendações
- [Guia de APIs e Integrações](03-apis-integracoes.md) - Como integrar com VTEX e outras APIs
- **[⚡ Weni CLI - Guia Completo](04-weni-cli-guia-completo.md)** - Instalação, comandos e deploy via CLI
- **[🔄 Guia de Migração](05-guia-migracao.md)** - Migre projetos existentes para a nova estrutura CLI
- **[📦 Weni CLI - Código Oficial](06-weni-cli-codigo-oficial.md)** - Análise completa do repositório oficial (v3.5.2)
- **[📊 Avaliação: O Que Temos e Falta](07-avaliacao-gaps-documentacao.md)** - Gaps críticos e roadmap

### 2. Exemplos Práticos
- [Agente de Busca de Produtos com Regionalização](exemplos/concierge-regionalizacao.md) - Exemplo completo e documentado
- [Projeto Completo com YAML e CLI](exemplos/projeto-completo-yaml.md) - E-commerce agent com deploy via CLI

### 3. Referências
- [API Reference](reference/api-reference.md) - Consulta rápida de APIs e padrões
- [Troubleshooting](reference/troubleshooting.md) - Solução de problemas comuns
- [Glossário](reference/glossario.md) - Terminologia e conceitos

## 🎯 Objetivo

Esta documentação foi criada a partir de:
- ✅ Análise de código de agentes em produção (Obramax)
- ✅ Transcrições de treinamentos técnicos da Weni
- ✅ Melhores práticas identificadas pela equipe de desenvolvimento
- ✅ Padrões de integração VTEX comprovados

## 📖 Como Usar Esta Documentação

### Para Iniciantes
1. 🚀 Comece com o [Guia de Início Rápido](00-guia-inicio-rapido.md)
2. 📁 Leia [Estrutura de Projetos](01-estrutura-projetos.md) para organização
3. 🎓 Estude um [Exemplo Prático](exemplos/concierge-regionalizacao.md) completo

### Para Desenvolvedores
1. ✨ Consulte [Padrões e Boas Práticas](02-padroes-boas-praticas.md) antes de codificar
2. 🔌 Use [APIs e Integrações](03-apis-integracoes.md) como referência
3. ⚡ Mantenha [API Reference](reference/api-reference.md) aberta para consultas rápidas

### Para Troubleshooting
1. 🔍 Consulte [Troubleshooting](reference/troubleshooting.md) para problemas comuns
2. 📖 Use o [Glossário](reference/glossario.md) para esclarecer termos
3. 💡 Revise os exemplos práticos para casos de uso similares

## 🛠️ Stack Tecnológica

- **Linguagem:** Python 3.8+
- **Framework:** Biblioteca Weni (`weni>=1.0.0`)
- **Integrações:** VTEX APIs, Weni Flows
- **Dependências:** requests, json, urllib

## 📊 Estrutura do Repositório

```
docs/
├── README.md                          # Este arquivo
├── 00-guia-inicio-rapido.md          # Quick start
├── 01-estrutura-projetos.md          # Organização de código
├── 02-padroes-boas-praticas.md       # Convenções
├── 03-apis-integracoes.md            # Integrações externas
├── 04-weni-cli-guia-completo.md      # Weni CLI documentação
├── 05-guia-migracao.md               # Guia de migração
├── 06-weni-cli-codigo-oficial.md     # Análise do código oficial
├── 07-avaliacao-gaps-documentacao.md # 🆕 O que temos e falta
├── JIRA-TASKS.md                     # 📋 Subtasks & Diagramas
├── MIRO-FLUXO-SUBTASKS.md            # 🎨 Guia para Miro
├── miro-import.csv                   # 📊 CSV para import no Miro
├── exemplos/                         # Casos de uso reais
│   ├── concierge-regionalizacao.md
│   └── projeto-completo-yaml.md
├── reference/                        # Referências rápidas
│   ├── api-reference.md
│   ├── troubleshooting.md
│   └── glossario.md
└── SUMARIO.md                        # Resumo geral
```

## 🎓 Conceitos-Chave

### Tool
Componente Python que executa lógica específica (busca, validação, integração).

### Context
Objeto com parâmetros, secrets e informações do usuário.

### TextResponse
Formato padrão de retorno de dados estruturados.

### Regionalização
Filtragem de produtos por CEP e disponibilidade regional.

## 💡 Melhores Práticas em Destaque

✅ **Sempre validar** parâmetros obrigatórios  
✅ **Tratar erros** em requisições HTTP  
✅ **Usar logging** estratégico (DEBUG, INFO, WARN, ERROR)  
✅ **Controlar payload** (máximo 20KB)  
✅ **Credenciais via secrets**, nunca hardcoded  
✅ **Mensagens user-friendly** em erros  

## 🔗 Recursos Externos

- [VTEX Developer Portal](https://developers.vtex.com/) - Documentação oficial VTEX
- [Weni Platform](https://weni.ai/) - Plataforma Weni
- Repositório Obramax - Exemplos de código real

## 📝 Contribuindo

Esta documentação está em constante evolução. Para contribuir:

1. Identifique gaps ou melhorias
2. Documente novos padrões descobertos
3. Adicione exemplos práticos
4. Atualize troubleshooting com novos casos

## 🏆 Casos de Sucesso

Os padrões documentados aqui são usados em produção nos seguintes agentes:

- **Concierge com Regionalização** - Busca de produtos com filtros regionais
- **Product Details Agent** - Detalhes de produtos e SKUs
- **Order Status Agent** - Consulta de pedidos VTEX
- **Orçamax** - Geração de orçamentos personalizados

## 📞 Suporte

Para dúvidas técnicas:
1. Consulte a documentação relevante
2. Revise exemplos práticos similares
3. Verifique troubleshooting para problemas conhecidos
4. Consulte a equipe técnica da Weni

---

**Última atualização:** Fevereiro 2026  
**Versão:** 1.0.0  
**Mantido por:** Equipe de Desenvolvimento Weni

---

## 🚀 Quick Links

| Preciso... | Vá para... |
|-----------|-----------|
| Começar do zero | [Guia de Início Rápido](00-guia-inicio-rapido.md) |
| Saber o que falta | [Avaliação de Gaps](07-avaliacao-gaps-documentacao.md) 🆕 |
| Ver como foi construído | [JIRA Tasks & Diagramas](JIRA-TASKS.md) 📋 |
| Criar fluxo no Miro | [Guia Miro + CSV](MIRO-FLUXO-SUBTASKS.md) 🎨 |
| Organizar meu código | [Estrutura de Projetos](01-estrutura-projetos.md) |
| Usar Weni CLI | [Weni CLI - Guia Completo](04-weni-cli-guia-completo.md) |
| Ver código oficial CLI | [Weni CLI - Código Oficial](06-weni-cli-codigo-oficial.md) |
| Migrar projeto existente | [Guia de Migração](05-guia-migracao.md) |
| Consultar APIs rapidamente | [API Reference](reference/api-reference.md) |
| Resolver um erro | [Troubleshooting](reference/troubleshooting.md) |
| Ver exemplo completo | [Projeto E-commerce YAML](exemplos/projeto-completo-yaml.md) |
| Entender um termo | [Glossário](reference/glossario.md) |

---

**💻 Happy Coding!** 🚀

## 📝 Contribuindo

Esta documentação está em constante evolução. Contribuições são bem-vindas!

---
**Última atualização:** Fevereiro 2026
