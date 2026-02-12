# 🚀 Setup do Workspace VS Code - Weni Platform

Este workspace está **pré-configurado** para desenvolvimento de agentes Weni com **integração automática** de toda a documentação!

## ✨ O que foi configurado?

### 1. 🤖 GitHub Copilot Intelligence
**Arquivo:** `.github/copilot-instructions.md`

O GitHub Copilot **lê automaticamente** este arquivo e usa como contexto! Quando você pedir ajuda ao Copilot, ele já conhece:
- ✅ Estrutura de agentes Weni
- ✅ Templates YAML e Python
- ✅ VTEX APIs (6 principais)
- ✅ Weni Flows integration
- ✅ Padrões de código Obramax
- ✅ Tratamento de erros
- ✅ Validação de inputs
- ✅ Logging estruturado

**Como usar:**
1. Abra o Copilot Chat (`Ctrl+Shift+I`)
2. Digite: "crie um agente que busca produtos na VTEX"
3. O Copilot vai gerar código **seguindo os padrões deste projeto**!

---

### 2. ⚡ Snippets de Código
**Arquivo:** `.vscode/weni-agent.code-snippets`

**11 snippets prontos** para acelerar desenvolvimento:

| Snippet | Atalho | Descrição |
|---------|--------|-----------|
| Agent YAML completo | `weni-agent` | Template agent_definition.yaml |
| Tool Python class | `weni-tool` | Classe Tool completa com error handling |
| VTEX Region API | `vtex-region` | Validação de CEP |
| VTEX Search | `vtex-search` | Busca de produtos |
| VTEX Simulation | `vtex-simulation` | Simulação de frete |
| Weni Flows Trigger | `weni-flow` | Disparo de fluxo |
| Try-Except completo | `weni-try` | Tratamento de erros |
| Validação de inputs | `weni-validate` | Validação de parâmetros |
| Formatação de CEP | `format-cep` | Limpar e validar CEP |
| Logging estruturado | `weni-log` | Print com níveis (INFO/WARN/ERROR) |

**Como usar:**
1. Crie um arquivo `.yaml` ou `.py`
2. Digite o atalho (ex: `weni-agent`)
3. Pressione `Tab` e navegue pelos campos com `Tab/Shift+Tab`

---

### 3. 🎯 Tasks (Comandos com 1 Clique)
**Arquivo:** `.vscode/tasks.json`

**13 tasks configuradas** acessíveis via `Ctrl+Shift+P` → "Run Task":

#### Weni CLI
- `Weni: Login` - Autenticar
- `Weni: List Projects` - Listar projetos
- `Weni: Init New Agent` - Criar novo agente
- `Weni: Run (Test Locally)` - Testar localmente
- `Weni: Run Verbose (With Logs)` - Testar com logs detalhados ⭐ **[F5]**
- `Weni: Push to Production` - Deploy
- `Weni: View Production Logs` - Ver logs de produção
- `Weni: View Logs (Follow)` - Logs em tempo real

#### Documentação
- `Open: Visão 360° Documentation` - Abre doc master
- `Open: Quick Reference` - Abre quick reference
- `Open: Visual Flow Diagrams` - Abre diagramas

#### Python
- `Python: Install Weni CLI`
- `Python: Upgrade Weni CLI`

**Como usar:**
- `Ctrl+Shift+P` → Digite "Run Task"
- Ou: `Ctrl+Shift+B` (build) ou `Ctrl+Shift+T` (test)
- Ou: **F5** para "Run Verbose" (default test task)

---

### 4. 📦 Extensões Recomendadas
**Arquivo:** `.vscode/extensions.json`

Quando abrir o workspace pela primeira vez, VS Code vai sugerir instalar:

- ✅ **Python** + **Pylance** (Análise de código Python)
- ✅ **YAML** (Validação de agent_definition.yaml)
- ✅ **GitHub Copilot** + **Copilot Chat** (IA com contexto do projeto!)
- ✅ **Markdown All in One** (Preview de documentação)
- ✅ **Markdown Mermaid** (Diagramas)
- ✅ **PowerShell** (Terminal)

**Como usar:**
1. Ao abrir o workspace, clique em "Install" na notificação
2. Ou: `Ctrl+Shift+X` → Aba "Recommended"

---

### 5. ⚙️ Settings Otimizadas
**Arquivo:** `.vscode/settings.json`

Configurações automáticas:
- ✅ Python: Pylance como language server
- ✅ YAML: Validação com schema para agent_definition.yaml
- ✅ Editor: Format on save, rulers em 80/120
- ✅ Terminal: PowerShell como padrão
- ✅ Markdown: Preview configurado
- ✅ GitHub Copilot: Habilitado para todos os tipos de arquivo
- ✅ Search: Inclui documentação (exclui __pycache__, node_modules)

**Nada precisa ser configurado manualmente!**

---

### 6. 📋 YAML Schema Validation
**Arquivo:** `.vscode/weni-agent-schema.json`

Validação automática de `agent_definition.yaml`:
- ✅ Autocomplete de campos (name, version, description, tools...)
- ✅ Validação de tipos (version precisa ser x.y.z)
- ✅ Erros inline se faltar campo obrigatório
- ✅ Descrições de cada campo no hover

**Como usar:**
1. Crie ou abra um arquivo `agent_definition.yaml`
2. VS Code automaticamente valida
3. Hover sobre campos para ver descrições
4. `Ctrl+Space` para autocomplete

---

## 🎯 Quick Start (Passo a Passo)

### 1. Configuração Inicial (Uma vez apenas)

```bash
# 1. Instalar Python 3.8+
python --version

# 2. Instalar Weni CLI
pip install weni-cli

# 3. Autenticar (Task ou comando)
weni login
# Ou: Ctrl+Shift+P → "Run Task" → "Weni: Login"
```

### 2. Criar Seu Primeiro Agente

```bash
# Opção A: Via Task (recomendado)
# Ctrl+Shift+P → "Run Task" → "Weni: Init New Agent"

# Opção B: Via terminal
weni init
```

### 3. Usar Snippets para Código

#### Criar agent_definition.yaml:
1. Crie arquivo `agent_definition.yaml`
2. Digite `weni-agent` + `Tab`
3. Preencha os campos (navega com Tab)

#### Criar Tool Python:
1. Crie `tools/myTool/main.py`
2. Digite `weni-tool` + `Tab`
3. Preencha a lógica da ferramenta

### 4. Testar Localmente

```bash
# Opção A: Pressione F5 (test task padrão)

# Opção B: Via Task
# Ctrl+Shift+P → "Run Task" → "Weni: Run Verbose (With Logs)"

# Opção C: Via terminal
weni run --verbose
```

### 5. Deploy para Produção

```bash
# Opção A: Via Task
# Ctrl+Shift+P → "Run Task" → "Weni: Push to Production"

# Opção B: Via terminal
weni project push
```

---

## 🤖 Como Usar o GitHub Copilot com Este Setup

### Exemplos de Prompts que Funcionam MUITO Bem:

1. **"Crie um agente que busca produtos na VTEX com regionalização"**
   - Copilot vai gerar YAML + Python seguindo os padrões Obramax

2. **"Adicione validação de CEP na tool SearchProduct"**
   - Copilot conhece o snippet `format-cep` e padrões de validação

3. **"Crie uma tool que dispara Weni Flow com dados do pedido"**
   - Copilot usa o template `weni-flow` automaticamente

4. **"Adicione tratamento de erro para timeout na API VTEX"**
   - Copilot conhece o padrão `weni-try` com Timeout handling

5. **"Como fazer simulação de frete para múltiplos SKUs?"**
   - Copilot referencia o snippet `vtex-simulation` e docs

### Copilot Chat (Ctrl+Shift+I):
- ✅ Pergunte sobre arquitetura → Copilot conhece os 5 agentes Obramax
- ✅ Peça exemplos → Copilot referencia código real em `Obramax/[Atual]...`
- ✅ Troubleshooting → Copilot conhece erros comuns e soluções

---

## 📚 Documentação Disponível

Todo o conhecimento está estruturado em:

### Documentos Master (Consulta Rápida)
1. **[docs/08-visao-360-projeto-weni-obramax.md](../docs/08-visao-360-projeto-weni-obramax.md)** 🔥
   - Documento COMPLETO com tudo
   - Arquitetura, agentes, APIs, flows, troubleshooting

2. **[INDICE-RAPIDO.md](../INDICE-RAPIDO.md)**
   - Navegação por objetivo (iniciante/desenvolvedor/especialista)

3. **[QUICK-REFERENCE.md](../QUICK-REFERENCE.md)**
   - Comandos CLI, snippets, endpoints

4. **[DIAGRAMA-FLUXO-COMPLETO.md](../DIAGRAMA-FLUXO-COMPLETO.md)**
   - Fluxos visuais end-to-end

### Outros Documentos (20 arquivos em docs/)
- 00-guia-inicio-rapido.md
- 01-estrutura-projetos.md
- 02-padroes-boas-praticas.md
- 03-apis-integracoes.md
- 04-weni-cli-guia-completo.md
- E mais 15 documentos!

---

## 🎓 Roadmap de Aprendizado

### Semana 1-2: Fundamentos
- [ ] Ler [INDICE-RAPIDO.md](../INDICE-RAPIDO.md)
- [ ] Fazer `weni init` e criar primeiro agente
- [ ] Testar snippet `weni-agent` e `weni-tool`
- [ ] Rodar localmente com `weni run --verbose`
- [ ] Explorar GitHub Copilot com prompts simples

### Semana 3-4: Integrações
- [ ] Ler [docs/03-apis-integracoes.md](../docs/03-apis-integracoes.md)
- [ ] Estudar VTEX APIs (Region, Search, Simulation)
- [ ] Testar snippets VTEX (`vtex-region`, `vtex-search`)
- [ ] Criar tool que integra com API externa
- [ ] Implementar tratamento de erros (`weni-try`)

### Mês 2: Produção
- [ ] Analisar código real em `Obramax/[Atual]...`
- [ ] Estudar [docs/08-visao-360](../docs/08-visao-360-projeto-weni-obramax.md)
- [ ] Implementar Weni Flows trigger (`weni-flow`)
- [ ] Adicionar logs estruturados (`weni-log`)
- [ ] Deploy para produção (`weni project push`)

### Mês 3+: Expert
- [ ] Otimizar performance (cache, retry, parallel)
- [ ] Implementar KPIs e analytics
- [ ] Criar guardrails customizados
- [ ] Contribuir para documentação

---

## 🆘 Troubleshooting

### "Snippets não aparecem"
✅ **Solução:** Verifique se instalou Python/YAML extensions (`Ctrl+Shift+X`)

### "Tasks não aparecem"
✅ **Solução:** `Ctrl+Shift+P` → "Tasks: Run Task" → Selecione na lista

### "GitHub Copilot não usa o contexto"
✅ **Solução:** 
1. Verifique se instalou GitHub Copilot extension
2. Confira se o arquivo `.github/copilot-instructions.md` existe
3. Reabra o workspace (`File` → `Close Workspace` → Reabrir)

### "YAML não valida"
✅ **Solução:**
1. Arquivo precisa se chamar exatamente `agent_definition.yaml`
2. Install YAML extension (RedHat)

### "Weni CLI não encontrado"
✅ **Solução:**
```bash
pip install weni-cli
# Ou use a task: Ctrl+Shift+P → "Python: Install Weni CLI"
```

---

## 🎯 Atalhos de Teclado Essenciais

| Atalho | Ação |
|--------|------|
| `Ctrl+Shift+P` | Command Palette (Run Tasks, etc) |
| `Ctrl+Shift+I` | GitHub Copilot Chat |
| `Ctrl+Space` | Autocomplete / Intellisense |
| `F5` | Run default test task (weni run --verbose) |
| `Ctrl+Shift+B` | Run build task |
| `Ctrl+Shift+T` | Reopen closed terminal |
| `Ctrl+Shift+X` | Extensions panel |
| `Ctrl+K Ctrl+O` | Open folder/workspace |
| `Tab` | Navigate snippet placeholders |
| `Ctrl+/` | Toggle comment |

---

## 📦 Estrutura de Arquivos do Setup

```
.vscode/
├── settings.json               # Configurações do workspace
├── tasks.json                  # 13 tasks para Weni CLI
├── extensions.json             # Extensões recomendadas
├── weni-agent.code-snippets    # 11 snippets prontos
└── weni-agent-schema.json      # Validação YAML

.github/
└── copilot-instructions.md     # Contexto para GitHub Copilot (🔥 IMPORTANTE!)
```

---

## 🚀 Próximos Passos

1. ✅ **Instale as extensões recomendadas** (notificação ao abrir workspace)
2. ✅ **Faça `weni login`** (Task ou comando)
3. ✅ **Teste um snippet** (crie `test.yaml` → `weni-agent` + Tab)
4. ✅ **Pergunte ao Copilot** (`Ctrl+Shift+I` → "Como criar um agente Weni?")
5. ✅ **Leia a Visão 360°** ([docs/08-visao-360](../docs/08-visao-360-projeto-weni-obramax.md))

---

## 💡 Dica Final

Este setup transforma o VS Code em uma **IDE especializada** para Weni Platform. Com GitHub Copilot ativado, você tem um **assistente IA que conhece TODO o projeto** - arquitetura, APIs, padrões de código, troubleshooting, etc.

**Basta perguntar!** 🤖💬

---

## 📞 Recursos

- **Documentação Local:** [docs/](../docs/)
- **Código Produção:** [Obramax/](../Obramax/)
- **Weni CLI Docs:** https://weni-ai.github.io/weni-cli/
- **VTEX Docs:** https://developers.vtex.com/

---

**Criado em:** 12/02/2026  
**Versão do Setup:** 1.0.0
