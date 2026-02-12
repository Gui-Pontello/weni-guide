# Exemplo Completo: Projeto Agente E-commerce com Weni CLI

## 📋 Visão Geral

Este é um exemplo completo de um projeto de agente de IA para e-commerce, mostrando:
- ✅ Estrutura de pastas organizada
- ✅ Arquivo YAML de definição do agente
- ✅ Múltiplas tools integradas
- ✅ Credenciais e constantes configuradas
- ✅ Testes automatizados
- ✅ Deploy via Weni CLI

## 🏗️ Estrutura do Projeto

```
ecommerce-agent/
├── agent_definition.yaml           # Definição do agente
├── README.md                       # Documentação do projeto
├── .gitignore                      # Arquivos ignorados
└── tools/                          # Todas as tools do agente
    ├── buscar_produtos/
    │   ├── main.py
    │   └── test_definition.yaml
    ├── consultar_estoque/
    │   ├── main.py
    │   └── test_definition.yaml
    └── status_pedido/
        ├── main.py
        └── test_definition.yaml
```

---

## 📄 agent_definition.yaml

```yaml
agents:
  ecommerce_agent:
    # Informações básicas
    name: "Assistente Virtual E-commerce"
    description: "Agente especializado em atendimento ao cliente de e-commerce, capaz de buscar produtos, consultar estoque e verificar status de pedidos."
    
    # Credenciais necessárias
    credentials:
      vtex_appkey:
        label: "VTEX App Key"
        placeholder: "vtexappkey-store-XXXXXX"
      
      vtex_apptoken:
        label: "VTEX App Token"
        placeholder: "XXXXXXXXXXXXXXXXXXXXXXXXXX"
      
      base_url:
        label: "VTEX Base URL"
        placeholder: "https://store.vtexcommercestable.com.br"
      
      store_url:
        label: "Store URL"
        placeholder: "https://www.store.com.br"
    
    # Constantes configuráveis
    constants:
      max_products:
        label: "Máximo de Produtos na Resposta"
        value: 10
      
      timeout_seconds:
        label: "Timeout de Requisições (segundos)"
        value: 30
      
      max_payload_kb:
        label: "Tamanho Máximo do Payload (KB)"
        value: 20
    
    # Instruções para o agente
    instructions:
      - "Você é um assistente virtual especializado em e-commerce"
      - "Seu objetivo é ajudar clientes a encontrar produtos, verificar disponibilidade e acompanhar pedidos"
      - "Sempre seja cordial, objetivo e prestativo"
      - "Quando buscar produtos, considere a região do cliente para verificar disponibilidade"
      - "Se um produto não estiver disponível, sugira alternativas similares"
      - "Para consultas de pedidos, solicite o número do pedido ou email do cliente"
    
    # Guardrails (limites e restrições)
    guardrails:
      - "Não discuta política, religião ou qualquer tópico sensível"
      - "Não forneça informações pessoais de outros clientes"
      - "Não prometa descontos ou promoções sem autorização"
      - "Não execute ações que modifiquem pedidos sem confirmação explícita do cliente"
      - "Mantenha o foco em produtos e serviços da loja"
    
    # Tools disponíveis
    tools:
      # Tool 1: Buscar Produtos
      - buscar_produtos:
          name: "Buscar Produtos"
          source:
            path: "tools/buscar_produtos"
            entrypoint: "main.BuscarProdutos"
            path_test: "test_definition.yaml"
          description: "Busca produtos no catálogo considerando regionalização por CEP e disponibilidade em estoque"
          parameters:
            - product_name:
                description: "Nome ou termo de busca do produto"
                type: "string"
                required: true
                contact_field: false
            
            - postal_code:
                description: "CEP do cliente para verificar disponibilidade regional"
                type: "string"
                required: true
                contact_field: true
            
            - brand_name:
                description: "Marca específica do produto (opcional)"
                type: "string"
                required: false
                contact_field: false
            
            - quantity:
                description: "Quantidade desejada (padrão: 1)"
                type: "integer"
                required: false
                contact_field: false
      
      # Tool 2: Consultar Estoque
      - consultar_estoque:
          name: "Consultar Estoque"
          source:
            path: "tools/consultar_estoque"
            entrypoint: "main.ConsultarEstoque"
            path_test: "test_definition.yaml"
          description: "Verifica disponibilidade em estoque de um produto específico por SKU"
          parameters:
            - sku_id:
                description: "ID do SKU do produto"
                type: "string"
                required: true
                contact_field: false
            
            - postal_code:
                description: "CEP para verificar disponibilidade regional"
                type: "string"
                required: true
                contact_field: true
            
            - quantity:
                description: "Quantidade desejada"
                type: "integer"
                required: false
                contact_field: false
      
      # Tool 3: Status do Pedido
      - status_pedido:
          name: "Consultar Status de Pedido"
          source:
            path: "tools/status_pedido"
            entrypoint: "main.StatusPedido"
            path_test: "test_definition.yaml"
          description: "Consulta o status e detalhes de um pedido existente"
          parameters:
            - order_id:
                description: "Número do pedido (ex: v123456789-01)"
                type: "string"
                required: false
                contact_field: false
            
            - email:
                description: "Email do cliente (busca últimos pedidos)"
                type: "string"
                required: false
                contact_field: true
```

---

## 🔧 Tool 1: Buscar Produtos

### tools/buscar_produtos/main.py

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests
import json

class BuscarProdutos(Tool):
    def execute(self, context: Context) -> TextResponse:
        # Extrair parâmetros
        product_name = context.parameters.get("product_name")
        postal_code = context.parameters.get("postal_code")
        brand_name = context.parameters.get("brand_name")
        quantity = int(context.parameters.get("quantity", 1))
        
        # Validar obrigatórios
        if not product_name or not postal_code:
            return TextResponse(data={
                "error": "Parâmetros 'product_name' e 'postal_code' são obrigatórios"
            })
        
        # Extrair credenciais
        base_url = context.credentials.get("base_url")
        store_url = context.credentials.get("store_url")
        vtex_appkey = context.credentials.get("vtex_appkey")
        vtex_apptoken = context.credentials.get("vtex_apptoken")
        
        # Extrair constantes
        max_products = int(context.constants.get("max_products", 10))
        timeout = int(context.constants.get("timeout_seconds", 30))
        
        print(f"INFO: Buscando '{product_name}' para CEP {postal_code}")
        
        # 1. Consultar regionalização
        region_id, sellers = self.get_region(postal_code, base_url)
        
        if not region_id:
            return TextResponse(data={
                "message": "Não atendemos sua região, mas você pode visitar nossas lojas físicas."
            })
        
        print(f"INFO: Região: {region_id}, Sellers: {sellers}")
        
        # 2. Buscar produtos
        products = self.search_products(
            product_name, brand_name, store_url, region_id, timeout
        )
        
        if not products:
            return TextResponse(data={
                "message": f"Nenhum produto encontrado para '{product_name}'"
            })
        
        print(f"INFO: {len(products)} produtos encontrados")
        
        # 3. Validar estoque
        available_products = self.check_stock(
            base_url, products, sellers, quantity, postal_code, timeout
        )
        
        # 4. Limitar quantidade
        final_products = available_products[:max_products]
        
        print(f"INFO: Retornando {len(final_products)} produtos com estoque")
        
        return TextResponse(data={"products": final_products})
    
    def get_region(self, postal_code, base_url):
        """Consulta API de regionalização"""
        url = f"{base_url}/api/checkout/pub/regions?country=BRA&postalCode={postal_code}&sc=1"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None, []
            
            region = data[0]
            region_id = region.get("id")
            sellers = [s.get("id") for s in region.get("sellers", [])]
            
            return region_id, sellers
        
        except Exception as e:
            print(f"ERROR: Regionalização falhou: {e}")
            return None, []
    
    def search_products(self, product_name, brand_name, url, region_id, timeout):
        """Busca produtos via Intelligent Search"""
        search_url = f"{url}/api/io/_v/api/intelligent-search/product_search/"
        params = {
            "query": product_name,
            "hideUnavailableItems": "true",
            "regionId": region_id
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            products = []
            for product in data.get("products", []):
                # Filtrar por marca se especificada
                if brand_name and product.get("brand", "").lower() != brand_name.lower():
                    continue
                
                for item in product.get("items", []):
                    products.append({
                        "sku_id": item.get("itemId"),
                        "name": item.get("nameComplete"),
                        "brand": product.get("brand"),
                        "image": item.get("images", [{}])[0].get("imageUrl", "")
                    })
            
            return products
        
        except Exception as e:
            print(f"ERROR: Busca falhou: {e}")
            return []
    
    def check_stock(self, base_url, products, sellers, quantity, postal_code, timeout):
        """Valida estoque via cart simulation"""
        available = []
        
        for product in products:
            sku_id = product["sku_id"]
            
            for seller_id in sellers:
                payload = {
                    "items": [{"id": str(sku_id), "quantity": quantity, "seller": str(seller_id)}],
                    "postalCode": postal_code,
                    "country": "BRA"
                }
                
                try:
                    url = f"{base_url}/api/checkout/pub/orderForms/simulation"
                    response = requests.post(url, json=payload, timeout=timeout)
                    response.raise_for_status()
                    data = response.json()
                    
                    items = data.get("items", [])
                    if items:
                        item = items[0]
                        if "available" in item.get("availability", "").lower():
                            product_with_stock = product.copy()
                            product_with_stock["quantity"] = item.get("quantity", 0)
                            product_with_stock["price"] = item.get("price", 0) / 100
                            product_with_stock["seller_id"] = seller_id
                            available.append(product_with_stock)
                            break
                
                except Exception as e:
                    print(f"WARN: Simulação falhou para SKU {sku_id}: {e}")
                    continue
        
        return available
```

### tools/buscar_produtos/test_definition.yaml

```yaml
tests:
  - name: "Busca de cimento com CEP válido"
    parameters:
      product_name: "cimento"
      postal_code: "01310-100"
    expected_output:
      products:
        - sku_id: "any"
          name: "any"
          quantity: ">=1"
  
  - name: "Busca com marca específica"
    parameters:
      product_name: "porcelanato"
      postal_code: "01310-100"
      brand_name: "Portobello"
    expected_output:
      products:
        - brand: "Portobello"
  
  - name: "CEP não atendido"
    parameters:
      product_name: "cimento"
      postal_code: "99999-999"
    expected_output:
      message: "Não atendemos sua região"
```

---

## 🚀 Como Usar

### 1. Instalar Weni CLI

```bash
pip install weni-cli
```

### 2. Autenticar

```bash
weni login
```

### 3. Selecionar Projeto

```bash
weni project list
weni project use <project_uuid>
```

### 4. Testar Localmente

```bash
# Testar tool de busca de produtos
weni run agent_definition.yaml ecommerce_agent buscar_produtos

# Modo verbose
weni run agent_definition.yaml ecommerce_agent buscar_produtos -v
```

### 5. Deploy

```bash
# Deploy inicial
weni project push agent_definition.yaml

# Atualizar agente existente
weni project push agent_definition.yaml --force-update
```

### 6. Monitorar Logs

```bash
# Ver logs da tool de busca
weni logs --agent ecommerce_agent --tool buscar_produtos

# Filtrar por período
weni logs \
  --agent ecommerce_agent \
  --tool buscar_produtos \
  --start-time 2024-01-01T00:00:00 \
  --end-time 2024-01-31T23:59:59
```

---

## 📝 Configuração de Credenciais

Após o deploy, configure as credenciais na UI da Weni Platform:

1. Acesse seu projeto na plataforma
2. Vá em Configurações → Credentials
3. Preencha:
   - **vtex_appkey**: Sua App Key VTEX
   - **vtex_apptoken**: Seu App Token VTEX
   - **base_url**: URL base VTEX (ex: https://store.vtexcommercestable.com.br)
   - **store_url**: URL pública da loja (ex: https://www.store.com.br)

---

## ✅ Checklist de Deploy

- [ ] Todas as tools implementadas
- [ ] Testes criados e passando
- [ ] Credenciais definidas no YAML
- [ ] Constantes configuradas
- [ ] Instructions e guardrails adequados
- [ ] README.md documentado
- [ ] .gitignore configurado
- [ ] Testado localmente com `weni run`
- [ ] Deploy realizado com `weni project push`
- [ ] Credenciais configuradas na plataforma
- [ ] Logs monitorados após deploy

---

## 🎓 Próximos Passos

1. **Adicionar mais tools:**
   - Calcular frete
   - Aplicar cupons
   - Gerar carrinho de compras

2. **Melhorias:**
   - Cache de consultas frequentes
   - Retry automático em falhas
   - Métricas de performance

3. **Testes:**
   - Testes de integração
   - Testes de carga
   - Validação de todos os cenários

---

## 📚 Recursos Relacionados

- [Weni CLI - Guia Completo](../04-weni-cli-guia-completo.md)
- [Estrutura de Projetos](../01-estrutura-projetos.md)
- [APIs VTEX](../03-apis-integracoes.md)
- [Troubleshooting](../reference/troubleshooting.md)
