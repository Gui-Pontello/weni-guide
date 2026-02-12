# Weni CLI - Guia Completo

## 🎯 Visão Geral

**Weni CLI** é uma ferramenta de linha de comando que simplifica a criação e gerenciamento de múltiplos agentes de IA de forma rápida e eficiente. Integrada com a plataforma Weni, permite desenvolvimento e deploy de agentes de alta performance em diversos canais de comunicação (WhatsApp, Instagram, Facebook, etc.).

## ✨ O que você pode fazer com a Weni CLI:

- ✅ Criar agentes de IA
- ✅ Adicionar tools customizadas aos seus agentes
- ✅ Fazer deploy de agentes
- ✅ Atualizar configurações e comportamentos
- ✅ Gerenciar múltiplos agentes em seus projetos
- ✅ Testar tools localmente
- ✅ Visualizar logs de execução

---

## 📋 Requisitos

- **Python** >= 3.10
- **Poetry** >= 1.8.5 (para instalação manual)
- Conta na [Plataforma Weni](https://weni.ai/)

---

## 🚀 Instalação

### Método 1: Via PIP (Recomendado)

```bash
pip install weni-cli
```

### Método 2: Instalação Manual (Desenvolvimento)

```bash
# Clone o repositório
git clone https://github.com/weni-ai/weni-cli.git
cd weni-cli

# Instale as dependências
poetry shell
poetry install
```

### Verificar Instalação

```bash
weni
```

Se instalado corretamente, você verá a lista de comandos disponíveis.

```bash
weni --version
```

Mostra a versão instalada da CLI.

---

## 🔐 Autenticação

### 1. Login na Plataforma

```bash
weni login
```

Este comando:
1. Abre o navegador automaticamente
2. Redireciona para a página de login da Weni
3. Após login bem-sucedido, retorna ao terminal
4. Exibe mensagem: **"Login Successfully"**

> **Nota:** O servidor de callback local escuta em `http://localhost:50051/sso-callback`

### 2. Gerenciar Projetos

```bash
# Listar todos os projetos
weni project list

# Listar projetos de uma organização específica
weni project list --org <org_uuid>

# Selecionar projeto para trabalhar
weni project use <project_uuid>

# Ver projeto atual
weni project current
```

---

## 🏗️ Estrutura de Projeto

### Estrutura Básica

```
meu-projeto/
├── agent_definition.yaml    # Definição do agente
└── tools/                   # Pasta de tools (recomendado)
    └── minha_tool/
        ├── main.py          # Código da tool
        └── test_definition.yaml  # Testes
```

### Arquivo `agent_definition.yaml`

```yaml
agents:
  meu_agente:
    name: "Meu Agente"
    description: "Descrição do meu agente"
    
    # Credenciais (opcionais)
    credentials:
      api_key:
        label: "API Key"
        placeholder: "Insira sua API Key"
    
    # Constantes (opcionais)
    constants:
      max_retries:
        label: "Max Retries"
        value: 3
    
    # Instruções (mínimo 40 caracteres)
    instructions:
      - "Você é um especialista em atendimento ao cliente"
      - "Sempre seja educado e prestativo"
    
    # Guardrails (mínimo 40 caracteres)
    guardrails:
      - "Não discuta política, religião ou tópicos sensíveis"
      - "Mantenha a conversa profissional"
    
    # Tools
    tools:
      - buscar_endereco:
          name: "Buscar Endereço"
          source:
            path: "tools/buscar_endereco"
            entrypoint: "main.BuscarEndereco"
            path_test: "test_definition.yaml"
          description: "Busca endereço por CEP"
          parameters:
            - cep:
                description: "CEP para busca"
                type: "string"
                required: true
                contact_field: true
```

---

## 🔧 Criando uma Tool

### Estrutura de uma Tool

```python
# tools/buscar_endereco/main.py
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class BuscarEndereco(Tool):
    def execute(self, context: Context) -> TextResponse:
        # 1. Extrair parâmetros
        cep = context.parameters.get("cep", "")
        
        # 2. Processar lógica
        endereco = self.obter_endereco_por_cep(cep)
        
        # 3. Retornar resposta
        return TextResponse(data=endereco)
    
    def obter_endereco_por_cep(self, cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        return response.json()
```

### Tool com Credenciais

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class MinhaToolComAuth(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Extrair credenciais do contexto
        api_key = context.credentials.get("api_key")
        
        if not api_key:
            return TextResponse(data={
                "error": "API Key não configurada"
            })
        
        # Usar API key
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(url, headers=headers)
        return TextResponse(data=response.json())
```

### Tool com Constantes

```python
class MinhaToolComConstantes(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Extrair constantes
        max_retries = context.constants.get("max_retries", 3)
        timeout = context.constants.get("timeout", 30)
        
        # Usar nas requisições
        for i in range(max_retries):
            try:
                response = requests.get(url, timeout=timeout)
                return TextResponse(data=response.json())
            except Exception as e:
                if i == max_retries - 1:
                    raise e
                continue
```

---

## 🎯 Comandos Principais

### Inicialização

```bash
# Criar setup inicial com exemplo
weni init
```

### Deploy e Atualização

```bash
# Deploy/atualizar agentes
weni project push agent_definition.yaml

# Forçar atualização (sobrescrever)
weni project push agent_definition.yaml --force-update
```

### Teste Local de Tools

```bash
# Rodar tool específica localmente
weni run agent_definition.yaml [agent_key] [tool_key]

# Especificar arquivo de teste customizado
weni run agent_definition.yaml meu_agente buscar_endereco -f custom_test.yaml

# Modo verbose (logs detalhados)
weni run agent_definition.yaml meu_agente buscar_endereco -v
```

**Exemplo de `test_definition.yaml`:**

```yaml
tests:
  - name: "Test CEP válido"
    parameters:
      cep: "01310-100"
    expected_output:
      logradouro: "Avenida Paulista"
```

### Logs de Execução

```bash
# Ver logs de execução de uma tool
weni logs --agent meu_agente --tool buscar_endereco

# Filtrar por período (ISO 8601)
weni logs \
  --agent meu_agente \
  --tool buscar_endereco \
  --start-time 2024-01-01T00:00:00 \
  --end-time 2024-01-31T23:59:59

# Filtrar por padrão de texto
weni logs \
  --agent meu_agente \
  --tool buscar_endereco \
  --pattern "ERROR"
```

### Canais de Comunicação

```bash
# Criar canal de comunicação
weni channel create channel_definition.yaml
```

---

## 📝 Context Object Completo

O objeto `Context` contém todas as informações necessárias:

```python
# Parâmetros enviados pelo usuário
context.parameters.get("param_name")

# Credenciais configuradas no YAML
context.credentials.get("api_key")

# Constantes definidas no YAML
context.constants.get("constant_name")

# Informações do usuário
context.user.get("urn")          # Ex: "whatsapp:5511999999999"
context.user.get("channel")      # Canal de origem
```

---

## 🎨 Tipos de Agentes

### Passive Agents (Reativos)

Agentes que **reagem** a input do usuário ou triggers específicos:

- Atendem quando usuário envia mensagem
- Executam tools baseadas no contexto da conversa
- Otimizados para atendimento ao cliente

```yaml
agents:
  atendente_passivo:
    name: "Atendente Virtual"
    instructions:
      - "Responda perguntas do cliente sobre produtos"
    tools:
      - buscar_produtos:
          # ... configuração
```

### Active Agents (Proativos)

Agentes que **iniciam** conversas ou ações automaticamente:

- Enviam notificações
- Fazem follow-ups proativos
- Disparam ações agendadas

---

## ✅ Melhores Práticas

### 1. Organização de Código

```
✅ BOA PRÁTICA:
projeto/
├── agent_definition.yaml
└── tools/
    ├── tool1/main.py
    ├── tool2/main.py
    └── tool3/main.py

❌ EVITE:
projeto/
├── agent.yaml
├── tool1.py
├── tool2.py
└── tool3.py
```

### 2. Nomenclatura

```yaml
# ✅ BOA PRÁTICA: Nomes descritivos
agents:
  atendimento_cliente:
    tools:
      - buscar_produtos:
          name: "Buscar Produtos"

# ❌ EVITE: Nomes genéricos
agents:
  agent1:
    tools:
      - tool1:
          name: "Tool"
```

### 3. Responsabilidade Única

```python
# ✅ BOA PRÁTICA: Uma tool, uma função
class BuscarEndereco(Tool):
    """Busca endereço por CEP"""
    pass

class ValidarCEP(Tool):
    """Valida formato de CEP"""
    pass

# ❌ EVITE: Tool fazendo muitas coisas
class EnderecoEValidacao(Tool):
    """Faz tudo relacionado a endereço"""
    pass
```

### 4. Tratamento de Erros

```python
def execute(self, context: Context) -> TextResponse:
    try:
        cep = context.parameters.get("cep")
        
        if not cep:
            return TextResponse(data={
                "error": "CEP é obrigatório"
            })
        
        resultado = self.processar(cep)
        return TextResponse(data=resultado)
    
    except requests.exceptions.RequestException as e:
        return TextResponse(data={
            "error": "Erro ao consultar serviço externo"
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return TextResponse(data={
            "error": "Erro inesperado ao processar requisição"
        })
```

### 5. Versionamento

- Use Git para versionar seus agentes
- Crie tags para releases
- Documente mudanças no README

---

## 🐛 Troubleshooting

### Problema: "weni: command not found"

**Solução:**
```bash
# Reinstalar
pip install --upgrade weni-cli

# Ou adicionar ao PATH
export PATH="$PATH:~/.local/bin"
```

### Problema: Erro de autenticação

**Solução:**
```bash
# Fazer logout e login novamente
weni login
```

### Problema: Tool não encontrada no deploy

**Solução:**
- Verificar path no YAML
- Confirmar entrypoint correto
- Checar se arquivo existe

```yaml
# ✅ Path relativo à raiz do projeto
source:
  path: "tools/minha_tool"
  entrypoint: "main.MinhaTool"
```

### Problema: Credenciais não acessíveis

**Solução:**
1. Configurar no YAML:
```yaml
credentials:
  api_key:
    label: "API Key"
```

2. Configurar na plataforma Weni UI
3. Acessar via `context.credentials.get("api_key")`

---

## 📊 Exemplo Completo: Agente de CEP

### 1. Estrutura

```
projeto-cep/
├── agent_definition.yaml
└── tools/
    └── buscar_endereco/
        ├── main.py
        └── test_definition.yaml
```

### 2. agent_definition.yaml

```yaml
agents:
  agente_cep:
    name: "Agente CEP"
    description: "Agente especializado em buscar endereços por CEP"
    
    instructions:
      - "Você é um especialista em fornecer endereços baseado em CEP"
      - "O usuário enviará um CEP e você deve retornar o endereço correspondente"
    
    guardrails:
      - "Não discuta política, religião ou tópicos sensíveis"
      - "Mantenha o foco em endereços e CEPs"
    
    tools:
      - buscar_endereco:
          name: "Buscar Endereço"
          source:
            path: "tools/buscar_endereco"
            entrypoint: "main.BuscarEndereco"
            path_test: "test_definition.yaml"
          description: "Busca endereço completo por CEP"
          parameters:
            - cep:
                description: "CEP do local (8 dígitos com ou sem hífen)"
                type: "string"
                required: true
                contact_field: true
```

### 3. tools/buscar_endereco/main.py

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests
import re

class BuscarEndereco(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Extrai CEP
        cep = context.parameters.get("cep", "")
        
        print(f"INFO: Buscando endereço para CEP: {cep}")
        
        # Valida formato
        if not self.validar_cep(cep):
            return TextResponse(data={
                "error": "CEP inválido. Use formato: 12345-678 ou 12345678"
            })
        
        # Busca endereço
        endereco = self.obter_endereco_por_cep(cep)
        
        if endereco.get("erro"):
            return TextResponse(data={
                "error": "CEP não encontrado"
            })
        
        print(f"INFO: Endereço encontrado: {endereco.get('logradouro')}")
        return TextResponse(data=endereco)
    
    def validar_cep(self, cep):
        """Valida formato de CEP brasileiro"""
        pattern = r'^\d{5}-?\d{3}$'
        return bool(re.match(pattern, cep))
    
    def obter_endereco_por_cep(self, cep):
        """Consulta API ViaCEP"""
        # Remove hífen para consulta
        cep_limpo = cep.replace("-", "")
        
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"ERROR: Falha ao consultar ViaCEP: {e}")
            return {"erro": True}
```

### 4. tools/buscar_endereco/test_definition.yaml

```yaml
tests:
  - name: "CEP válido - Av Paulista"
    parameters:
      cep: "01310-100"
    expected_output:
      logradouro: "Avenida Paulista"
      bairro: "Bela Vista"
      localidade: "São Paulo"
      uf: "SP"
  
  - name: "CEP sem hífen"
    parameters:
      cep: "01310100"
    expected_output:
      logradouro: "Avenida Paulista"
  
  - name: "CEP inválido"
    parameters:
      cep: "123"
    expected_output:
      error: "CEP inválido"
```

### 5. Comandos

```bash
# Testar localmente
weni run agent_definition.yaml agente_cep buscar_endereco

# Testar com verbose
weni run agent_definition.yaml agente_cep buscar_endereco -v

# Deploy
weni project push agent_definition.yaml

# Ver logs
weni logs --agent agente_cep --tool buscar_endereco
```

---

## 🔗 Recursos Adicionais

### Documentação Oficial
- [Weni CLI Documentation](https://weni-ai.github.io/weni-cli/)
- [GitHub Repository](https://github.com/weni-ai/weni-cli)

### Nossa Documentação
- [Estrutura de Projetos](01-estrutura-projetos.md)
- [Padrões e Boas Práticas](02-padroes-boas-praticas.md)
- [APIs e Integrações](03-apis-integracoes.md)
- [API Reference](reference/api-reference.md)

### Comunidade
- [GitHub Issues](https://github.com/weni-ai/weni-cli/issues)
- [Platform Weni](https://weni.ai/)

---

## ⚡ Resumo de Comandos

| Comando | Descrição |
|---------|-----------|
| `weni` | Mostra comandos disponíveis |
| `weni --version` | Versão da CLI |
| `weni init` | Criar projeto inicial |
| `weni login` | Autenticar na plataforma |
| `weni project list` | Listar projetos |
| `weni project use <uuid>` | Selecionar projeto |
| `weni project push <yaml>` | Deploy de agente |
| `weni run <yaml> <agent> <tool>` | Testar tool localmente |
| `weni logs --agent <a> --tool <t>` | Ver logs de execução |
| `weni channel create <yaml>` | Criar canal |

---

**🎉 Pronto!** Agora você domina a Weni CLI e pode criar agentes profissionais de forma eficiente!
