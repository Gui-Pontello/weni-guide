# API Reference - Referência Rápida

## 🚀 Quick Start

### Template Básico de Tool

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class MyTool(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Parâmetros
        param = context.parameters.get("param_name")
        
        # Credenciais
        api_key = context.credentials.get("api_key")
        
        # Constantes
        max_items = context.constants.get("max_items", 10)
        
        # Lógica
        result = self.process(param, api_key, max_items)
        
        # Retorno
        return TextResponse(data=result)
    
    def process(self, param, api_key, max_items):
        # Implementação
        return {"status": "success"}
```

---

## ⚡ Comandos Weni CLI

### Essenciais

```bash
# Ajuda e versão
weni                  # Lista comandos disponíveis
weni --version        # Mostra versão da CLI

# Autenticação
weni login            # Login na plataforma

# Gerenciamento de projetos
weni project list     # Lista projetos
weni project use <uuid>  # Seleciona projeto
weni project current  # Mostra projeto atual

# Deploy
weni project push agent_definition.yaml           # Deploy
weni project push agent_definition.yaml --force-update  # Força atualização

# Desenvolvimento
weni init             # Cria projeto inicial
weni run <yaml> <agent> <tool>      # Testa tool localmente
weni run <yaml> <agent> <tool> -v   # Modo verbose
weni run <yaml> <agent> <tool> -f custom_test.yaml  # Teste customizado

# Logs e monitoramento
weni logs --agent <name> --tool <name>  # Ver logs
weni logs --agent <name> --tool <name> --start-time 2024-01-01T00:00:00
weni logs --agent <name> --tool <name> --pattern "ERROR"

# Canais
weni channel create channel_definition.yaml  # Criar canal
```

---

## 📦 Context Object

### Estrutura

```python
context.parameters   # dict - Parâmetros de entrada
context.credentials  # dict - Credenciais/variáveis de ambiente sensíveis
context.constants    # dict - Constantes configuráveis do agente
context.user         # dict - Informações do usuário
```

### Exemplos

```python
# Parâmetros (enviados pelo usuário)
product_name = context.parameters.get("product_name")
quantity = int(context.parameters.get("quantity", 1))

# Credenciais (configuradas no YAML e na plataforma)
base_url = context.credentials.get("base_url")
api_key = context.credentials.get("api_key")

# Constantes (configuradas no YAML)
max_items = int(context.constants.get("max_items", 10))
timeout = int(context.constants.get("timeout", 30))

# User
user_urn = context.user.get("urn")  # Ex: "whatsapp:5511999999999"
channel = context.user.get("channel")
```

---

## 🔄 Response Types

### TextResponse

```python
# Sucesso
return TextResponse(data={
    "products": [...],
    "total": 10
})

# Erro
return TextResponse(data={
    "error": "Mensagem de erro user-friendly"
})

# Mensagem informativa
return TextResponse(data={
    "message": "Operação concluída com sucesso"
})
```

---

## 🛒 VTEX APIs - Quick Reference

### 1. Regionalização

**GET** `/api/checkout/pub/regions`

```python
url = f"{base_url}/api/checkout/pub/regions"
params = {
    "country": "BRA",
    "postalCode": "01310100",
    "sc": "1"
}
response = requests.get(url, params=params)
```

**Response:**
```json
[{"id": "v2.ABC123", "sellers": [{"id": "1"}]}]
```

---

### 2. Intelligent Search

**GET** `/api/io/_v/api/intelligent-search/product_search/`

```python
url = f"{base_url}/api/io/_v/api/intelligent-search/product_search/"
params = {
    "query": "cimento",
    "hideUnavailableItems": "true",
    "regionId": "v2.ABC123"  # opcional
}
response = requests.get(url, params=params)
```

**Response:**
```json
{
  "products": [
    {
      "productName": "Cimento CP II",
      "brand": "Votorantim",
      "items": [...]
    }
  ]
}
```

---

### 3. Cart Simulation

**POST** `/api/checkout/pub/orderForms/simulation`

```python
url = f"{base_url}/api/checkout/pub/orderForms/simulation"
payload = {
    "items": [
        {"id": "123456", "quantity": 1, "seller": "1"}
    ],
    "postalCode": "01310100",
    "country": "BRA"
}
response = requests.post(url, json=payload)
```

**Response:**
```json
{
  "items": [
    {
      "id": "123456",
      "quantity": 10,
      "price": 8990,
      "availability": "available"
    }
  ],
  "logisticsInfo": [...]
}
```

---

### 4. SKU Details (Private API)

**GET** `/api/catalog/pvt/stockkeepingunit/{skuId}`

```python
url = f"{base_url}/api/catalog/pvt/stockkeepingunit/{sku_id}"
headers = {
    'X-VTEX-API-AppKey': vtex_appkey,
    'X-VTEX-API-AppToken': vtex_apptoken
}
response = requests.get(url, headers=headers)
```

**Response:**
```json
{
  "Id": 123456,
  "PackagedHeight": 10,
  "PackagedLength": 60,
  "PackagedWidth": 60,
  "PackagedWeightKg": 15.5
}
```

---

### 5. Order Details (Private API)

**GET** `/api/oms/pvt/orders/{orderId}`

```python
url = f"{base_url}/api/oms/pvt/orders/{order_id}"
headers = {
    'X-VTEX-API-AppKey': vtex_appkey,
    'X-VTEX-API-AppToken': vtex_apptoken
}
response = requests.get(url, headers=headers)
```

**Response:**
```json
{
  "orderId": "v123456789-01",
  "status": "payment-approved",
  "value": 10000,
  "items": [...],
  "clientProfileData": {...}
}
```

---

## 🌊 Weni Flow API

### Trigger Flow

**POST** `https://flows.weni.ai/api/v2/flow_starts.json`

```python
url = "https://flows.weni.ai/api/v2/flow_starts.json"
headers = {
    "Authorization": f"Token {weni_token}",
    "Content-Type": "application/json"
}
payload = {
    "flow": weni_flow_id,
    "urns": [user_urn],
    "params": {
        "executions": 1,
        "custom_param": "value"
    }
}
response = requests.post(url, json=payload, headers=headers)
```

**Success Response:** Status 200

---

## 🔐 Secrets Configuration

### Nome das Secrets

```python
# VTEX
BASE_URL = "https://store.vtexcommercestable.com.br"
VTEX_APPKEY = "vtexappkey-store-XXXXXX"
VTEX_APPTOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
STORE_URL = "https://www.store.com.br"

# Weni
WENI_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxx"
WENI_FLOW_ID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Extração

```python
base_url = context.secrets.get("BASE_URL")
vtex_appkey = context.secrets.get("VTEX_APPKEY")
vtex_apptoken = context.secrets.get("VTEX_APPTOKEN")
```

---

## 🛡️ Error Handling Patterns

### HTTP Requests

```python
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print(f"ERROR: Timeout")
    return None
except requests.exceptions.HTTPError as e:
    print(f"ERROR: HTTP {e.response.status_code}")
    return None
except json.JSONDecodeError:
    print(f"ERROR: Invalid JSON")
    return None
```

### Parameter Validation

```python
required_param = context.params.get("required_param")
if not required_param:
    return TextResponse(data={
        "error": "Parâmetro 'required_param' é obrigatório"
    })
```

### Credentials Validation

```python
api_key = context.secrets.get("API_KEY")
if not api_key:
    return TextResponse(data={
        "error": "Configuração incompleta"
    })
```

---

## 📊 Common Patterns

### 1. Extract Price from Cents

```python
price_cents = 8990  # VTEX retorna em centavos
price_reais = price_cents / 100  # 89.90
```

### 2. Control Payload Size

```python
json_data = json.dumps(data)
size_kb = len(json_data.encode('utf-8')) / 1024

if size_kb > 20:
    # Reduzir dados
    pass
```

### 3. Format CEP

```python
cep = "01310-100"
cep_numerico = cep.replace("-", "")  # "01310100"
```

### 4. Check Stock Availability

```python
availability = item.get("availability", "").lower()
quantity = item.get("quantity", 0)

is_available = "available" in availability and quantity > 0
```

### 5. Prevent Multiple Triggers

```python
class MyTool(Tool):
    def __init__(self):
        super().__init__()
        self._weni_flow_triggered = False
    
    def trigger_flow(self):
        if self._weni_flow_triggered:
            return
        # ... trigger logic ...
        self._weni_flow_triggered = True
```

---

## 🧪 Debug Helpers

### Print with Context

```python
print(f"DEBUG: {variable_name}: {value}")
print(f"INFO: Operação concluída - {len(items)} itens")
print(f"WARN: Situação atípica detectada")
print(f"ERROR: Falha crítica: {error_message}")
```

### Type Checking

```python
print(f"Type: {type(data)}, Is list: {isinstance(data, list)}")
```

### JSON Pretty Print

```python
import json
print(json.dumps(data, indent=2, ensure_ascii=False))
```

---

## 📦 Requirements.txt Template

```txt
weni>=1.0.0
requests>=2.28.0
python-dotenv>=0.19.0
```

---

## 🚀 Deployment Checklist

- [ ] Todos os parâmetros obrigatórios validados
- [ ] Secrets configuradas na plataforma
- [ ] Tratamento de erros implementado
- [ ] Logs de debug adequados
- [ ] Payload size controlado (< 20KB)
- [ ] Timeout configurado em requisições
- [ ] Requirements.txt atualizado
- [ ] Testado com dados reais
- [ ] Documentação atualizada

---

## 📚 Links Úteis

- [Estrutura de Projetos](../01-estrutura-projetos.md)
- [Padrões e Boas Práticas](../02-padroes-boas-praticas.md)
- [APIs Detalhadas](../03-apis-integracoes.md)
- [Troubleshooting](troubleshooting.md)
- [Glossário](glossario.md)
