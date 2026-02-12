# ⚡ Quick Reference - Weni Platform

> Comandos e snippets essenciais para o dia a dia

---

## 🔧 Weni CLI - Comandos Essenciais

### Autenticação
```bash
weni login                          # Login na plataforma
weni logout                         # Logout
```

### Gerenciamento de Projetos
```bash
weni project list                   # Listar projetos
weni project use <PROJECT_ID>       # Selecionar projeto
weni project current                # Ver projeto atual
```

### Deploy
```bash
weni project push                   # Deploy do projeto
weni project push --verbose          # Deploy com logs detalhados
```

### Testes
```bash
weni run <tool_name>                # Executar tool localmente
weni run <tool_name> --verbose      # Com debug
weni run <tool_name> --test-file custom.yaml
```

### Logs
```bash
weni logs <agent_name>              # Ver logs do agente
weni logs <agent_name> --tail       # Logs em tempo real
```

---

## 📁 Estrutura de Projeto

```
meu-projeto/
├── agent_definition.yaml       # Configuração do agente
└── tools/
    └── minha_tool/
        ├── main.py             # Código da tool
        ├── requirements.txt    # Dependências
        └── test_definition.yaml # Testes
```

---

## 🐍 Python - Template de Tool

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class MinhaTool(Tool):
    def execute(self, context: Context):
        # 1. Obter parâmetros
        param = context.params.get("parametro")
        if not param:
            return TextResponse(data={"error": "Parâmetro obrigatório"})
        
        # 2. Obter credenciais
        api_key = context.secrets.get("API_KEY")
        base_url = context.secrets.get("BASE_URL")
        
        # 3. Obter constantes (opcional)
        constant = context.constants.get("MINHA_CONSTANTE")
        
        # 4. Fazer requisição
        try:
            response = requests.get(
                f"{base_url}/endpoint",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"ERROR: {e}")
            return TextResponse(data={"error": str(e)})
        
        # 5. Retornar resultado
        return TextResponse(data={
            "message": "Sucesso!",
            "resultado": data
        })
```

---

## 📝 YAML - agent_definition.yaml

```yaml
agents:
  meu_agente:
    # Credenciais (gerenciadas pela Weni)
    credentials:
      API_KEY:
        label: "API Key"
        placeholder: "sua-api-key"
        is_confidential: true
      BASE_URL:
        label: "Base URL"
        placeholder: "https://api.exemplo.com"
        is_confidential: false
    
    # Constantes (valores fixos)
    constants:
      MAX_RESULTS:
        value: 50
      TIMEOUT_SECONDS:
        value: 30
    
    # Metadados
    name: "Nome do Agente"
    description: "Quando o Manager deve invocar este agente"
    
    # Instruções (o que fazer)
    instructions:
      - "Você deve sempre fazer X"
      - "Quando receber Y, faça Z"
      - "Sempre retorne W"
    
    # Guardrails (o que NÃO fazer)
    guardrails:
      - "Nunca invente dados"
      - "Nunca exponha credenciais"
    
    # Tools
    tools:
      - minha_tool:
          name: "Nome da Tool"
          source:
            path: "tools/minha_tool"
            entrypoint: "main.MinhaTool"
            path_test: "test_definition.yaml"
          description: "O que esta tool faz"
          parameters:
            - parametro1:
                description: "Descrição do parâmetro"
                type: "string"
                required: true
                contact_field: false
```

---

## 🧪 test_definition.yaml

```yaml
- name: "Teste caso sucesso"
  parameters:
    parametro1: "valor_teste"
  expected_output:
    message: "Sucesso!"
  
- name: "Teste caso erro"
  parameters:
    parametro1: ""
  expected_error: true
```

---

## 🛒 VTEX - Endpoints Principais

### 1. Regionalização (valida CEP)
```
GET /api/checkout/pub/regions?country=BRA&postalCode={cep}&sc=1
```

### 2. Busca de Produtos
```
GET /_v/api/intelligent-search/product_search/{query}?regionId={id}&count=50
```

### 3. Simulação de Frete
```
POST /api/checkout/pub/orderforms/simulation
Body: {
  "items": [{"id": "123", "quantity": 1, "seller": "1"}],
  "postalCode": "03001000",
  "country": "BRA"
}
```

### 4. Detalhes do SKU
```
GET /api/catalog/pvt/stockkeepingunit/{skuId}
Headers:
  X-VTEX-API-AppKey: {appkey}
  X-VTEX-API-AppToken: {apptoken}
```

### 5. Criar Carrinho
```
POST /api/checkout/pub/orderForm
```

### 6. Consultar Pedido
```
GET /api/oms/pvt/orders/{orderId}
Headers: (mesmos da API 4)
```

---

## 🌊 Weni Flows - Trigger

```python
import requests

def trigger_flow(api_token, event_uuid, phone, data):
    """Dispara um Weni Flow"""
    url = "https://flows.weni.ai/api/v2/flow_starts.json"
    
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "flow": event_uuid,
        "urns": [f"whatsapp:{phone}"],
        "extra": data
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 200
```

---

## 🔍 Debugging - Print Estratégico

```python
# Início de operação
print(f"DEBUG: Iniciando busca - Query: '{query}'")

# Antes de API call
print(f"DEBUG: URL: {url}")

# Após API call
print(f"DEBUG: Status: {response.status_code}")

# Pontos de decisão
if condition:
    print(f"INFO: Condição X atendida")

# Resultados
print(f"INFO: {len(items)} itens encontrados")

# Alertas
print(f"WARN: Payload grande, limitando resultados")

# Erros
print(f"ERROR: Falha na requisição: {error}")
```

---

## ✅ Context Object - Propriedades

```python
# Parâmetros da requisição
context.params.get("nome_parametro")
context.params.get("opcional", "valor_default")

# Credenciais (secrets)
context.secrets.get("API_KEY")
context.secrets.get("BASE_URL")

# Constantes
context.constants.get("MAX_RESULTS")

# Informações do usuário
context.user.get("name")
context.user.get("phone")
context.user.get("email")
```

---

## 📤 TextResponse - Retorno

```python
# Sucesso simples
return TextResponse(data={
    "message": "Operação concluída"
})

# Com múltiplos campos
return TextResponse(data={
    "products": [...],
    "total": 10,
    "message": "Encontrados 10 produtos"
})

# Erro
return TextResponse(data={
    "error": "Descrição do erro"
})
```

---

## 🔐 Segurança - Checklist

### ❌ NUNCA faça:
- Commitar credenciais no código
- Logar senhas ou tokens
- Expor PII (CPF, email) em logs
- Retornar credenciais no TextResponse

### ✅ SEMPRE faça:
- Usar `context.secrets` para credenciais
- Marcar `is_confidential: true` no YAML
- Validar parâmetros antes de usar
- Tratar erros adequadamente
- Logar apenas dados não-sensíveis

---

## 🚨 Troubleshooting Rápido

### Tool não executa
```bash
# Verificar estrutura
ls -la tools/minha_tool/

# Testar localmente
weni run minha_tool --verbose

# Ver logs
weni logs meu_agente --tail
```

### Erro de import
```bash
# Verificar requirements.txt
cat tools/minha_tool/requirements.txt

# Reinstalar deps localmente
pip install -r tools/minha_tool/requirements.txt
```

### Payload muito grande
```python
# Limitar resultados
products = products[:20]

# Remover campos desnecessários
for p in products:
    p.pop('campo_grande', None)
```

### API retorna erro
```python
# Adicionar tratamento
try:
    response = requests.get(url, timeout=30)
    print(f"DEBUG: Status {response.status_code}")
    print(f"DEBUG: Body: {response.text[:500]}")
    response.raise_for_status()
except requests.exceptions.Timeout:
    print("ERROR: Timeout na requisição")
except requests.exceptions.HTTPError as e:
    print(f"ERROR: HTTP {e.response.status_code}")
```

---

## 📊 Status Codes HTTP

| Código | Significado | Ação |
|--------|-------------|------|
| 200 | OK | Processar resposta |
| 400 | Bad Request | Validar parâmetros |
| 401 | Unauthorized | Checar credenciais |
| 404 | Not Found | Recurso não existe |
| 429 | Too Many Requests | Implementar retry |
| 500 | Server Error | Retry com backoff |

---

## 🎯 Padrões de Código

### Validação de Parâmetros
```python
def validate_params(context):
    required = ["param1", "param2"]
    for param in required:
        if not context.params.get(param):
            return False, f"Parâmetro '{param}' obrigatório"
    return True, None

# Uso
valid, error = validate_params(context)
if not valid:
    return TextResponse(data={"error": error})
```

### Request com Retry
```python
import time

def request_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt  # Exponential backoff
                time.sleep(wait)
            else:
                raise e
```

### Formatação de CEP
```python
def format_cep(cep):
    """Remove caracteres e formata CEP"""
    cep = ''.join(filter(str.isdigit, cep))
    if len(cep) == 8:
        return f"{cep[:5]}-{cep[5:]}"
    return cep
```

---

## 📚 Documentação Completa

**Para detalhes completos, consulte:**

- 📘 [Visão 360° - Projeto Weni & Obramax](docs/08-visao-360-projeto-weni-obramax.md)
- 🗺️ [Índice Rápido](INDICE-RAPIDO.md)
- 🚀 [Guia de Início Rápido](docs/00-guia-inicio-rapido.md)
- 📖 [Documentação Completa](docs/README.md)

---

**Dica:** Imprima esta página ou salve como PDF para referência offline! 🖨️
