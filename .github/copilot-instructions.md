# GitHub Copilot Instructions - Weni AI Agent Development

## 🎯 Context
This workspace is for developing AI agents on the **Weni Platform** (conversational AI). The main client is **Obramax** (construction e-commerce) with **5 production agents** integrated with **VTEX APIs** and **WhatsApp Business**.

## 📚 Core Documentation
- **Master Doc:** `docs/08-visao-360-projeto-weni-obramax.md` (complete 360° reference)
- **Quick Start:** `docs/00-guia-inicio-rapido.md`
- **CLI Guide:** `docs/04-weni-cli-guia-completo.md`
- **Quick Reference:** `QUICK-REFERENCE.md`
- **Visual Flows:** `DIAGRAMA-FLUXO-COMPLETO.md`

## 🏗️ Project Architecture

### Agent Structure
```
project/
├── agent_definition.yaml   # Main config (name, instructions, tools, guardrails)
└── tools/
    └── toolName/
        ├── main.py         # Tool class (inherits from Tool)
        └── requirements.txt
```

### YAML Template (agent_definition.yaml)
```yaml
agent:
  name: "Agent Name"
  version: "1.0.0"
  description: "Brief description"

credentials:
  - name: API_KEY
    description: "API key description"

constants:
  - name: BASE_URL
    value: "https://api.example.com"

instructions: |
  You are an AI assistant that...
  - Task 1
  - Task 2

guardrails:
  - type: check_message_limit
    params:
      max_messages: 20

tools:
  - name: ToolName
    path: tools/toolName
```

### Python Tool Template (tools/toolName/main.py)
```python
from weni import Tool, Context, TextResponse

class ToolName(Tool):
    def execute(self, context: Context, **kwargs) -> TextResponse:
        """
        Brief description.
        
        Args:
            param1 (str): Description
            param2 (int): Description
            
        Returns:
            TextResponse: Success/error message
        """
        # Get credentials
        api_key = context.credentials.get("API_KEY")
        base_url = context.constants.get("BASE_URL")
        
        # Get parameters from kwargs
        param1 = kwargs.get("param1")
        
        # Validation
        if not param1:
            return TextResponse(
                text="❌ ERROR: param1 is required",
                should_wait_agent_response=True
            )
        
        # Logging
        print(f"[INFO] Processing {param1}")
        
        try:
            # API call
            response = requests.get(
                f"{base_url}/endpoint",
                headers={"Authorization": f"Bearer {api_key}"},
                params={"param": param1}
            )
            
            if response.status_code == 200:
                data = response.json()
                return TextResponse(
                    text=f"✅ Success: {data}",
                    should_wait_agent_response=True
                )
            else:
                return TextResponse(
                    text=f"⚠️ API Error: {response.status_code}",
                    should_wait_agent_response=True
                )
                
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return TextResponse(
                text=f"❌ Error: {str(e)}",
                should_wait_agent_response=True
            )
```

## 🛠️ Weni CLI Commands

### Setup
```bash
pip install weni-cli
weni login                    # Authenticate
weni project list             # List projects
weni project use <PROJECT_ID> # Select project
```

### Development
```bash
weni init                     # Create new agent
weni run --verbose            # Test locally (shows logs)
weni project push             # Deploy to production
weni logs                     # View production logs
```

## 🔌 VTEX API Integration (Obramax)

### 1. Region API (Regionalization)
```python
# Check CEP coverage
GET https://{accountName}.vtexcommercestable.com.br/api/checkout/pub/regions?country={country}&postalCode={cep}

# Response: {"id": "v2.2AC...", "sellers": [{"id": "1", "name": "Seller"}]}
```

### 2. Intelligent Search API
```python
# Product search with region
GET https://{accountName}.vtexcommercestable.com.br/api/io/_v/api/intelligent-search/product_search?query={term}&regionId={regionId}

# Response: products array with id, name, price, image, link
```

### 3. Cart Simulation API
```python
# Stock + shipping calculation
POST https://{accountName}.vtexcommercestable.com.br/api/checkout/pub/orderForms/simulation
Body: {
  "items": [{"id": "sku", "quantity": 1, "seller": "1"}],
  "postalCode": "01310100",
  "country": "BRA"
}
```

### 4. Catalog API
```python
# SKU details
GET https://{accountName}.vtexcommercestable.com.br/api/catalog_system/pub/products/search?fq=skuId:{sku}
```

### 5. Checkout API
```python
# Create cart
POST https://{accountName}.vtexcommercestable.com.br/api/checkout/pub/orderForm
Body: {"items": [{"id": "sku", "quantity": 1, "seller": "1"}]}
```

### 6. Order Management API
```python
# Order status
GET https://{accountName}.vtexcommercestable.com.br/api/oms/pvt/orders/{orderId}
Headers: {"X-VTEX-API-AppKey": key, "X-VTEX-API-AppToken": token}
```

## 🔄 Weni Flows Integration (Message Triggering)

```python
import requests

def trigger_flow(context: Context, flow_uuid: str, contact_urn: str, data: dict):
    """Trigger Weni Flow to send structured message."""
    url = "https://flows.weni.ai/api/v2/flow_starts.json"
    token = context.credentials.get("WENI_FLOWS_TOKEN")
    
    payload = {
        "flow": flow_uuid,
        "urns": [contact_urn],
        "extra": data,
        "restart_participants": True
    }
    
    response = requests.post(
        url,
        json=payload,
        headers={"Authorization": f"Token {token}"}
    )
    
    return response.status_code == 201
```

## 🚨 Omni Handoff (Human Transfer)

### When to Transfer to Human
- User explicitly requests human agent
- AI cannot resolve after 3+ attempts
- Complex issues (refund, credit, cancellation)
- User frustrated or angry

### Template Messages (11 standardized)
1. **Transbordo próximo dia útil** - After hours
2. **Início de atendimento** - Session start
3. **Reagendamento** - Reschedule call
4. **Cupom fiscal** - Invoice request
5. **Solicitação de imagens** - Request photos
6. **Contato sem sucesso** - Callback failed
7. **Crédito** - Credit request
8. **Estorno** - Refund request
9. **Finalização** - Close ticket
10. **Comprovante** - Payment proof
11. **Geral** - General transfer

## 🎯 Best Practices

### Code Quality
- ✅ Always validate user inputs
- ✅ Use try/except for API calls
- ✅ Log with timestamps: `[INFO] Message`
- ✅ Return user-friendly messages (✅, ❌, ⚠️)
- ✅ Set `should_wait_agent_response=True` for agent followup

### Security
- ✅ Never hardcode credentials (use `context.credentials`)
- ✅ Never log sensitive data (tokens, passwords, CPF)
- ✅ Validate all external inputs
- ✅ Use HTTPS only

### Performance
- ✅ Cache repeated API calls when possible
- ✅ Use timeouts: `requests.get(url, timeout=10)`
- ✅ Limit retries: max 3 attempts
- ✅ Return early on errors

### UX
- ✅ Use emojis for clarity (✅❌⚠️🔍📦🚚💳)
- ✅ Provide actionable error messages
- ✅ Offer alternatives when something fails
- ✅ Format currency: R$ 123,45
- ✅ Format dates: 12/02/2026

## 📊 Production Agents (Obramax)

### 1. Concierge (SearchProduct)
- Validates CEP via Region API
- Searches products with Intelligent Search
- Filters by regionId (stock availability)
- Returns top 3 results with price/image/link

### 2. Product Details (ProductDetails)
- Gets SKU details from Catalog API
- Returns dimensions, weight, specifications
- Shows availability by region

### 3. Checkout (SimulateShipping + CreateCart)
- Simulates shipping via Cart Simulation API
- Calculates total (items + shipping)
- Creates cart with Checkout API
- Returns payment link

### 4. Order Status (GetOrder)
- Fetches order by ID via OMS API
- Returns status, tracking, delivery date

### 5. Orçamax (Budget Agent)
- Custom budget generation
- Integration with Obramax backend

## 🧪 Testing Patterns

### Local Testing
```bash
# Test with verbose logging
weni run --verbose

# Check for errors in output
# Test edge cases: empty inputs, invalid CEP, out-of-stock
```

### Common Test Cases
- ✅ Valid input → Success response
- ✅ Invalid input → Clear error message
- ✅ API timeout → Retry logic
- ✅ API 404 → User-friendly message
- ✅ Missing credentials → Helpful error
- ✅ Empty results → Suggest alternatives

## 🎓 Learning Path

### Week 1-2: Basics
- Read `docs/00-guia-inicio-rapido.md`
- Create first agent with `weni init`
- Test locally with `weni run`

### Week 3-4: Integrations
- Study VTEX APIs in `docs/03-apis-integracoes.md`
- Implement SearchProduct tool
- Test with real data

### Month 2: Advanced
- Study production agents in `Obramax/[Atual]...`
- Implement error handling and retries
- Add Weni Flows integration

### Month 3+: Expert
- Optimize performance (caching, parallel calls)
- Implement analytics and KPIs
- Create custom guardrails

## 💡 Code Generation Rules

### When generating agent_definition.yaml:
- Always include: name, version, description, instructions
- Add credentials section for any API keys needed
- Use constants for URLs and configuration
- Include guardrails (message_limit recommended)
- List all tools with correct paths

### When generating Python tools:
- Inherit from `Tool` class
- Implement `execute(self, context: Context, **kwargs)` method
- Add docstring with Args and Returns
- Validate inputs first
- Use try/except for external calls
- Return `TextResponse` with user-friendly text
- Always set `should_wait_agent_response=True` for agent followup
- Log important events with `print(f"[INFO] ...")`

### When generating requirements.txt:
- Include: `requests>=2.31.0`
- Add any specific libraries needed
- Pin major versions for stability

## 🔍 Troubleshooting Quick Reference

### "Invalid credentials"
→ Check `context.credentials.get("KEY_NAME")` matches YAML

### "Tool not found"
→ Verify `tools/toolName/main.py` exists and class name matches

### "API returns 401"
→ Check credential values in Weni Platform dashboard

### "No results found"
→ Add fallback message suggesting alternatives

### "Connection timeout"
→ Add `timeout=10` to requests and implement retry logic

## 📚 Additional Resources

- **Weni CLI Docs:** https://weni-ai.github.io/weni-cli/
- **VTEX Developer:** https://developers.vtex.com/
- **Weni Platform:** https://weni.ai/

---

## 🤖 Copilot Instructions Summary

When helping with Weni agents:
1. **Always** use the templates above for YAML and Python
2. **Always** validate inputs and handle errors gracefully
3. **Always** use `context.credentials` and `context.constants`
4. **Always** return `TextResponse` with clear messages
5. **Follow** the production agent patterns in `Obramax/[Atual]...`
6. **Reference** the master doc when needed: `docs/08-visao-360-projeto-weni-obramax.md`
7. **Use** emojis for better UX (✅❌⚠️)
8. **Log** important events with timestamps
9. **Test** edge cases: empty inputs, timeouts, API errors
10. **Keep** code simple, readable, and well-documented

This workspace contains **23 comprehensive docs**, **5 production agents**, and **2,500+ lines** of example code. Always check existing patterns before implementing from scratch!
