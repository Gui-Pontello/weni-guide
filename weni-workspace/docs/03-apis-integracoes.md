# Guia de APIs e Integrações - Plataforma Weni

## 🔌 Visão Geral

Este guia cobre as principais integrações utilizadas em agentes de IA na Weni, com foco em APIs VTEX e Weni Flows.

## 🛒 Integração VTEX

### Configuração Básica

```python
# Credenciais necessárias (via context.secrets)
BASE_URL = "https://sualoja.vtexcommercestable.com.br"
VTEX_APPKEY = "vtexappkey-sualoja-XXXXXX"
VTEX_APPTOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
STORE_URL = "https://www.sualoja.com.br"

# Headers padrão para APIs VTEX
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-VTEX-API-AppKey': VTEX_APPKEY,
    'X-VTEX-API-AppToken': VTEX_APPTOKEN
}
```

### 1. API de Regionalização

Determina região de entrega baseada no CEP.

**Endpoint:**
```
GET /api/checkout/pub/regions?country=BRA&postalCode={cep}&sc=1
```

**Exemplo de Implementação:**

```python
def get_region_id(self, postal_code, base_url):
    """
    Consulta a API de regionalização para obter o ID da região baseado no CEP
    
    Args:
        postal_code: CEP do cliente (com ou sem hífen)
        base_url: URL base da loja VTEX
        
    Returns:
        tuple: (region_id, error_message, seller_ids)
    """
    region_url = f"{base_url}/api/checkout/pub/regions?country=BRA&postalCode={postal_code}&sc=1"
    
    print(f"DEBUG: Consultando regionalização - URL: {region_url}")
    
    try:
        response = requests.get(region_url)
        print(f"DEBUG: Status: {response.status_code}")
        
        response.raise_for_status()
        regions_data = response.json()
        
        if not regions_data:
            error_msg = "Não atendemos a sua região, mas você pode comprar presencialmente em nossas lojas físicas."
            return None, error_msg, []
        
        region = regions_data[0]
        sellers = region.get("sellers", [])
        
        if not sellers:
            error_msg = "Não atendemos a sua região, mas você pode comprar presencialmente em nossas lojas físicas."
            return None, error_msg, []
        
        region_id = region.get("id")
        seller_ids = [seller.get("id") for seller in sellers]
        
        print(f"INFO: Region ID: {region_id}, Sellers: {seller_ids}")
        return region_id, None, seller_ids
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na regionalização: {e}")
        return None, str(e), []
```

**Resposta Típica:**
```json
[
  {
    "id": "v2.1A2B3C4D",
    "sellers": [
      {"id": "lojaobramax1000"},
      {"id": "lojaobramax1003"}
    ]
  }
]
```

### 2. Intelligent Search API

Busca produtos com filtros e regionalização.

**Endpoint:**
```
GET /api/io/_v/api/intelligent-search/product_search/
```

**Parâmetros Comuns:**
- `query`: Termo de busca
- `hideUnavailableItems`: true/false
- `regionId`: ID da região (opcional)

**Exemplo de Implementação:**

```python
def intelligent_search(self, product_name, url, region_id=None):
    """
    Busca produtos usando Intelligent Search da VTEX
    
    Args:
        product_name: Nome ou termo de busca
        url: URL base da loja
        region_id: ID da região para filtrar por disponibilidade
    
    Returns:
        dict: Produtos encontrados estruturados
    """
    # Monta URL base
    search_url = f"{url}/api/io/_v/api/intelligent-search/product_search/?query={product_name}&hideUnavailableItems=true"
    
    # Adiciona regionalização se disponível
    if region_id:
        search_url += f"&regionId={region_id}"
    
    print(f"DEBUG: Buscando produtos - URL: {search_url}")
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        
        products = data.get("products", [])
        print(f"INFO: {len(products)} produtos encontrados")
        
        # Estrutura os produtos
        structured_products = {}
        
        for product in products:
            product_name_vtex = product.get("productName", "")
            
            # Extrai informações dos SKUs
            items = product.get("items", [])
            variations = []
            
            for item in items:
                sku_data = {
                    "sku_id": item.get("itemId"),
                    "sku_name": item.get("nameComplete"),
                    "imageUrl": item.get("images", [{}])[0].get("imageUrl", ""),
                    "sellers": item.get("sellers", [])
                }
                variations.append(sku_data)
            
            structured_products[product_name_vtex] = {
                "description": product.get("description", ""),
                "brand": product.get("brand", ""),
                "categories": product.get("categories", []),
                "variations": variations
            }
        
        return structured_products
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na busca: {e}")
        return {}
```

### 3. Cart Simulation API

Simula carrinho para verificar estoque, preço e frete.

**Endpoint:**
```
POST /api/checkout/pub/orderForms/simulation
```

**Payload:**
```json
{
  "items": [
    {
      "id": "123456",
      "quantity": 1,
      "seller": "1"
    }
  ],
  "postalCode": "01310100",
  "country": "BRA"
}
```

**Exemplo de Implementação:**

```python
def cart_simulation(self, base_url, sku_id, quantity, postal_code, seller_id):
    """
    Simula carrinho para verificar disponibilidade e preço
    
    Args:
        base_url: URL base VTEX
        sku_id: ID do SKU
        quantity: Quantidade desejada
        postal_code: CEP de entrega
        seller_id: ID do seller
        
    Returns:
        dict: Dados de estoque, preço e frete
    """
    url = f"{base_url}/api/checkout/pub/orderForms/simulation"
    
    payload = {
        "items": [
            {
                "id": str(sku_id),
                "quantity": quantity,
                "seller": str(seller_id)
            }
        ],
        "postalCode": postal_code,
        "country": "BRA"
    }
    
    print(f"DEBUG: Simulando carrinho - SKU: {sku_id}, Qty: {quantity}")
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extrai informações relevantes
        items = data.get("items", [])
        logistics = data.get("logisticsInfo", [])
        
        if not items:
            return None
        
        item = items[0]
        logistic = logistics[0] if logistics else {}
        
        # Valida disponibilidade
        availability = item.get("availability", "")
        quantity_available = item.get("quantity", 0)
        
        if "available" not in availability.lower() or quantity_available == 0:
            print(f"INFO: SKU {sku_id} sem estoque")
            return None
        
        result = {
            "sku_id": sku_id,
            "quantity": quantity_available,
            "price": item.get("price", 0) / 100,  # VTEX retorna em centavos
            "seller_id": item.get("seller", ""),
            "availability": availability,
            "shipping": {
                "slas": logistic.get("slas", [])
            }
        }
        
        print(f"INFO: SKU {sku_id} disponível - Qty: {quantity_available}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Erro na simulação: {e}")
        return None
```

### 4. Catalog API - SKU Details

Busca detalhes técnicos de um SKU (dimensões, peso, etc.).

**Endpoint:**
```
GET /api/catalog/pvt/stockkeepingunit/{skuId}
```

**Requer Autenticação:** Headers com AppKey e AppToken

**Exemplo de Implementação:**

```python
def get_sku_details(self, sku_id, base_url, vtex_appkey, vtex_apptoken):
    """
    Busca informações detalhadas do SKU incluindo dimensões e peso
    
    Args:
        sku_id: ID do SKU
        base_url: URL base VTEX
        vtex_appkey: App Key VTEX
        vtex_apptoken: App Token VTEX
        
    Returns:
        dict: Dimensões e peso do produto
    """
    # Valida credenciais
    if not vtex_appkey or not vtex_apptoken:
        return {
            "PackagedHeight": None,
            "PackagedLength": None,
            "PackagedWidth": None,
            "PackagedWeightKg": None
        }
    
    url = f"{base_url}/api/catalog/pvt/stockkeepingunit/{sku_id}"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': vtex_appkey,
        'X-VTEX-API-AppToken': vtex_apptoken
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"WARN: SKU {sku_id} - Status {response.status_code}")
            return {
                "PackagedHeight": None,
                "PackagedLength": None,
                "PackagedWidth": None,
                "PackagedWeightKg": None
            }
        
        data = response.json()
        
        return {
            "PackagedHeight": data.get('PackagedHeight'),
            "PackagedLength": data.get('PackagedLength'),
            "PackagedWidth": data.get('PackagedWidth'),
            "PackagedWeightKg": data.get('PackagedWeightKg'),
            "Height": data.get('Height'),
            "Length": data.get('Length'),
            "Width": data.get('Width'),
            "WeightKg": data.get('WeightKg')
        }
        
    except Exception as e:
        print(f"ERROR: Erro ao buscar detalhes do SKU {sku_id}: {e}")
        return {
            "PackagedHeight": None,
            "PackagedLength": None,
            "PackagedWidth": None,
            "PackagedWeightKg": None
        }
```

### 5. Order Management API

Consulta status de pedidos.

**Endpoints:**

Por número do pedido:
```
GET /api/oms/pvt/orders/{orderId}
```

Por email:
```
GET /api/oms/pvt/orders?q={email}
```

Por documento (CPF):
```
GET /api/oms/pvt/orders?q={cpf}
```

**Exemplo de Implementação:**

```python
def get_order_by_id(self, order_id, base_url, vtex_appkey, vtex_apptoken):
    """
    Busca pedido por número
    
    Args:
        order_id: Número do pedido
        base_url: URL base VTEX
        vtex_appkey: App Key VTEX
        vtex_apptoken: App Token VTEX
        
    Returns:
        dict: Dados do pedido
    """
    url = f"{base_url}/api/oms/pvt/orders/{order_id}"
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-VTEX-API-AppKey': vtex_appkey,
        'X-VTEX-API-AppToken': vtex_apptoken
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extrai informações relevantes
        order_info = {
            "orderId": data.get("orderId"),
            "status": data.get("status"),
            "statusDescription": data.get("statusDescription"),
            "value": data.get("value", 0) / 100,
            "creationDate": data.get("creationDate"),
            "items": [
                {
                    "name": item.get("name"),
                    "quantity": item.get("quantity"),
                    "price": item.get("price", 0) / 100
                }
                for item in data.get("items", [])
            ],
            "shippingData": {
                "address": data.get("shippingData", {}).get("address", {}),
                "logisticsInfo": data.get("shippingData", {}).get("logisticsInfo", [])
            }
        }
        
        print(f"INFO: Pedido {order_id} encontrado - Status: {order_info['status']}")
        return order_info
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"INFO: Pedido {order_id} não encontrado")
            return None
        print(f"ERROR: Erro ao buscar pedido: {e}")
        return None
```

## 🌊 Integração Weni Flows

### Trigger de Flows

Dispara flows para registrar eventos ou enviar notificações.

**Endpoint:**
```
POST https://flows.weni.ai/api/v2/flow_starts.json
```

**Headers:**
```python
headers = {
    "Authorization": f"Token {WENI_TOKEN}",
    "Content-Type": "application/json"
}
```

**Exemplo de Implementação:**

```python
def trigger_weni_flow(self, context: Context):
    """
    Dispara um flow da Weni
    
    Args:
        context: Contexto da Weni
        
    Returns:
        bool: True se sucesso, False caso contrário
    """
    # Previne múltiplos triggers
    if self._weni_flow_triggered:
        return True
    
    # Extrai configurações
    weni_token = context.secrets.get("WENI_TOKEN")
    weni_flow_id = context.secrets.get("WENI_FLOW_ID")
    user_urn = context.user.get("urn")
    
    if not all([weni_token, weni_flow_id, user_urn]):
        print(f"WARN: Configuração incompleta para trigger de flow")
        return False
    
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
            "event_type": "product_search",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"INFO: Flow disparado com sucesso")
            self._weni_flow_triggered = True
            return True
        else:
            print(f"WARN: Falha ao disparar flow: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: Erro ao disparar flow: {e}")
        return False
```

## 🔑 Resumo de Secrets Necessárias

### Para VTEX:
```
BASE_URL=https://sualoja.vtexcommercestable.com.br
VTEX_APPKEY=vtexappkey-sualoja-XXXXXX
VTEX_APPTOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXX
STORE_URL=https://www.sualoja.com.br
```

### Para Weni Flows:
```
WENI_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
WENI_FLOW_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## 📚 Recursos Adicionais

- [VTEX Developer Portal](https://developers.vtex.com/)
- [Weni Platform Documentation](https://docs.weni.ai/)
- [Estrutura de Projetos](01-estrutura-projetos.md)
- [Padrões e Boas Práticas](02-padroes-boas-praticas.md)
