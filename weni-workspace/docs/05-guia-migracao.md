# Guia de Migração - Para Projetos Existentes

## 🎯 Objetivo

Este guia ajuda desenvolvedores que já têm agentes desenvolvidos a migrar para a estrutura com Weni CLI e YAML.

## 📋 Antes de Começar

### Checklist Pré-Migração

- [ ] Fazer backup completo do projeto
- [ ] Documentar tools existentes
- [ ] Listar todas as credenciais usadas
- [ ] Identificar parâmetros de cada tool
- [ ] Instalar Weni CLI (`pip install weni-cli`)
- [ ] Fazer login (`weni login`)

---

## 🔄 Processo de Migração

### Passo 1: Analisar Estrutura Atual

#### Estrutura Antiga (Exemplo)

```
meu-projeto/
├── tool1.py
├── tool2.py
├── tool3.py
└── README.md
```

#### Estrutura Nova (Desejada)

```
meu-projeto/
├── agent_definition.yaml    # NOVO
└── tools/                   # NOVO
    ├── tool1/
    │   ├── main.py
    │   └── test_definition.yaml
    ├── tool2/
    │   ├── main.py
    │   └── test_definition.yaml
    └── tool3/
        ├── main.py
        └── test_definition.yaml
```

---

### Passo 2: Atualizar Código das Tools

#### Antes (Código Antigo)

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse

class MinhaTool(Tool):
    def run(self, context: Context):  # ❌ Método antigo
        # Extração antiga
        param = context.params.get("param")      # ❌ params
        secret = context.secrets.get("SECRET")   # ❌ secrets
        
        # Lógica
        result = self.processar(param, secret)
        
        return TextResponse(data=result)
```

#### Depois (Código Atualizado)

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse

class MinhaTool(Tool):
    def execute(self, context: Context) -> TextResponse:  # ✅ Método novo
        # Extração atualizada
        param = context.parameters.get("param")        # ✅ parameters
        secret = context.credentials.get("secret")     # ✅ credentials
        max_items = context.constants.get("max_items", 10)  # ✅ constants
        
        # Lógica (mantém igual)
        result = self.processar(param, secret, max_items)
        
        return TextResponse(data=result)
```

#### Resumo das Mudanças

| Antes | Depois |
|-------|--------|
| `run(self, context)` | `execute(self, context) -> TextResponse` |
| `context.params.get()` | `context.parameters.get()` |
| `context.secrets.get()` | `context.credentials.get()` |
| N/A | `context.constants.get()` (novo) |

---

### Passo 3: Criar agent_definition.yaml

#### Template Base

```yaml
agents:
  seu_agente:  # Chave única do agente (snake_case)
    
    # Informações básicas
    name: "Nome do Seu Agente"
    description: "Descrição detalhada do que o agente faz"
    
    # Credenciais (migrar dos antigos secrets)
    credentials:
      # Para cada secret que você usava:
      nome_credencial:
        label: "Label Amigável"
        placeholder: "Exemplo do valor"
    
    # Constantes (valores configuráveis)
    constants:
      nome_constante:
        label: "Label Amigável"
        value: valor_padrao
    
    # Instruções (mínimo 40 caracteres)
    instructions:
      - "Primeira instrução de comportamento"
      - "Segunda instrução"
      - "Continue adicionando conforme necessário"
    
    # Guardrails (mínimo 40 caracteres)
    guardrails:
      - "Primeiro limite ou restrição"
      - "Segundo limite"
      - "Continue adicionando limites necessários"
    
    # Tools
    tools:
      - tool_key:  # Chave única da tool
          name: "Nome Amigável da Tool"
          source:
            path: "tools/nome_pasta_tool"
            entrypoint: "main.NomeDaClasse"
            path_test: "test_definition.yaml"
          description: "O que esta tool faz"
          parameters:
            - param_name:
                description: "Descrição do parâmetro"
                type: "string"  # string, integer, boolean, etc.
                required: true  # ou false
                contact_field: false  # true se é campo do contato
```

---

### Passo 4: Migrar Cada Tool

#### Exemplo Prático de Migração

**Antes:** `buscar_cep.py`

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class BuscarCEP(Tool):
    def run(self, context: Context):
        cep = context.params.get("cep")
        
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        
        return TextResponse(data=response.json())
```

**Depois:** `tools/buscar_cep/main.py`

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class BuscarCEP(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Atualizado: parameters
        cep = context.parameters.get("cep")
        
        # Pode adicionar constantes se necessário
        timeout = context.constants.get("timeout", 10)
        
        # Lógica mantém igual
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url, timeout=timeout)
        
        return TextResponse(data=response.json())
```

**Novo:** `tools/buscar_cep/test_definition.yaml`

```yaml
tests:
  - name: "CEP válido"
    parameters:
      cep: "01310-100"
    expected_output:
      logradouro: "Avenida Paulista"
```

**YAML Entry:**

```yaml
tools:
  - buscar_cep:
      name: "Buscar CEP"
      source:
        path: "tools/buscar_cep"
        entrypoint: "main.BuscarCEP"
        path_test: "test_definition.yaml"
      description: "Busca endereço completo por CEP"
      parameters:
        - cep:
            description: "CEP brasileiro (8 dígitos)"
            type: "string"
            required: true
            contact_field: false
```

---

### Passo 5: Migrar Credenciais

#### Identificar Secrets Antigos

```python
# No código antigo, você tinha:
api_key = context.secrets.get("API_KEY")
base_url = context.secrets.get("BASE_URL")
token = context.secrets.get("AUTH_TOKEN")
```

#### Adicionar ao YAML

```yaml
credentials:
  api_key:
    label: "API Key"
    placeholder: "Insira sua API Key"
  
  base_url:
    label: "Base URL"
    placeholder: "https://api.exemplo.com"
  
  auth_token:
    label: "Token de Autenticação"
    placeholder: "Bearer xxxxx"
```

#### Atualizar Código

```python
# Código atualizado:
api_key = context.credentials.get("api_key")       # ✅ credentials
base_url = context.credentials.get("base_url")     # ✅ credentials
token = context.credentials.get("auth_token")      # ✅ credentials
```

---

### Passo 6: Criar Testes

Para cada tool, criar `test_definition.yaml`:

```yaml
tests:
  - name: "Teste caso de sucesso"
    parameters:
      param1: "valor1"
      param2: "valor2"
    expected_output:
      campo_esperado: "valor_esperado"
  
  - name: "Teste caso de erro"
    parameters:
      param1: "valor_invalido"
    expected_output:
      error: "Mensagem de erro esperada"
```

---

### Passo 7: Testar Localmente

```bash
# Testar cada tool
weni run agent_definition.yaml seu_agente tool1

# Modo verbose para debug
weni run agent_definition.yaml seu_agente tool1 -v

# Testar todas as tools
weni run agent_definition.yaml seu_agente tool1
weni run agent_definition.yaml seu_agente tool2
weni run agent_definition.yaml seu_agente tool3
```

---

### Passo 8: Deploy

```bash
# Selecionar projeto
weni project list
weni project use <project_uuid>

# Deploy
weni project push agent_definition.yaml

# Se já existe, forçar atualização
weni project push agent_definition.yaml --force-update
```

---

### Passo 9: Configurar Credenciais na Plataforma

1. Acessar Weni Platform
2. Ir em Configurações → Credentials
3. Preencher valores das credenciais definidas no YAML

---

### Passo 10: Validar e Monitorar

```bash
# Ver logs de execução
weni logs --agent seu_agente --tool tool1

# Filtrar por período
weni logs \
  --agent seu_agente \
  --tool tool1 \
  --start-time 2024-01-01T00:00:00
```

---

## 🔍 Checklist de Migração Completa

### Código
- [ ] Método `run()` → `execute()`
- [ ] `context.params` → `context.parameters`
- [ ] `context.secrets` → `context.credentials`
- [ ] Adicionar `context.constants` onde aplicável
- [ ] Type hint no retorno: `-> TextResponse`

### Estrutura
- [ ] Criar pasta `tools/`
- [ ] Mover cada tool para `tools/nome_tool/main.py`
- [ ] Criar `test_definition.yaml` para cada tool
- [ ] Criar `agent_definition.yaml`

### YAML
- [ ] Definir agent name e description
- [ ] Migrar secrets → credentials
- [ ] Adicionar constants (se aplicável)
- [ ] Escrever instructions (mín 40 chars)
- [ ] Escrever guardrails (mín 40 chars)
- [ ] Definir todas as tools
- [ ] Especificar parameters de cada tool

### Testes
- [ ] Criar casos de teste para cada tool
- [ ] Testar localmente com `weni run`
- [ ] Validar outputs esperados

### Deploy
- [ ] Instalar Weni CLI
- [ ] Fazer login
- [ ] Selecionar projeto
- [ ] Deploy com `weni project push`
- [ ] Configurar credentials na plataforma
- [ ] Validar com logs reais

---

## ⚠️ Problemas Comuns

### 1. Erro: "Method 'run' not found"

**Causa:** Código ainda usa `run()` em vez de `execute()`

**Solução:**
```python
# Trocar:
def run(self, context: Context):

# Por:
def execute(self, context: Context) -> TextResponse:
```

---

### 2. Erro: "'params' not found in context"

**Causa:** Código ainda usa `context.params`

**Solução:**
```python
# Trocar:
param = context.params.get("param")

# Por:
param = context.parameters.get("param")
```

---

### 3. Erro: "Credentials not configured"

**Causa:** Credenciais não foram configuradas na plataforma após deploy

**Solução:**
1. Acessar Weni Platform UI
2. Ir em Configurações → Credentials
3. Preencher valores

---

### 4. Tool não é encontrada no deploy

**Causa:** Path ou entrypoint incorreto no YAML

**Solução:**
```yaml
# Verificar:
source:
  path: "tools/nome_tool"        # Deve ser relativo à raiz
  entrypoint: "main.NomeClasse"  # main = arquivo, NomeClasse = classe
```

---

### 5. Testes não passam

**Causa:** test_definition.yaml com formato incorreto

**Solução:**
```yaml
tests:  # Certifique-se que está no plural
  - name: "Nome do teste"  # Use hífen antes de cada teste
    parameters:            # Exatamente como no código
      param: "valor"
    expected_output:
      campo: "valor"
```

---

## 📚 Recursos de Apoio

- [Weni CLI - Guia Completo](04-weni-cli-guia-completo.md)
- [Projeto Completo YAML](exemplos/projeto-completo-yaml.md)
- [API Reference](reference/api-reference.md)
- [Troubleshooting](reference/troubleshooting.md)

---

## 💡 Dicas Pro

### 1. Migre Uma Tool por Vez
Não tente migrar tudo de uma vez. Migre, teste e valide uma tool antes de passar para a próxima.

### 2. Use Git
```bash
git checkout -b migracao-cli
# Faça as alterações
git commit -m "Migração para estrutura CLI"
```

### 3. Mantenha Backup
Guarde a versão antiga até confirmar que a nova está 100% funcional.

### 4. Documente Diferenças
Se você fez customizações específicas, documente-as no README.

### 5. Teste em Ambiente de Dev Primeiro
Não faça deploy direto em produção. Teste em ambiente de desenvolvimento.

---

## 🎯 Resumo do Processo

1. ✅ Backup do projeto
2. ✅ Instalar Weni CLI
3. ✅ Atualizar código das tools (`execute`, `parameters`, `credentials`)
4. ✅ Criar estrutura de pastas
5. ✅ Criar `agent_definition.yaml`
6. ✅ Criar testes
7. ✅ Testar localmente
8. ✅ Deploy
9. ✅ Configurar credentials
10. ✅ Validar em produção

---

**🚀 Sucesso na Migração!**

Se tiver dúvidas, consulte o [Guia Completo da CLI](04-weni-cli-guia-completo.md) ou o [Troubleshooting](reference/troubleshooting.md).
