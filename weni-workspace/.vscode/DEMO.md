# 🎬 Demo: Como Usar o Workspace Weni no VS Code

## 🎯 Cenário 1: Criar Agente com Snippets (30 segundos)

### Passo a Passo Visual:

```
1. Criar novo arquivo: agent_definition.yaml
   📁 Right-click → New File → "agent_definition.yaml"

2. Abrir arquivo e digitar: weni-agent
   📝 Type: "weni-agent"

3. Pressionar Tab
   ⌨️ Press: Tab

4. Resultado: Template completo aparece!
   ✨ Magic happens:
   
   agent:
     name: "█"  ← Cursor aqui (Tab para navegar)
     version: "1.0.0"
     description: "..."
   
   credentials:
     - name: API_KEY
   ...
```

**🎥 Fluxo:**
```
weni-agent [Tab] → Template completo → [Tab] para preencher campos → ✅ Pronto!
```

---

## 🎯 Cenário 2: Desenvolver Tool com Copilot (2 minutos)

### Passo a Passo Visual:

```
1. Abrir GitHub Copilot Chat
   ⌨️ Ctrl+Shift+I

2. Fazer pergunta ao Copilot:
   💬 "Crie uma tool que busca produtos na VTEX com validação de CEP"

3. Copilot gera código usando CONTEXTO DO PROJETO:
   🤖 Copilot responde:
   
   "Vou criar uma tool SearchProduct seguindo o padrão Obramax.
   Vou usar a Region API para validar o CEP e Intelligent Search
   para buscar produtos com regionId..."
   
   [Mostra código completo com:
    - Classe herdando de Tool
    - Validação de CEP com regex
    - Chamada Region API
    - Chamada Search API
    - Tratamento de erros
    - Logs estruturados
    - Mensagens com emojis]

4. Copiar código gerado
   📋 Click "Copy" ou Ctrl+A → Ctrl+C

5. Criar arquivo tools/searchProduct/main.py
   📁 New File → Cole o código

6. Testar localmente
   ⌨️ Press F5 (ou Run Task → "Weni: Run Verbose")
```

**🎥 Fluxo:**
```
Copilot Chat → Pergunta → Código gerado com padrões → F5 para testar → ✅ Funciona!
```

---

## 🎯 Cenário 3: Deploy com Tasks (1 clique)

### Passo a Passo Visual:

```
1. Abrir Command Palette
   ⌨️ Ctrl+Shift+P

2. Digitar "task"
   🔍 Type: "Run Task"

3. Selecionar task da lista:
   📋 Lista aparece:
   
   ┌─────────────────────────────────────┐
   │ Weni: Login                         │
   │ Weni: List Projects                 │
   │ Weni: Init New Agent                │
   │ Weni: Run (Test Locally)            │
   │ Weni: Run Verbose (With Logs) ⭐    │
   │ Weni: Push to Production            │
   │ Weni: View Production Logs          │
   │ Open: Visão 360° Documentation      │
   │ ...                                 │
   └─────────────────────────────────────┘

4. Clicar em "Weni: Push to Production"
   🚀 Task executa: weni project push
   
   Terminal mostra:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🚀 Pushing to production...
   ✅ Agent deployed successfully!
   📊 Version: 1.0.0
   🔗 URL: https://...
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**🎥 Fluxo:**
```
Ctrl+Shift+P → "Run Task" → Select → ✅ Deploy completo!
```

---

## 🎯 Cenário 4: Usar Snippets de Integração (10 segundos)

### Exemplo: Adicionar busca VTEX em tool existente

```
1. Abrir arquivo: tools/myTool/main.py

2. Dentro do método execute(), digitar: vtex-search
   📝 Type: "vtex-search"

3. Pressionar Tab
   ⌨️ Press: Tab

4. Código completo aparece:
   ✨ Snippet expande para:
   
   # Product search with regionalization
   search_url = f"https://{account_name}.vtexcommercestable.com.br/..."
   search_response = requests.get(
       search_url,
       params={
           "query": █,  ← Cursor aqui
           "regionId": region_id,
           ...
       },
       timeout=10
   )
   
   if search_response.status_code == 200:
       products = search_response.json().get("products", [])
       # ... (código completo de formatação)

5. Tab para preencher variáveis
   ⌨️ Tab → search_term → Tab → region_id → ...

6. Pronto!
   ✅ Código completo com tratamento de erros
```

**🎥 Fluxo:**
```
vtex-search [Tab] → Código API completo → [Tab] nas variáveis → ✅ API pronta!
```

---

## 🎯 Cenário 5: YAML Validation em Tempo Real

### Validação automática ao editar agent_definition.yaml:

```
1. Abrir agent_definition.yaml

2. Começar a digitar "agent:"
   📝 Type: "agent:"

3. Autocomplete aparece automaticamente:
   💡 VS Code mostra:
   
   agent:
     name         ← (hover: "Agent name (no spaces)")
     version      ← (hover: "Semantic version (e.g., 1.0.0)")
     description  ← (hover: "Brief description")

4. Se digitar versão errada:
   ❌ version: "1.0"  ← Linha fica vermelha
   
   Hover mostra erro:
   "String does not match pattern: ^\d+\.\d+\.\d+$"

5. Corrigir para formato válido:
   ✅ version: "1.0.0"  ← Erro some

6. Campos obrigatórios faltando:
   ⚠️ Se faltar "name", VS Code mostra warning
```

**🎥 Fluxo:**
```
Editar YAML → Autocomplete → Validação em tempo real → ✅ Zero erros ao salvar!
```

---

## 🎯 Cenário 6: Testar com F5 (Atalho Rápido)

### Debug/Test com um clique:

```
1. Editar agent_definition.yaml ou tool Python

2. Salvar (Ctrl+S)

3. Pressionar F5
   ⌨️ Press: F5

4. Task "Weni: Run Verbose" executa automaticamente:
   🚀 Terminal abre e mostra:
   
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔧 Running agent locally...
   
   [DEBUG] Loading agent_definition.yaml
   [INFO] Agent: SearchProductAgent v1.0.0
   [INFO] Loading tool: SearchProduct
   [INFO] Starting local server...
   [INFO] Server listening on http://localhost:8000
   
   💬 Send message to test:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. Interagir com agente no console
   💬 Digite mensagem → Agente responde com logs

6. Ver logs em tempo real:
   📊 Todos os prints aparecem:
   
   [INFO] Processing search: "furadeira"
   [INFO] Validating CEP: 01310100
   [INFO] Region ID: v2.2AC...
   [INFO] Searching products...
   [INFO] Found 3 products
   ✅ Response sent
```

**🎥 Fluxo:**
```
Edit code → [F5] → Test locally com logs → Ver mensagens/erros → ✅ Debug fácil!
```

---

## 🎯 Cenário 7: GitHub Copilot com Contexto Completo

### Copilot conhece TODO o projeto:

```
1. Abrir Copilot Chat (Ctrl+Shift+I)

2. Fazer perguntas específicas:
   
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💬 Você: "Como funcionam os 5 agentes Obramax?"
   
   🤖 Copilot: "Os 5 agentes em produção são:
   
   1. Concierge - Busca produtos com regionalização
      - Tool: SearchProduct
      - APIs: Region + Intelligent Search
      - Valida CEP e filtra por estoque regional
   
   2. Product Details (PDP) - Detalhes do produto
      - Tool: ProductDetails
      - API: Catalog
      - Retorna dimensões, peso, specs
   
   ... [continua com detalhes completos]"
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. Pedir código específico:
   
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💬 Você: "Adicione retry logic na chamada VTEX"
   
   🤖 Copilot: "Vou adicionar retry com backoff exponencial:
   
   from time import sleep
   
   max_retries = 3
   for attempt in range(max_retries):
       try:
           response = requests.get(url, timeout=10)
           if response.status_code == 200:
               break
       except requests.exceptions.Timeout:
           if attempt < max_retries - 1:
               sleep(2 ** attempt)  # 1s, 2s, 4s
               continue
           raise
   
   ... [código completo com logging]"
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. Troubleshooting:
   
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💬 Você: "Erro: Tool not found"
   
   🤖 Copilot: "Este erro ocorre quando:
   
   1. O path no agent_definition.yaml está incorreto
      ✅ Verifique: tools: name: ToolName, path: tools/toolName
   
   2. A classe Python não corresponde ao nome
      ✅ Verifique: class ToolName(Tool) no main.py
   
   3. O arquivo main.py não existe
      ✅ Verifique: tools/toolName/main.py existe
   
   Exemplo correto:
   ... [mostra estrutura completa]"
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**🎥 Por que funciona?**
```
Copilot lê → .github/copilot-instructions.md → Contexto completo
            ↓
Conhece: Templates, APIs, Padrões, Agentes, Erros comuns, Soluções
            ↓
Respostas precisas baseadas no PROJETO REAL (não genéricas!)
```

---

## 📊 Comparação: Antes vs Depois

### ANTES (Sem Setup):
```
❌ Buscar templates manualmente em docs/
❌ Copiar/colar código de exemplos
❌ Digitar comandos CLI completos no terminal
❌ Não ter validação de YAML
❌ Copilot dar respostas genéricas (não Weni-specific)
❌ Não saber quais extensões instalar
❌ Configurar settings manualmente
```

### DEPOIS (Com Setup):
```
✅ Snippets prontos: weni-agent [Tab] → Código completo
✅ Tasks com 1 clique: F5 → Testa agente
✅ YAML validado em tempo real
✅ Copilot com contexto do projeto (respostas específicas)
✅ Extensões recomendadas automaticamente
✅ Settings otimizadas (format on save, etc)
✅ Documentação acessível via tasks
```

**Ganho:** De 30 min para criar um agente → **2 minutos!** ⚡

---

## 🎯 Fluxo Completo: Criar Agente do Zero

### Timeline: ~5 minutos (em vez de 30+)

```
┌─────────────────────────────────────────────────────────────────┐
│ TEMPO    │ AÇÃO                          │ FERRAMENTA USADA    │
├──────────┼───────────────────────────────┼─────────────────────┤
│ 0:00     │ Criar novo folder "MyAgent"   │ VS Code Explorer    │
│ 0:10     │ Criar agent_definition.yaml   │ Snippet: weni-agent │
│ 0:30     │ Preencher campos (Tab)        │ Snippet navigation  │
│ 1:00     │ Criar tools/myTool/main.py    │ Snippet: weni-tool  │
│ 1:30     │ Adicionar lógica específica   │ Copilot Chat        │
│ 2:00     │ Adicionar API call            │ Snippet: vtex-*     │
│ 2:30     │ Validar YAML                  │ YAML schema (auto)  │
│ 3:00     │ Testar localmente             │ F5                  │
│ 4:00     │ Debug e ajustar               │ Logs + Copilot      │
│ 4:30     │ Deploy para produção          │ Task: Push          │
│ 5:00     │ ✅ PRONTO EM PRODUÇÃO!        │                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Próximos Passos

1. ✅ **Leia:** [.vscode/README.md](.vscode/README.md) - Guia completo do setup
2. ✅ **Instale:** Extensões recomendadas (notificação ao abrir workspace)
3. ✅ **Teste:** Crie arquivo `.yaml` → Digite `weni-agent` → Tab
4. ✅ **Explore:** Ctrl+Shift+I → Pergunte ao Copilot sobre o projeto
5. ✅ **Pratique:** Crie seu primeiro agente seguindo o roadmap

---

## 💡 Dicas de Produtividade

### Atalhos Essenciais:
- `weni-agent` → Template YAML completo
- `weni-tool` → Classe Python completa
- `vtex-search` → Busca VTEX pronta
- `weni-try` → Try-except com todos os erros
- `F5` → Test local com logs
- `Ctrl+Shift+I` → Copilot Chat (contexto do projeto)
- `Ctrl+Shift+P` → Command Palette (tasks)

### Workflow Recomendado:
1. **Planejar** → Pergunte ao Copilot sobre arquitetura
2. **Criar** → Use snippets para estrutura
3. **Desenvolver** → Copilot para lógica específica
4. **Testar** → F5 para rodar localmente
5. **Debugar** → Logs + Copilot para troubleshooting
6. **Deploy** → Task "Push to Production"

---

**Agora você tem um ambiente de desenvolvimento COMPLETO e OTIMIZADO! 🚀**
