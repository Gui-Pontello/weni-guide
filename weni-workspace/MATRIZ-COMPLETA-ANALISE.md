# 📊 Análise Completa: Matriz de Funcionalidade Weni - Obramax

## 📁 Sobre este Documento

Este documento consolida **todas as informações** do arquivo Excel completo:  
**"Weni _ Matriz de Funcionalidade _ Transbordo _ Instruções.xlsx"**

O arquivo contém **13 abas** com informaçõesestratégicas do projeto Weni/Obramax.

---

## 📚 Estrutura do Excel (13 Abas)

### 1. 👥 **Usuários e Perfis**
**Conteúdo:** Gestão de usuários da plataforma Weni  
**Campos:**
- E-mail do usuário
- Perfil (Admin, Remover, Service, etc.)
- Permissões:
  - Trocar mensagens com cliente
  - Criar fluxos de automação
  - Disparar fluxos
  - Mensagens de marketing
  - Ver relatórios
  - Editar agentes
  - Adicionar aplicativos
  - Configurações
- Roles Omni (["admin"], ["service"], etc.)

**Uso:** Controle de acesso e permissões na plataforma Weni.

---

### 2. 🔐 **Permissões**
**Conteúdo:** Matriz detalhada de permissões por perfil/usuário  
**Uso:** Definir níveis de acesso granulares.

---

### 3. 📝 **Novas Instruções Pós**
**Conteúdo:** Instruções atualizadas para agentes de **Pós-vendas**  
**Uso:** Atualizar o campo `instructions` no agent_definition.yaml dos agentes de pós-vendas.

---

### 4. 📝 **Novas Instruções TLV**
**Conteúdo:** Instruções atualizadas para agentes de **Televendas (TLV)**  
**Uso:** Atualizar o campo `instructions` no agent_definition.yaml dos agentes de televendas.

---

### 5. 💬 **Mensagens Omni**
**Conteúdo:** 11+ templates de mensagens para **transbordo (handoff) para humanos**  
**Templates incluem:**
1. Transbordo próximo dia útil
2. Início de atendimento
3. Reagendamento
4. Cupom fiscal (nota fiscal)
5. Solicitação de imagens
6. Contato sem sucesso
7. Crédito
8. Estorno/Devolução
9. Finalização de atendimento
10. Comprovante de pagamento
11. Mensagem geral

**Variáveis:** `{{nome}}`, `{{data}}`, `{{protocolo}}`, `{{atendente}}`, etc.

**Uso:** Mensagens padronizadas enviadas via Weni Flows durante transbordo para Omni.

---

### 6. 🔍 **Pesquisa Solucx**
**Conteúdo:** Integrações ou dados relacionados ao sistema **Solucx**  
**Uso:** Referência para integrações com sistemas externos de pesquisa/CRM.

---

### 7. 📄 **Instruções Atuais**
**Conteúdo:** Instruções em produção atualmente (baseline)  
**Uso:** Comparar com "Novas Instruções" para gerenciar mudanças.

---

### 8. 📦 **REQ Pós-vendas**
**Conteúdo:** Requisitos funcionais e técnicos para agentes de **Pós-vendas**  
**Inclui:**
- Casos de uso
- Fluxos de conversa
- Integrações necessárias (VTEX, Omni, etc.)
- Regras de negócio
- Critérios de transbordo

**Uso:** Documento de requisitos para desenvolver/manter agentes de pós-vendas.

---

### 9. 📞 **REQ Televendas**
**Conteúdo:** Requisitos funcionais e técnicos para agentes de **Televendas**  
**Inclui:**
- Casos de uso
- Fluxos de conversa
- Integrações necessárias
- Regras de negócio
- Critérios de transbordo

**Uso:** Documento de requisitos para desenvolver/manter agentes de televendas.

---

### 10. 🎓 **REQ CRM Academia Crédito**
**Conteúdo:** Requisitos para agentes de **CRM, Academia e Crédito**  
**Inclui:**
- Gestão de relacionamento com cliente
- Programas de fidelidade/academia
- Solicitações de crédito
- Fluxos específicos

**Uso:** Requisitos para agentes especializados em CRM e crédito.

---

### 11. 🔧 **REQ Técnico**
**Conteúdo:** Requisitos técnicos gerais do projeto  
**Inclui:**
- Arquitetura de sistema
- APIs e integrações
- Performance e SLA
- Segurança e compliance
- Logging e monitoramento

**Uso:** Guia técnico para implementação e manutenção.

---

### 12. 📢 **Campanhas**
**Conteúdo:** Campanhas de marketing/comunicação via WhatsApp  
**Inclui:**
- Mensagens de campanha
- Segmentação de público
- Gatilhos e agendamento
- Templates de mensagem

**Uso:** Configurar envios massivos via Weni Flows.

---

### 13. 📨 **Transacional**
**Conteúdo:** Mensagens transacionais automáticas  
**Exemplos:**
- Confirmação de pedido
- Atualização de entrega
- Cobrança/pagamento
- Notas fiscais

**Uso:** Mensagens automáticas disparadas por eventos do sistema.

---

## 🎯 Como Usar Este Documento

### Para Desenvolvedores:
1. **Instruções dos Agentes:** Use abas "Novas Instruções Pós/TLV" para atualizar `agent_definition.yaml`
2. **Mensagens Omni:** Use aba "Mensagens Omni" para templates de transbordo
3. **Requisitos:** Consulte abas "REQ *" para entender regras de negócio

### Para Gestores de Projeto:
1. **Usuários e Permissões:** Use abas "Usuários e Perfis" e "Permissões" para controlar acesso
2. **Campanhas:** Use aba "Campanhas" para planejar envios
3. **Requisitos:** Use abas "REQ *" para validar escopo

### Para QA/Testes:
1. **Instruções:** Compare "Instruções Atuais" vs "Novas Instruções" para testar mudanças
2. **Mensagens:** Valide todos os templates em "Mensagens Omni"
3. **Requisitos:** Use abas "REQ *" para casos de teste

---

## 📊 Resumo Estatístico

| Aba | Tipo | Conteúdo Principal |
|-----|------|-------------------|
| Usuários e Perfis | Gestão | Controle de acesso |
| Permissões | Gestão | Matriz de permissões |
| Novas Instruções Pós | Config | Instructions YAML |
| Novas Instruções TLV | Config | Instructions YAML |
| **Mensagens Omni** | Templates | **11+ mensagens padronizadas** |
| Pesquisa Solucx | Integração | Sistema externo |
| Instruções Atuais | Baseline | Versão em produção |
| REQ Pós-vendas | Requisitos | Specs funcionais |
| REQ Televendas | Requisitos | Specs funcionais |
| REQ CRM Academia Crédito | Requisitos | Specs funcionais |
| REQ Técnico | Requisitos | Specs técnicos |
| Campanhas | Marketing | Envios massivos |
| Transacional | Automação | Mensagens por evento |

---

## 🔄 Integração com Documentação Existente

Este Excel complementa a documentação em `/docs`:

| Excel | Documentação |
|-------|-------------|
| Mensagens Omni | `docs/08-visao-360` (seção Omni) |
| REQ Técnico | `docs/01-estrutura-projetos.md` |
| REQ Pós/TLV/CRM | `docs/02-padroes-boas-praticas.md` |
| Instruções | `agent_definition.yaml` (campo instructions) |
| Campanhas/Transacional | `docs/03-apis-integracoes.md` (Weni Flows) |

---

## 💡 Recomendações

### 1. Versionamento das Instruções
- Sempre compare "Instruções Atuais" vs "Novas Instruções" antes de deploy
- Mantenha histórico de mudanças

### 2. Templates Omni
- Use variáveis `{{}}` para personalização
- Teste todos os templates no Weni Flows antes de produção

### 3. Requisitos
- Mantenha abas "REQ *" atualizadas conforme evoluções do projeto
- Use como fonte única de verdade para regras de negócio

### 4. Permissões
- Revise "Usuários e Perfis" periodicamente
- Remova acessos de usuários inativos

### 5. Campanhas
- Segmente público adequadamente
- Respeite janelas de envio (horário comercial)
- Monitore taxa de resposta

---

## 🔗 Referências Relacionadas

- **Documento Master:** [docs/08-visao-360-projeto-weni-obramax.md](docs/08-visao-360-projeto-weni-obramax.md)
- **Guia Rápido:** [INDICE-RAPIDO.md](INDICE-RAPIDO.md)
- **Quick Reference:** [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
- **Diagramas:** [DIAGRAMA-FLUXO-COMPLETO.md](DIAGRAMA-FLUXO-COMPLETO.md)

---

## 📅 Histórico

- **12/02/2026:** Análise completa das 13 abas do Excel
- Consolidação em workspace único
- Integração com documentação existente

---

**📁 Arquivo Excel:** `Weni _ Matriz de Funcionalidade _ Transbordo _ Instruções.xlsx`  
**📊 Total de Abas:** 13  
**🎯 Objetivo:** Centralizar toda configuração e requisitos do projeto Weni/Obramax
