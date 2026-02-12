# Padrões e Boas Práticas - Desenvolvimento de Agentes de IA na Weni

## 🎯 Princípios Fundamentais

### 1. Sempre Validar Entradas

```python
def run(self, context: Context):
    # ❌ EVITE: Assumir que parâmetros existem
    # product_name = context.params["product_name"]
    
    # ✅ CORRETO: Validar antes de usar
    product_name = context.params.get("product_name")
    if not product_name:
        return TextResponse(data={
            "error": "Parâmetro 'product_name' é obrigatório"
        })
```

### 2. Tratar Erros Adequadamente

```python
try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"ERROR: Erro na requisição: {e}")
    return TextResponse(data={"error": f"Falha ao consultar API: {str(e)}"})
except json.JSONDecodeError as e:
    print(f"ERROR: Erro ao processar JSON: {e}")
    return TextResponse(data={"error": "Resposta da API inválida"})
```

### 3. Usar Logging Estratégico

```python
# Início de operações importantes
print(f"DEBUG: Iniciando busca de produtos - Termo: '{product_name}', CEP: {postal_code}")

# Pontos de decisão
if is_priority_category:
    print(f"DEBUG: Produto identificado como categoria prioritária")

# Resultados de operações
print(f"INFO: {len(products)} produtos encontrados com estoque")

# Alertas
print(f"WARN: Payload excedeu 20KB, removendo produtos extras")

# Erros
print(f"ERROR: Falha ao consultar API de regionalização: {error}")
```

## 🔄 Padrões de Integração com APIs

### Estrutura de Requisição HTTP

```python
def consultar_api(self, url, headers=None, params=None):
    """
    Template padrão para requisições HTTP
    """
    try:
        print(f"DEBUG: Consultando URL: {url}")
        
        response = requests.get(url, headers=headers, params=params)
        print(f"DEBUG: Status code: {response.status_code}")
        
        # Verifica status antes de processar
        if response.status_code != 200:
            print(f"WARN: Status não-200 recebido: {response.status_code}")
            return None
        
        response.raise_for_status()
        data = response.json()
        
        print(f"INFO: Dados recebidos com sucesso")
        return data
        
    except requests.exceptions.Timeout:
        print(f"ERROR: Timeout na requisição")
        return None
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na requisição: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Erro ao decodificar JSON: {e}")
        return None
```

### Headers Padrão VTEX

```python
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-VTEX-API-AppKey': vtex_appkey,
    'X-VTEX-API-AppToken': vtex_apptoken
}
```

## 🎨 Padrões de Resposta

### Estrutura de Dados Consistente

```python
# ✅ BOA PRÁTICA: Estrutura clara e organizada
{
    "products": [
        {
            "sku_id": "123",
            "sku_name": "Produto A",
            "price": 100.00,
            "stock": 10,
            "imageUrl": "https://...",
            "specifications": {...}
        }
    ],
    "metadata": {
        "total_found": 5,
        "region_id": "v2.1234"
    }
}

# ❌ EVITE: Dados não estruturados ou inconsistentes
{
    "product_123": {...},
    "product_456": {...},
    "info": "texto solto"
}
```

### Mensagens de Erro User-Friendly

```python
# ✅ BOA PRÁTICA: Mensagem clara para o usuário
if not regions_data:
    return TextResponse(data={
        "error": "Não atendemos sua região",
        "message": "Informe ao cliente que não atendemos a sua região, mas o cliente pode comprar presencialmente em nossas lojas físicas."
    })

# ❌ EVITE: Mensagens técnicas expostas ao usuário
return TextResponse(data={"error": "NoneType object has no attribute 'get'"})
```

## 🔍 Otimização de Performance

### 1. Controle de Tamanho de Payload

```python
# Limite de 20KB para respostas
def controlar_tamanho_payload(self, produtos):
    """
    Garante que o payload não exceda o limite
    """
    json_data = json.dumps(produtos)
    size_kb = len(json_data.encode('utf-8')) / 1024
    
    print(f"INFO: Tamanho inicial do payload: {size_kb:.2f} KB")
    
    if size_kb > 20:
        print(f"WARN: Payload excede 20KB, reduzindo...")
        while size_kb > 20 and produtos:
            produtos.pop()
            json_data = json.dumps(produtos)
            size_kb = len(json_data.encode('utf-8')) / 1024
        
        print(f"INFO: Tamanho final: {size_kb:.2f} KB, {len(produtos)} itens")
    
    return produtos
```

### 2. Evitar Requisições Desnecessárias

```python
# ✅ BOA PRÁTICA: Verificar condições antes de fazer requisições
if not vtex_appkey or not vtex_apptoken:
    # Retorna valores padrão sem fazer requisição
    return {"stock": None, "price": None}

response = self.consultar_api(url, headers)
```

### 3. Reutilizar Conexões

```python
# Para múltiplas requisições, considere usar Session
session = requests.Session()
session.headers.update(headers)

for produto in produtos:
    response = session.get(f"{base_url}/produto/{produto['id']}")
```

## 🛡️ Segurança e Credenciais

### Nunca Hardcode Credenciais

```python
# ❌ NUNCA FAÇA ISSO
api_key = "abc123xyz"
base_url = "https://api.exemplo.com"

# ✅ SEMPRE USE SECRETS
api_key = context.secrets.get("API_KEY")
base_url = context.secrets.get("BASE_URL")

if not api_key or not base_url:
    return TextResponse(data={"error": "Configuração incompleta"})
```

### Sanitização de Dados de Log

```python
# ✅ BOA PRÁTICA: Não logue dados sensíveis
print(f"DEBUG: Autenticando com usuário: {username}")
print(f"DEBUG: Token presente: {bool(api_token)}")

# ❌ EVITE: Expor credenciais em logs
print(f"DEBUG: API Token: {api_token}")  # NÃO FAÇA ISSO!
```

## 🔄 Integração com Flows da Weni

### Trigger de Flows

```python
def trigger_weni_flow(self, context: Context):
    """
    Dispara um flow da Weni para registrar evento ou notificação
    """
    # Previne múltiplos triggers
    if self._weni_flow_triggered:
        return
    
    weni_token = context.secrets.get("WENI_TOKEN")
    weni_flow_id = context.secrets.get("WENI_FLOW_ID")
    user_urn = context.user.get("urn")
    
    if not all([weni_token, weni_flow_id, user_urn]):
        print(f"WARN: Configuração incompleta para trigger de flow")
        return
    
    url = "https://flows.weni.ai/api/v2/flow_starts.json"
    
    headers = {
        "Authorization": f"Token {weni_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "flow": weni_flow_id,
        "urns": [user_urn],
        "params": {
            "event": "product_search",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"INFO: Flow disparado com sucesso")
            self._weni_flow_triggered = True
        else:
            print(f"WARN: Falha ao disparar flow: {response.status_code}")
    except Exception as e:
        print(f"ERROR: Erro ao disparar flow: {e}")
```

## 📊 Padrões de Dados

### Formatação de Preços

```python
# ✅ BOA PRÁTICA: Retorne valores numéricos
"price": 149.99,
"spotPrice": 134.99

# ❌ EVITE: Strings formatadas que dificultam processamento
"price": "R$ 149,99"
```

### Datas e Timestamps

```python
from datetime import datetime

# ✅ BOA PRÁTICA: ISO 8601
"created_at": datetime.now().isoformat()
# Resultado: "2026-02-11T10:30:00.123456"

# Para timestamps Unix
"timestamp": int(datetime.now().timestamp())
```

## 🧪 Testabilidade

### Separar Lógica de Negócio

```python
# ✅ BOA PRÁTICA: Métodos testáveis independentemente
def validar_cep(self, cep):
    """Valida formato de CEP brasileiro"""
    import re
    pattern = r'^\d{5}-?\d{3}$'
    return bool(re.match(pattern, cep))

def consultar_regiao(self, cep, base_url):
    """Consulta região por CEP"""
    if not self.validar_cep(cep):
        return None, "CEP inválido"
    # ... resto da lógica
```

## 🎓 Regras de Negócio Específicas

### Regionalização e Sellers

```python
def aplicar_regras_regionais(self, region_id, sellers, category):
    """
    Aplica regras específicas baseadas em região e categoria
    
    Exemplo: Mooca tem sellers diferentes para Retirada vs Entrega
    em categorias prioritárias (pisos e porcelanatos)
    """
    if not sellers:
        return sellers
    
    # Identifica sellers da região Mooca
    mooca_sellers = ["lojaobramax1000", "lojaobramax1003", "lojaobramax1500"]
    is_mooca = all(s in mooca_sellers for s in sellers)
    
    if is_mooca and self.is_priority_category(category):
        # Regras específicas da Mooca para categorias prioritárias
        # (requer deliverytype)
        pass
    
    return sellers
```

### Priorização de Estoque

```python
def priorizar_por_estoque(self, produtos, is_priority_category):
    """
    Para categorias prioritárias (pisos, porcelanatos),
    ordena por maior quantidade disponível
    """
    if is_priority_category:
        produtos.sort(
            key=lambda x: x.get("quantity", 0),
            reverse=True
        )
    return produtos
```

## ✅ Checklist de Boas Práticas

- [ ] Validação de todos os parâmetros obrigatórios
- [ ] Tratamento de exceções em requisições HTTP
- [ ] Logs em pontos críticos (DEBUG, INFO, WARN, ERROR)
- [ ] Credenciais via `context.secrets`, nunca hardcoded
- [ ] Respostas estruturadas e consistentes
- [ ] Mensagens de erro user-friendly
- [ ] Controle de tamanho de payload (< 20KB)
- [ ] Prevenir múltiplos triggers de flows
- [ ] Sanitização de dados sensíveis em logs
- [ ] Métodos auxiliares com responsabilidade única
- [ ] Documentação inline (docstrings)
- [ ] Formatação consistente de dados (preços, datas)

## 📚 Recursos Adicionais

- [Estrutura de Projetos](01-estrutura-projetos.md)
- [APIs e Integrações](03-apis-integracoes.md)
- [Exemplos Práticos](../exemplos/)
