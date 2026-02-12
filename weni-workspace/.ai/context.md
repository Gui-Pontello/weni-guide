# General AI Context - Weni Platform Project

> **For:** Any AI assistant (ChatGPT, Claude, Gemini, etc.)  
> **Use:** Copy/paste this when starting conversations about the project

---

## Project Summary

**Weni Platform** - AI Conversational Agents for Obramax  
Building WhatsApp chatbots for e-commerce (construction materials)

- **Stack:** Python 3.8+, Weni SDK, VTEX APIs
- **Status:** 5 production agents, 24 documentation files
- **Scale:** ~2,500 lines of code, 7 API integrations

---

## Quick Architecture

```
User (WhatsApp) 
    ↓
Weni Platform (Python agents)
    ↓
External APIs (VTEX, Weni Flows, Omni)
```

**5 Production Agents:**
1. Concierge - Product search + regionalization
2. Product Details - SKU specifications
3. Checkout - Cart + shipping
4. Order Status - Tracking
5. Orçamax - Budget quotes

---

## Key Technologies

- **Weni SDK:** Agent framework (Tool, Context, TextResponse)
- **VTEX APIs:** 6 APIs (Region, Search, Simulation, Catalog, Checkout, OMS)
- **Weni Flows:** Message automation/triggers
- **Omni:** Human handoff system

---

## Code Pattern (Standard)

### Agent Structure
```
agent_definition.yaml ← Configuration
tools/
  └── toolName/
      └── main.py ← Python logic
```

### Python Tool Template
```python
from weni import Tool, Context, TextResponse

class ToolName(Tool):
    def execute(self, context: Context, **kwargs):
        # Get credentials
        api_key = context.credentials.get("API_KEY")
        
        # Validate input
        param = kwargs.get("param")
        if not param:
            return TextResponse(
                text="❌ Error message",
                should_wait_agent_response=True
            )
        
        # API call + error handling
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

## Important Rules

**ALWAYS:**
- Use `context.credentials` (never hardcode)
- Validate ALL inputs
- Add timeout=10 to requests
- Return TextResponse with should_wait_agent_response=True
- Use try-except for external calls
- Log with `print(f"[INFO] message")`

**NEVER:**
- Hardcode credentials/secrets
- Log sensitive data
- Return raw exceptions to users

---

## Key Files to Reference

1. **AI-CONTEXT.md** - Detailed project context
2. **QUICK-REFERENCE.md** - Commands, APIs, snippets
3. **docs/08-visao-360-projeto-weni-obramax.md** - Complete reference
4. **cursor-rules.md** - Coding standards
5. **MATRIZ-COMPLETA-ANALISE.md** - Excel data (13 sheets)

---

## Common Commands

```bash
weni login                  # Authenticate
weni run --verbose          # Test locally
weni project push           # Deploy
weni logs --follow          # Monitor
```

---

## API Quick Reference

**VTEX Region (CEP validation):**
```
GET /api/checkout/pub/regions?country=BRA&postalCode={cep}
```

**VTEX Search (Products):**
```
GET /api/io/_v/api/intelligent-search/product_search?query={term}&regionId={id}
```

**Cart Simulation:**
```
POST /api/checkout/pub/orderForms/simulation
Body: {items, postalCode, country}
```

**Weni Flows (Trigger message):**
```
POST https://flows.weni.ai/api/v2/flow_starts.json
Headers: Authorization: Token {token}
Body: {flow, urns, extra}
```

---

## Documentation Structure

```
weni-workspace/
├── AI-CONTEXT.md          ← START HERE
├── .ai/                   ← AI-specific contexts
├── docs/                  ← 20+ docs
├── QUICK-REFERENCE.md     ← Commands/APIs
└── .vscode/               ← Code snippets
```

---

## How to Get Help

1. **Quick question:** Check AI-CONTEXT.md
2. **API integration:** Check QUICK-REFERENCE.md
3. **Complete reference:** Read docs/08-visao-360-projeto-weni-obramax.md
4. **Code examples:** Check .vscode/weni-agent.code-snippets
5. **Troubleshooting:** Check docs/reference/troubleshooting.md

---

## Asking Better Questions

**Good prompts:**
- "Create a tool that searches products using VTEX Search API following the pattern in AI-CONTEXT.md"
- "Review this code against standards in cursor-rules.md"
- "Debug this error using troubleshooting.md"

**Include context:**
- Mention relevant files
- Paste error messages
- Show what you've tried

---

## Project Stats

- 📄 24 documentation files
- 🤖 5 production agents
- 🔌 7 API integrations
- 💬 11+ message templates
- 📊 13 Excel data sheets
- 💻 ~2,500 lines of code

---

## Next Steps

1. **NEW TO WENI?** Start with **QUICK-START.md** (10 min hands-on)
2. Read **AI-CONTEXT.md** for detailed overview
3. Check **QUICK-REFERENCE.md** for quick lookups
4. Study production agents in workspace
5. Use snippets in .vscode/weni-agent.code-snippets
6. Follow patterns in cursor-rules.md

---

**Quick Links:**
- Full context: AI-CONTEXT.md
- Commands: QUICK-REFERENCE.md
- Master doc: docs/08-visao-360-projeto-weni-obramax.md
- Code templates: .vscode/weni-agent.code-snippets

---

**Last Updated:** 12/02/2026  
**Version:** 1.0.0  
**Repository:** https://github.com/Gui-Pontello/weni-guide
