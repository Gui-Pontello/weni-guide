# 📦 Weni CLI - Análise do Código Oficial

> **Fonte:** Análise direta do repositório [weni-ai/weni-cli](https://github.com/weni-ai/weni-cli)  
> **Versão:** 3.5.2  
> **Data:** Fevereiro 2026

Este documento consolida informações **extraídas diretamente do código-fonte oficial** da Weni CLI, garantindo precisão e atualização.

---

## 📋 Índice

1. [Informações do Repositório](#informações-do-repositório)
2. [Dependências e Requisitos](#dependências-e-requisitos)
3. [Comandos Disponíveis](#comandos-disponíveis)
4. [Context Object - Estrutura Oficial](#context-object---estrutura-oficial)
5. [Testing com weni run](#testing-com-weni-run)
6. [Logs com weni logs](#logs-com-weni-logs)
7. [Exemplos Oficiais](#exemplos-oficiais)
8. [Diferenças vs Documentação Anterior](#diferenças-vs-documentação-anterior)

---

## 📦 Informações do Repositório

### Estrutura do Repositório

```
weni-cli/
├── weni_cli/                 # Código principal
│   ├── commands/             # Implementação dos comandos
│   │   ├── login.py
│   │   ├── project_list.py
│   │   ├── project_use.py
│   │   ├── project_current.py
│   │   ├── project_push.py
│   │   ├── run.py            # ⭐ Testes locais
│   │   ├── logs.py           # ⭐ Fetch de logs
│   │   ├── init.py
│   │   └── channel_create.py
│   ├── clients/              # Cliente API
│   ├── validators/           # Validadores YAML
│   ├── packager/             # Empacotamento de agents
│   └── formatter/            # Formatação de output
├── docs/                     # Documentação oficial
│   ├── examples/             # Exemplos práticos
│   │   ├── cep-agent.md
│   │   ├── book-agent.md
│   │   ├── movie-agent.md
│   │   └── news-agent.md
│   ├── getting-started/
│   ├── user-guide/
│   ├── run/
│   │   ├── tool-run.md       # ⭐ Documentação weni run
│   │   └── logs.md           # ⭐ Documentação weni logs
│   └── core-concepts/
├── tests/                    # Testes automatizados
├── pyproject.toml            # Configuração Poetry
├── README.md
└── CHANGELOG.md
```

### Versão e Metadados

**pyproject.toml:**
```toml
[tool.poetry]
name = "weni-cli"
version = "3.5.2"
description = ""
authors = ["Paulo Bernardo <paulo.bernardo@weni.ai>"]

[tool.poetry.dependencies]
python = "^3.10"
click = "^8.1.8"
requests = "^2.32.3"
flask = "^3.1.1"
waitress = "^3.0.2"
pyyaml = "^6.0.2"
python-slugify = "^8.0.4"
regex = "^2024.11.6"
weni-agents-toolkit = "2.3.3"  # ⭐ SDK oficial
rich-click = "^1.8.6"
rich = "^13.9.4"
```

---

## 🔧 Dependências e Requisitos

### Requisitos Mínimos

```
Python >= 3.10
Poetry >= 1.8.5  (para instalação manual)
```

### Dependências Principais

| Pacote | Versão | Uso |
|--------|--------|-----|
| `weni-agents-toolkit` | 2.3.3 | SDK oficial para criar tools |
| `click` / `rich-click` | ^8.1.8 / ^1.8.6 | Interface CLI |
| `pyyaml` | ^6.0.2 | Parse de agent_definition.yaml |
| `requests` | ^2.32.3 | HTTP client para APIs |
| `flask` + `waitress` | ^3.1.1 + ^3.0.2 | Servidor local para auth |

### Instalação

**Via pip (recomendado):**
```bash
pip install weni-cli
```

**Via Poetry (desenvolvimento):**
```bash
git clone https://github.com/weni-ai/weni-cli.git
cd weni-cli
poetry shell
poetry install
```

---

## 🎯 Comandos Disponíveis

### Arquivo: `weni_cli/commands/`

| Comando | Arquivo | Descrição |
|---------|---------|-----------|
| `weni login` | `login.py` | Autenticação via browser |
| `weni project list` | `project_list.py` | Lista projetos disponíveis |
| `weni project use <uuid>` | `project_use.py` | Seleciona projeto ativo |
| `weni project current` | `project_current.py` | Mostra projeto atual |
| `weni project push <yaml>` | `project_push.py` | Deploy do agent |
| `weni run <yaml> <agent> <tool>` | `run.py` | ⭐ Testa tool localmente |
| `weni logs -a <agent> -t <tool>` | `logs.py` | ⭐ Busca logs de produção |
| `weni init` | `init.py` | Cria estrutura inicial |
| `weni channel create` | `channel_create.py` | Cria canal de comunicação |

---

## 🧩 Context Object - Estrutura Oficial

### Definição (weni-agents-toolkit 2.3.3)

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse

class MyTool(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Context attributes oficiais:
        
        # 1️⃣ Parâmetros da tool
        param = context.parameters.get("param_name")
        
        # 2️⃣ Credenciais (definidas no agent_definition.yaml)
        api_key = context.credentials.get("api_key")
        
        # 3️⃣ Constantes globais (arquivo .globals)
        base_url = context.globals.get("BASE_URL")
        
        # 4️⃣ Informações do usuário
        user_name = context.user.get("name")
        user_id = context.user.get("id")
        
        return TextResponse(data="Response")
```

### Atributos do Context

| Atributo | Tipo | Fonte | Exemplo |
|----------|------|-------|---------|
| `context.parameters` | `dict` | YAML `parameters` | `context.parameters.get("cep")` |
| `context.credentials` | `dict` | `.env` (local) ou Weni Console | `context.credentials.get("api_key")` |
| `context.globals` | `dict` | `.globals` (local) ou Agent config | `context.globals.get("BASE_URL")` |
| `context.user` | `dict` | Weni Platform (usuário atual) | `context.user.get("name")` |

### ⚠️ Importante: Nomenclatura Correta

| ❌ Errado | ✅ Correto |
|-----------|------------|
| `context.params` | `context.parameters` |
| `context.secrets` | `context.credentials` |
| `context.constants` | `context.globals` |

---

## 🧪 Testing com `weni run`

### Comando Completo

```bash
weni run <agent_definition_file> <agent_key> <tool_key> [-f FILE] [-v]
```

### Parâmetros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `agent_definition_file` | posicional | Caminho para `agent_definition.yaml` |
| `agent_key` | posicional | Chave do agent no YAML (ex: `cep_agent`) |
| `tool_key` | posicional | Chave da tool no agent (ex: `get_address`) |
| `-f, --file` | opcional | Arquivo de teste customizado |
| `-v, --verbose` | flag | Logs detalhados para debug |

### Exemplo Prático

**agent_definition.yaml:**
```yaml
agents:
  cep_agent:
    name: "CEP Agent"
    description: "Agent de consulta de CEP"
    instructions:
      - "Você fornece endereços baseados em CEP brasileiro"
    guardrails:
      - "Não responda sobre política ou religião"
    tools:
      - get_address:
          name: "Get Address"
          source:
            path: "tools/get_address"
            entrypoint: "main.GetAddress"
            path_test: "test_definition.yaml"  # ⭐ Path do teste
          description: "Busca endereço por CEP"
          parameters:
            - cep:
                description: "CEP brasileiro"
                type: "string"
                required: true
                contact_field: true
```

**tools/get_address/test_definition.yaml:**
```yaml
tests:
    test_1:
        parameters:
            cep: "01311-000"
    test_2:
        parameters:
            cep: "70150-900"
    test_3:
        parameters:
            cep: "20050-090"
```

**tools/get_address/main.py:**
```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class GetAddress(Tool):
    def execute(self, context: Context) -> TextResponse:
        cep = context.parameters.get("cep", "")
        address = self.get_address_by_cep(cep)
        return TextResponse(data=address)
    
    def get_address_by_cep(self, cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        return response.json()
```

**tools/get_address/requirements.txt:**
```
requests==2.32.3
```

### Executando o Teste

**Teste normal:**
```bash
weni run agent_definition.yaml cep_agent get_address
```

**Output esperado:**
```
✅ Test test_1 passed
✅ Test test_2 passed
✅ Test test_3 passed

All tests passed! 🎉
```

**Teste com logs detalhados:**
```bash
weni run agent_definition.yaml cep_agent get_address -v
```

**Output verbose:**
```
📦 Loading agent definition...
✅ Agent 'cep_agent' found
✅ Tool 'get_address' found
📄 Test file: tools/get_address/test_definition.yaml
🔧 Installing dependencies from requirements.txt...

🧪 Running test_1:
   Parameters: {"cep": "01311-000"}
   📤 Response: {"cep": "01311-000", "logradouro": "Avenida Paulista", ...}
   ✅ Test test_1 passed

🧪 Running test_2:
   Parameters: {"cep": "70150-900"}
   📤 Response: {"cep": "70150-900", "logradouro": "Esplanada dos Ministérios", ...}
   ✅ Test test_2 passed

🧪 Running test_3:
   Parameters: {"cep": "20050-090"}
   📤 Response: {"cep": "20050-090", "logradouro": "Rua da Alfândega", ...}
   ✅ Test test_3 passed

All tests passed! 🎉
```

### Teste Customizado

```bash
weni run agent_definition.yaml cep_agent get_address -f custom_tests.yaml
```

### Descoberta de Arquivos

**Ordem de precedência:**
1. Flag `-f/--file` (se especificada)
2. `source.path_test` no agent_definition.yaml
3. `test_definition.yaml` padrão no diretório da tool

---

## 🔐 Credentials e Globals

### Estrutura de Arquivos

**tools/get_address/.env** (credenciais):
```env
api_key=sk_test_abc123xyz
secret_token=my_secret_value
database_url=postgresql://user:pass@localhost/db
```

**tools/get_address/.globals** (constantes):
```env
BASE_URL=https://api.example.com
API_VERSION=v2
MAX_RETRIES=3
TIMEOUT=30
```

### Uso no Código

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class GetAddressWithAuth(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Parâmetros
        cep = context.parameters.get("cep", "")
        
        # Credenciais (.env)
        api_key = context.credentials.get("api_key")
        
        # Constantes (.globals)
        base_url = context.globals.get("BASE_URL")
        timeout = int(context.globals.get("TIMEOUT", "30"))
        
        # Chamada API
        url = f"{base_url}/cep/{cep}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers, timeout=timeout)
        
        return TextResponse(data=response.json())
```

### Agent Definition com Credentials

```yaml
agents:
  cep_agent:
    credentials:                    # ⭐ Definição das credenciais
      api_key:
        label: "API Key"
        placeholder: "Sua chave de API"
      secret_token:
        label: "Secret Token"
        placeholder: "Token secreto"
    name: "CEP Agent"
    # ... resto da definição
```

### Fluxo de Credentials

**Local (weni run):**
1. CLI lê `.env` no diretório da tool
2. Expõe via `context.credentials`

**Produção (weni project push):**
1. Usuário configura credentials no Weni Console
2. Credentials injetadas automaticamente em `context.credentials`

---

## 📊 Logs com `weni logs`

### Comando Completo

```bash
weni logs --agent <agent_key> --tool <tool_key> [--start-time ISO8601] [--end-time ISO8601] [--pattern TEXT]
```

### Opções

| Opção | Short | Tipo | Descrição |
|-------|-------|------|-----------|
| `--agent` | `-a` | **obrigatório** | Chave do agent (ex: `cep_agent`) |
| `--tool` | `-t` | **obrigatório** | Chave da tool (ex: `get_address`) |
| `--start-time` | `-s` | opcional | Data/hora início (ISO 8601) |
| `--end-time` | `-e` | opcional | Data/hora fim (ISO 8601) |
| `--pattern` | `-p` | opcional | Filtro de texto simples (substring) |

### Formatos de Data/Hora

Aceitos (ISO 8601):
```
2024-01-01T00:00:00
2024-01-01T00:00:00.000
2024-01-01T00:00:00Z
2024-01-01T00:00:00+00:00
2024-01-01T00:00:00-03:00
```

### Exemplos Práticos

**1. Logs básicos:**
```bash
weni logs -a cep_agent -t get_address
```

**2. Com filtro de tempo:**
```bash
weni logs -a cep_agent -t get_address \
  -s 2024-01-01T00:00:00 \
  -e 2024-01-01T23:59:59
```

**3. Com padrão de busca:**
```bash
weni logs -a cep_agent -t get_address -p error
```

**4. Combinação completa:**
```bash
weni logs -a cep_agent -t get_address \
  -s 2024-02-10T08:00:00-03:00 \
  -e 2024-02-11T18:00:00-03:00 \
  -p "timeout"
```

### Output

```
[2024-02-10 08:15:23] Starting tool execution: get_address
[2024-02-10 08:15:23] Parameters: {"cep": "01311-000"}
[2024-02-10 08:15:24] API Response: 200 OK
[2024-02-10 08:15:24] Tool execution completed successfully
```

### Paginação

Se houver mais logs:
```
Fetch more logs? [Y/n]: y
```

- **Y/Enter**: Busca próxima página
- **n**: Interrompe busca

### ⚠️ Limitações

- ❌ **Regex NÃO suportado** em `--pattern`
- ✅ **Apenas substring simples** (case-insensitive)
- Padrões como `%error%` ou `^error$` **não funcionam**

---

## 📚 Exemplos Oficiais

### 1. CEP Agent (Simples)

**Localização:** `docs/examples/cep-agent.md`

**Funcionalidade:** Busca de endereço por CEP usando ViaCEP API

**agent_definition.yaml:**
```yaml
agents:
  sample_agent:
    name: "CEP Agent"
    description: "Weni's CEP agent"
    instructions:
      - "You are an expert in providing addresses based on postal codes"
    guardrails:
      - "Keep it neutral and professional"
    tools:
      - get_address:
          name: "Get Address"
          source:
            path: "tools/get_address"
            entrypoint: "main.GetAddress"
            path_test: "test_definition.yaml"
          description: "Get address from postal code"
          parameters:
            - cep:
                description: "Brazilian postal code"
                type: "string"
                required: true
                contact_field: true
```

**tools/get_address/main.py:**
```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class GetAddress(Tool):
    def execute(self, context: Context) -> TextResponse:
        cep = context.parameters.get("cep", "")
        address_response = self.get_address_by_cep(cep=cep)
        return TextResponse(data=address_response)

    def get_address_by_cep(self, cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        return response.json()
```

### 2. Book Agent (Com Credentials)

**Localização:** `docs/examples/book-agent.md`

**Funcionalidade:** Busca de livros na Google Books API

**agent_definition.yaml (parcial):**
```yaml
agents:
  book_agent:
    credentials:
      apiKey:
        label: "Google Books API Key"
        placeholder: "Your API Key"
    name: "Book Agent"
    # ...
    tools:
      - get_books:
          name: "Search Books"
          source:
            path: "tools/get_books"
            entrypoint: "books.GetBooks"
            path_test: "test_definition.yaml"
          parameters:
            - book_title:
                description: "Book title to search"
                type: "string"
                required: true
```

**tools/get_books/books.py:**
```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class GetBooks(Tool):
    def execute(self, context: Context) -> TextResponse:
        # ⭐ Acessando credential
        api_key = context.credentials.get("apiKey")
        
        book_title = context.parameters.get("book_title", "")
        books = self.get_books_by_title(title=book_title, key=api_key)
        
        # Formatação da resposta
        items = books.get("items", [])
        if not items:
            return TextResponse(data="No books found.")
        
        response_data = {
            "status": "success",
            "totalResults": len(items[:5]),
            "books": []
        }
        
        for book in items[:5]:
            volume_info = book.get("volumeInfo", {})
            book_data = {
                "id": book.get("id"),
                "title": volume_info.get("title"),
                "authors": volume_info.get("authors", []),
                "publisher": volume_info.get("publisher"),
                "publishedDate": volume_info.get("publishedDate"),
                "description": volume_info.get("description", ""),
                "pageCount": volume_info.get("pageCount"),
                "averageRating": volume_info.get("averageRating"),
            }
            response_data["books"].append(book_data)
        
        return TextResponse(data=response_data)
    
    def get_books_by_title(self, title, key=None):
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {"q": title}
        if key:
            params["key"] = key
        response = requests.get(url, params=params)
        return response.json()
```

**tools/get_books/.env** (para testes locais):
```env
apiKey=AIzaSyABC123XYZ789...
```

### 3. Outros Exemplos Disponíveis

- **Movie Agent** (`docs/examples/movie-agent.md`): TMDb API integration
- **News Agent** (`docs/examples/news-agent.md`): NewsAPI integration

---

## ⚡ Diferenças vs Documentação Anterior

### Nomenclatura Corrigida

| Documentação Anterior | ✅ Código Oficial | Fonte |
|-----------------------|-------------------|-------|
| `context.params` | `context.parameters` | `weni-agents-toolkit` |
| `context.secrets` | `context.credentials` | `weni-agents-toolkit` |
| `context.constants` | `context.globals` | `weni-agents-toolkit` |
| `def run(self, context)` | `def execute(self, context)` | `Tool` base class |

### Comando weni run

**Anterior:**
```bash
weni test <agent> <tool>           # ❌ Incompleto
```

**Oficial:**
```bash
weni run <yaml> <agent> <tool> [-f FILE] [-v]    # ✅ Completo
```

### Test Definition

**Anterior (hipotético):**
```yaml
# ❌ Estrutura não documentada
tests:
  - cep: "01311-000"
  - cep: "70150-900"
```

**Oficial:**
```yaml
# ✅ Estrutura oficial
tests:
    test_1:
        parameters:
            cep: "01311-000"
    test_2:
        parameters:
            cep: "70150-900"
```

### Credentials

**Anterior:**
```python
# ❌ Nomenclatura incorreta
api_key = context.secrets.get("api_key")
```

**Oficial:**
```python
# ✅ Nomenclatura oficial
api_key = context.credentials.get("api_key")
```

### Source Path Test

**Anterior:**
```yaml
# ❌ Não documentado
tools:
  - get_address:
      source:
        path: "tools/get_address"
```

**Oficial:**
```yaml
# ✅ Com path_test opcional
tools:
  - get_address:
      source:
        path: "tools/get_address"
        entrypoint: "main.GetAddress"
        path_test: "test_definition.yaml"  # ⭐ Opcional
```

---

## 🎯 Checklist de Migração

Se você está usando a documentação anterior, atualize:

- [ ] **Renomear** `context.params` → `context.parameters`
- [ ] **Renomear** `context.secrets` → `context.credentials`
- [ ] **Renomear** `context.constants` → `context.globals`
- [ ] **Renomear** método `run()` → `execute()` nas tools
- [ ] **Atualizar** estrutura do `test_definition.yaml`
- [ ] **Adicionar** `path_test` no `agent_definition.yaml` (opcional)
- [ ] **Criar** arquivos `.env` e `.globals` quando necessário
- [ ] **Testar** com `weni run <yaml> <agent> <tool> -v`
- [ ] **Verificar** logs com `weni logs -a <agent> -t <tool>`

---

## 📖 Recursos Adicionais

### Repositório Oficial
- **GitHub:** https://github.com/weni-ai/weni-cli
- **Docs:** https://weni-ai.github.io/weni-cli/

### Dependências
- **weni-agents-toolkit:** 2.3.3
- **Python:** >= 3.10

### Comunidade
- **Issues:** https://github.com/weni-ai/weni-cli/issues
- **Pull Requests:** Bem-vindos!

---

## ✅ Conclusão

Este documento reflete a **implementação real** da Weni CLI baseada no código-fonte oficial (v3.5.2). Todas as informações foram extraídas diretamente do repositório e validadas com os exemplos oficiais.

**Use este guia como referência principal** para garantir compatibilidade e evitar problemas com nomenclaturas incorretas ou comandos desatualizados.

---

**📅 Última atualização:** 11 de fevereiro de 2026  
**🔗 Repositório analisado:** [weni-ai/weni-cli](https://github.com/weni-ai/weni-cli) @ commit mais recente
