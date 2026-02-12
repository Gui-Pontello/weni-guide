# Context for Claude - Weni Platform Development

**Attach this file when starting a new conversation with Claude about this project.**

---

## 📋 Project Summary

**Name:** Weni Platform - Obramax AI Agents  
**Type:** Conversational AI agents for e-commerce (construction materials)  
**Stack:** Python 3.8+, Weni SDK, VTEX APIs, WhatsApp Business  
**Status:** 5 production agents, 24 documentation files, complete VS Code workspace  

---

## 🏗️ Architecture Overview

```
WhatsApp User
    ↓
Weni Platform
├── Manager Agent (routes messages)
└── 5 Specialist Agents:
    ├── Concierge (product search + regionalization)
    ├── Product Details (SKU specifications)
    ├── Checkout (cart + shipping calculation)
    ├── Order Status (tracking)
    └── Orçamax (budget quotes)
    ↓
External Systems
├── VTEX (6 APIs: Region, Search, Simulation, Catalog, Checkout, OMS)
├── Weni Flows (message automation)
└── Omni (human handoff system)
```

---

## 📁 Repository Structure

```
weni-workspace/
├── AI-CONTEXT.md              ← Quick context (read first!)
├── .ai/                       ← AI-specific contexts (this file is here)
├── .github/                   ← GitHub Copilot instructions
├── .vscode/                   ← VS Code setup (snippets, tasks)
├── docs/                      ← 20+ documentation files
│   └── 08-visao-360-projeto-weni-obramax.md  ← Master reference
├── QUICK-REFERENCE.md         ← Commands, APIs, snippets
├── MATRIZ-COMPLETA-ANALISE.md ← Excel analysis (13 sheets)
└── Weni_Matriz[...].xlsx      ← Source data
```

---

## 🎯 What You Need to Know

### Agent Structure (Standard Pattern)

**Configuration: agent_definition.yaml**
```yaml
agent:
  name: "AgentName"
  version: "1.0.0"
  description: "What it does"

credentials:
  - name: API_KEY
    description: "..."

constants:
  - name: BASE_URL
    value: "https://..."

instructions: |
  System prompt here

guardrails:
  - type: check_message_limit
    params: {max_messages: 20}

tools:
  - name: ToolName
    path: tools/toolName
```

**Python Tool: tools/toolName/main.py**
```python
from weni import Tool, Context, TextResponse

class ToolName(Tool):
    def execute(self, context: Context, **kwargs) -> TextResponse:
        # 1. Get credentials
        api_key = context.credentials.get("API_KEY")
        
        # 2. Validate inputs
        param = kwargs.get("param")
        if not param:
            return TextResponse(
                text="❌ Error message",
                should_wait_agent_response=True
            )
        
        # 3. API call with error handling
        try:
            response = requests.get(url, timeout=10)
            return TextResponse(
                text=f"✅ Success: {result}",
                should_wait_agent_response=True
            )
        except Exception as e:
            return TextResponse(
                text="❌ User-friendly error",
                should_wait_agent_response=True
            )
```

---

## 🔌 VTEX APIs Reference

### 1. Region API (Validate CEP coverage)
```
GET https://{account}.vtexcommercestable.com.br/api/checkout/pub/regions
Params: country=BRA, postalCode={8-digit CEP}
Returns: {"id": "regionId", "sellers": [...]}
```

### 2. Intelligent Search (Find products)
```
GET https://{account}.vtexcommercestable.com.br/api/io/_v/api/intelligent-search/product_search
Params: query={term}, regionId={id}, _from=0, _to=2
Returns: {"products": [{id, name, price, link, image}]}
```

### 3. Cart Simulation (Check stock + shipping)
```
POST https://{account}.vtexcommercestable.com.br/api/checkout/pub/orderForms/simulation
Body: {
  "items": [{"id": "sku", "quantity": 1, "seller": "1"}],
  "postalCode": "01310100",
  "country": "BRA"
}
Returns: {items, totals, logisticsInfo}
```

### 4. Catalog API (SKU details)
```
GET https://{account}.vtexcommercestable.com.br/api/catalog_system/pub/products/search?fq=skuId:{sku}
```

### 5. Checkout API (Create cart)
```
POST https://{account}.vtexcommercestable.com.br/api/checkout/pub/orderForm
Body: {"items": [...]}
Returns: orderFormId, payment link
```

### 6. Order Management API (Order status)
```
GET https://{account}.vtexcommercestable.com.br/api/oms/pvt/orders/{orderId}
Headers: X-VTEX-API-AppKey, X-VTEX-API-AppToken
```

---

## 🔄 Weni Flows Integration

```python
url = "https://flows.weni.ai/api/v2/flow_starts.json"
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

## ✅ Code Standards (Follow Always)

**DO:**
- ✅ Use `context.credentials` for API keys (NEVER hardcode)
- ✅ Validate ALL inputs before processing
- ✅ Use try-except for external calls
- ✅ Set timeout=10 on all requests
- ✅ Return `TextResponse` with `should_wait_agent_response=True`
- ✅ Log with levels: `[INFO]`, `[WARN]`, `[ERROR]`
- ✅ Use emojis in user messages: ✅ ❌ ⚠️
- ✅ Return user-friendly error messages

**DON'T:**
- ❌ Hardcode credentials or secrets
- ❌ Log sensitive data (tokens, CPF, passwords)
- ❌ Return raw exceptions to users
- ❌ Make requests without timeouts
- ❌ Skip input validation

---

## 🚨 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Invalid credentials" | Check `context.credentials.get()` matches YAML |
| "Tool not found" | Verify class name matches tool name in YAML |
| "API 401" | Check credential values in Weni Platform |
| "Timeout" | Add `timeout=10` and retry logic |
| "No results" | Add fallback message to user |

---

## 📚 Documentation Hierarchy

**Start here (in order):**
1. **QUICK-START.md** - First agent in 10 minutes (HANDS-ON!)
2. **AI-CONTEXT.md** (root) - Quick overview (YOU SHOULD READ THIS)
3. **QUICK-REFERENCE.md** - Commands, APIs, snippets
4. **docs/08-visao-360-projeto-weni-obramax.md** - Complete 360° reference
5. **.vscode/weni-agent.code-snippets** - Code templates
6. **MATRIZ-COMPLETA-ANALISE.md** - 13 Excel sheets explained

**Reference as needed:**
- docs/00-guia-inicio-rapido.md - Quick start guide
- docs/02-padroes-boas-praticas.md - Best practices
- docs/03-apis-integracoes.md - API integration details
- docs/reference/troubleshooting.md - Common problems

---

## 🛠️ Development Workflow

```bash
# 1. Authenticate
weni login

# 2. Test locally (with logs)
weni run --verbose

# 3. Deploy to production
weni project push

# 4. Monitor logs
weni logs --follow
```

---

## 💡 Tips for Working with Claude

1. **Start conversations by asking:** "Have you read AI-CONTEXT.md?"
2. **Reference specific docs:** "According to docs/08-visao-360, how should I...?"
3. **Ask for code generation:** "Generate a tool that searches products using vtex-search pattern"
4. **Request reviews:** "Review this code against the standards in cursor-rules.md"
5. **Troubleshoot:** "This error occurred, check troubleshooting.md and suggest fix"

---

## 🎯 Common Tasks to Ask Claude

### Create New Agent
> "Create a new agent called CustomerSupport that integrates with VTEX Order Management API. Follow the standard pattern in AI-CONTEXT.md."

### Add VTEX Integration
> "Add VTEX Cart Simulation API integration to this tool. Use the pattern from QUICK-REFERENCE.md and include proper error handling."

### Debug Issue
> "I'm getting 'Tool not found' error. Check troubleshooting.md and help me fix it."

### Improve Code
> "Review this code against the standards in cursor-rules.md and suggest improvements."

### Write Documentation
> "Generate documentation for this new tool following the style in docs/02-padroes-boas-praticas.md"

---

## 🔗 External Resources

- **Weni CLI Docs:** https://weni-ai.github.io/weni-cli/
- **VTEX Developer:** https://developers.vtex.com/
- **Weni Platform:** https://weni.ai/

---

## 📊 Project Stats

- **Agents:** 5 in production
- **Documentation:** 24 files (~15,000 lines)
- **APIs:** 7 integrated (6 VTEX + 1 Weni Flows)
- **Templates:** 11+ Omni handoff messages
- **Code Examples:** 2,500+ lines
- **Workspace:** Fully configured VS Code setup

---

## 🎓 Learning Context

If you're helping someone new to the project:
1. **Follow QUICK-START.md step-by-step** (10 minutes, hands-on)
2. Read AI-CONTEXT.md for architecture
3. Work through QUICK-REFERENCE.md
4. Study production agent examples
5. Read docs/08-visao-360 for complete understanding

---

**Last Updated:** 12/02/2026  
**Version:** 1.0.0  
**For:** Claude (Sonnet, Opus, Haiku)  
**Attach:** This file when starting new conversations about this project
