# 🤖 AI Context - Weni Platform Development

> **Quick context for AI assistants working on this project**

## 🎯 Project Overview

**What:** AI conversational agents on Weni Platform for Obramax (construction e-commerce)  
**Stack:** Python 3.8+, Weni SDK, VTEX APIs, WhatsApp Business  
**Status:** 5 agents in production, 24 docs, complete workspace setup  

---

## 🏗️ Architecture (3 Layers)

```
┌─────────────────────────────────────────┐
│  WhatsApp (User Interface)              │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  Weni Platform (Orchestration)          │
│  - Manager Agent (routes)               │
│  - 5 Specialist Agents (execute)        │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│  External APIs                           │
│  - VTEX (6 APIs): Region, Search,       │
│    Simulation, Catalog, Checkout, OMS   │
│  - Weni Flows (message triggers)        │
│  - Omni (human handoff)                 │
└─────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
weni-workspace/
├── AI-CONTEXT.md              ← YOU ARE HERE
├── .ai/                       ← AI-specific contexts
├── .github/                   ← Copilot instructions
├── .vscode/                   ← Snippets, tasks, setup
├── docs/                      ← 20+ technical docs
│   └── 08-visao-360-projeto-weni-obramax.md  ← MASTER DOC
├── QUICK-REFERENCE.md         ← Commands, APIs, snippets
└── MATRIZ-COMPLETA-ANALISE.md ← 13 Excel sheets explained
```

---

## 🤖 5 Production Agents

| Agent | Purpose | Main Tool | Integration |
|-------|---------|-----------|-------------|
| **Concierge** | Product search | SearchProduct | Region + Intelligent Search APIs |
| **Product Details** | SKU specs | ProductDetails | Catalog API |
| **Checkout** | Cart + shipping | SimulateShipping | Cart Simulation + Checkout APIs |
| **Order Status** | Track orders | GetOrder | Order Management API |
| **Orçamax** | Budget quotes | CustomBudget | Obramax backend |

---

## 📝 Agent Structure (Always Follow)

### YAML Configuration
```yaml
# agent_definition.yaml
agent:
  name: "AgentName"
  version: "1.0.0"
  description: "Brief description"

credentials:
  - name: API_KEY
    description: "API key for..."

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

### Python Tool (Always Follow)
```python
from weni import Tool, Context, TextResponse

class ToolName(Tool):
    def execute(self, context: Context, **kwargs) -> TextResponse:
        # 1. Get credentials
        api_key = context.credentials.get("API_KEY")
        base_url = context.constants.get("BASE_URL")
        
        # 2. Get and validate parameters
        param = kwargs.get("param")
        if not param:
            return TextResponse(
                text="❌ ERROR: param is required",
                should_wait_agent_response=True
            )
        
        # 3. Log
        print(f"[INFO] Processing {param}")
        
        # 4. Try-except for external calls
        try:
            response = requests.get(f"{base_url}/endpoint", timeout=10)
            
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

---

## 🔌 VTEX APIs (Quick Reference)

### 1. Region API (CEP validation)
```python
GET https://{account}.vtexcommercestable.com.br/api/checkout/pub/regions
Params: country=BRA, postalCode=01310100
Returns: {"id": "v2.2AC...", "sellers": [...]}
```

### 2. Intelligent Search (Products)
```python
GET https://{account}.vtexcommercestable.com.br/api/io/_v/api/intelligent-search/product_search
Params: query={term}, regionId={id}, _from=0, _to=2
Returns: {"products": [{id, name, price, link, image}]}
```

### 3. Cart Simulation (Stock + Shipping)
```python
POST https://{account}.vtexcommercestable.com.br/api/checkout/pub/orderForms/simulation
Body: {"items": [{"id": sku, "quantity": 1, "seller": "1"}], "postalCode": "01310100", "country": "BRA"}
Returns: {items, totals, logisticsInfo}
```

### 4. Catalog API (SKU details)
```python
GET https://{account}.vtexcommercestable.com.br/api/catalog_system/pub/products/search?fq=skuId:{sku}
Returns: Full product details
```

### 5. Checkout API (Create cart)
```python
POST https://{account}.vtexcommercestable.com.br/api/checkout/pub/orderForm
Body: {"items": [...]}
Returns: orderFormId, payment link
```

### 6. Order Management (Order status)
```python
GET https://{account}.vtexcommercestable.com.br/api/oms/pvt/orders/{orderId}
Headers: X-VTEX-API-AppKey, X-VTEX-API-AppToken
Returns: Order status, tracking
```

---

## 🔄 Weni Flows Integration

```python
# Trigger flow to send structured message
url = "https://flows.weni.ai/api/v2/flow_starts.json"
token = context.credentials.get("WENI_FLOWS_TOKEN")

payload = {
    "flow": "flow-uuid",
    "urns": ["whatsapp:5511999999999"],
    "extra": {"key": "value"},
    "restart_participants": True
}

response = requests.post(url, json=payload, 
    headers={"Authorization": f"Token {token}"})
```

---

## 🚨 Omni Handoff (Human Transfer)

**When to transfer:**
- User explicitly requests human
- AI cannot resolve after 3 attempts
- Complex issues (refund, credit, cancellation)
- User frustrated/angry

**Standard messages:** 11 templates in Matriz Excel (sheet "Mensagens Omni")

---

## ✅ Code Standards (CRITICAL)

### DO ✅
- Use `context.credentials.get()` for API keys
- Use `context.constants.get()` for URLs
- Always validate inputs before processing
- Use try-except for ALL external calls
- Return `TextResponse` with `should_wait_agent_response=True`
- Log with timestamps: `print(f"[INFO] Message")`
- Use emojis for UX: ✅ ❌ ⚠️ 🔍 📦 🚚 💳
- Set timeout=10 for requests
- Return user-friendly error messages

### DON'T ❌
- Never hardcode credentials
- Never log sensitive data (tokens, CPF, passwords)
- Never return raw exception messages to user
- Don't use blocking operations without timeout
- Don't make assumptions about API responses

---

## 🛠️ Development Workflow

### Local Testing
```bash
# 1. Authenticate
weni login

# 2. Test locally with logs
weni run --verbose

# 3. Deploy to production
weni project push

# 4. View production logs
weni logs --follow
```

### VS Code Setup
- **F5** = Test agent locally with logs
- **Ctrl+Shift+P** → "Run Task" = CLI commands
- **Type `weni-agent` + Tab** = YAML template
- **Type `weni-tool` + Tab** = Python class template
- **Type `vtex-search` + Tab** = VTEX API call

---

## 📚 Documentation Priority

**Read these first (in order):**
1. **This file** (AI-CONTEXT.md) - Overview
2. **QUICK-REFERENCE.md** - Commands, APIs, snippets
3. **docs/08-visao-360-projeto-weni-obramax.md** - Complete 360° reference
4. **.vscode/weni-agent.code-snippets** - Code templates
5. **MATRIZ-COMPLETA-ANALISE.md** - 13 Excel sheets explained

**Reference when needed:**
- docs/00-guia-inicio-rapido.md - Quick start
- docs/02-padroes-boas-praticas.md - Best practices
- docs/03-apis-integracoes.md - API details
- docs/reference/troubleshooting.md - Common issues

---

## 🎯 Common Tasks

### Create New Agent
1. Use snippet: `weni-agent` + Tab
2. Fill fields (name, version, description)
3. Add credentials/constants
4. Write instructions
5. Create tools with `weni-tool` + Tab

### Add VTEX Integration
1. Use snippet: `vtex-region`, `vtex-search`, etc.
2. Get credentials from context
3. Add error handling with `weni-try`
4. Test with `weni run --verbose`

### Implement Omni Handoff
1. Check conditions (3 failures, user request, etc.)
2. Use Weni Flows trigger snippet: `weni-flow`
3. Send template message from Matriz Excel
4. Return success/error to user

---

## 🔍 Troubleshooting Quick Fixes

| Error | Solution |
|-------|----------|
| "Invalid credentials" | Check `context.credentials.get("KEY")` matches YAML |
| "Tool not found" | Verify path: `tools/toolName/main.py` |
| "API 401" | Check credential values in platform |
| "No results" | Add fallback message |
| "Timeout" | Add `timeout=10` and retry logic |

---

## 📊 Key Metrics (KPIs)

- Response time: <2s average
- Success rate: >95%
- Handoff rate: <10%
- User satisfaction: >4.5/5

---

## 🚀 Quick Commands

```bash
# CLI
weni login
weni project list
weni project use <ID>
weni run --verbose
weni project push
weni logs

# Python (use tool instead of terminal)
from weni import Tool, Context, TextResponse

# Snippets (VS Code)
weni-agent      # YAML template
weni-tool       # Python tool
vtex-search     # Product search
weni-flow       # Trigger flow
```

---

## 🔐 Security Checklist

- [ ] No hardcoded credentials
- [ ] No sensitive data in logs
- [ ] Use HTTPS only
- [ ] Validate all inputs
- [ ] Timeout on external calls
- [ ] Sanitize user inputs
- [ ] Use `.gitignore` for `.env`

---

## 💡 Pro Tips

1. **GitHub Copilot knows everything** - Just ask in Copilot Chat (Ctrl+Shift+I)
2. **Use snippets** - Type `weni-` and Tab to see all templates
3. **Test locally first** - Press F5 before deploying
4. **Check logs** - `weni logs --follow` for production debugging
5. **Follow patterns** - Check existing production agents in Obramax folder (if available)

---

## 🎓 Learning Path

**Day 1 (Start Here!):** Follow [QUICK-START.md](QUICK-START.md) → Create first agent in 10 minutes  
**Week 1:** Read this file + QUICK-REFERENCE.md + Study production agents  
**Week 2:** Study docs/08-visao-360 + Implement VTEX integration  
**Week 3:** Add error handling + Weni Flows + Deploy to prod  
**Month 2+:** Optimize performance, add analytics, custom guardrails  

---

## 🤝 Contributing

When making changes:
1. Follow code standards above
2. Test locally with `weni run --verbose`
3. Update documentation if adding features
4. Use semantic commit messages: `feat:`, `fix:`, `docs:`, `refactor:`

---

## 🔗 Important Links

- **Weni CLI Docs:** https://weni-ai.github.io/weni-cli/
- **VTEX Developer:** https://developers.vtex.com/
- **Weni Platform:** https://weni.ai/
- **GitHub Repo:** https://github.com/Gui-Pontello/weni-guide

---

## 📞 Help

- **Stuck?** Read: docs/reference/troubleshooting.md
- **Need examples?** Check: .vscode/weni-agent.code-snippets
- **Full context?** Read: docs/08-visao-360-projeto-weni-obramax.md

---

**Last Updated:** 12/02/2026  
**Version:** 1.0.0  
**Workspace:** weni-workspace
