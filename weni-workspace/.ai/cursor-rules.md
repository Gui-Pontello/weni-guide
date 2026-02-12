# Cursor AI Rules - Weni Platform Development

## Project Context

Building AI conversational agents on Weni Platform for Obramax (construction e-commerce).  
Stack: Python 3.8+, Weni SDK, VTEX APIs, WhatsApp Business.

---

## Code Generation Rules

### Python (Weni Tools)

**ALWAYS:**
- Inherit from `Tool` class
- Implement `execute(self, context: Context, **kwargs)` method
- Get credentials with `context.credentials.get("KEY")`
- Validate inputs BEFORE processing
- Use try-except for ALL external API calls
- Return `TextResponse(text="...", should_wait_agent_response=True)`
- Add `timeout=10` to all requests
- Log with `print(f"[INFO] Message")`
- Use emojis in user messages: ✅ ❌ ⚠️

**NEVER:**
- Hardcode credentials or API keys
- Log sensitive data (tokens, passwords, CPF)
- Return raw exceptions to users
- Make requests without timeout
- Skip input validation

### YAML (agent_definition.yaml)

**ALWAYS:**
- Include: agent (name, version, description)
- Add credentials section for API keys
- Add constants for URLs/config values
- Write clear instructions in `instructions` field
- Add guardrails (at least message_limit)
- List tools with correct paths: `tools/toolName`

**STRUCTURE:**
```yaml
agent:
  name: "AgentName"
  version: "1.0.0"
  description: "Description"

credentials:
  - name: API_KEY

constants:
  - name: BASE_URL
    value: "https://..."

instructions: |
  You are...

guardrails:
  - type: check_message_limit

tools:
  - name: ToolName
    path: tools/toolName
```

---

## API Integration Patterns

### VTEX APIs (Use these exact patterns)

**Region API (CEP validation):**
```python
response = requests.get(
    f"https://{account}.vtexcommercestable.com.br/api/checkout/pub/regions",
    params={"country": "BRA", "postalCode": cep},
    timeout=10
)
```

**Intelligent Search (Products):**
```python
response = requests.get(
    f"https://{account}.vtexcommercestable.com.br/api/io/_v/api/intelligent-search/product_search",
    params={"query": term, "regionId": region_id, "_from": 0, "_to": 2},
    timeout=10
)
```

**Cart Simulation:**
```python
response = requests.post(
    f"https://{account}.vtexcommercestable.com.br/api/checkout/pub/orderForms/simulation",
    json={"items": [...], "postalCode": cep, "country": "BRA"},
    timeout=10
)
```

### Weni Flows (Message triggers)

```python
response = requests.post(
    "https://flows.weni.ai/api/v2/flow_starts.json",
    json={
        "flow": "flow-uuid",
        "urns": [contact_urn],
        "extra": data,
        "restart_participants": True
    },
    headers={"Authorization": f"Token {token}"},
    timeout=10
)
```

---

## Error Handling Pattern

**ALWAYS use this structure:**
```python
try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        return TextResponse(
            text=f"✅ Success: {result}",
            should_wait_agent_response=True
        )
    else:
        print(f"[WARN] API returned {response.status_code}")
        return TextResponse(
            text="⚠️ Serviço temporariamente indisponível. Tente novamente.",
            should_wait_agent_response=True
        )
        
except requests.exceptions.Timeout:
    print("[ERROR] Request timeout")
    return TextResponse(
        text="⚠️ Tempo limite excedido. Por favor, tente novamente.",
        should_wait_agent_response=True
    )
except Exception as e:
    print(f"[ERROR] {str(e)}")
    return TextResponse(
        text="❌ Erro ao processar solicitação. Nossa equipe foi notificada.",
        should_wait_agent_response=True
    )
```

---

## Validation Pattern

```python
# Get parameter
param = kwargs.get("param")

# Validate
if not param:
    return TextResponse(
        text="❌ Por favor, informe o parâmetro necessário.",
        should_wait_agent_response=True
    )

# Additional validation (e.g., CEP)
if param_type == "cep":
    import re
    param = re.sub(r'\D', '', str(param))
    if len(param) != 8:
        return TextResponse(
            text="❌ CEP inválido. Digite 8 dígitos.",
            should_wait_agent_response=True
        )
```

---

## Logging Standards

```python
# Use structured logs with levels
print(f"[DEBUG] Loading configuration")
print(f"[INFO] Processing request for {user_id}")
print(f"[WARN] Rate limit approaching: {count}/100")
print(f"[ERROR] API call failed: {error}")
```

---

## User Messages Style

**Guidelines:**
- Use Portuguese (BR) for user-facing messages
- Use emojis for clarity: ✅ ❌ ⚠️ 🔍 📦 🚚 💳
- Be polite and professional
- Provide actionable information
- Format currency: R$ 123,45
- Format dates: 12/02/2026

**Examples:**
```python
# Success
"✅ Produto encontrado! Nome: {name}, Preço: R$ {price:.2f}"

# Error
"❌ Não foi possível processar sua solicitação. Tente novamente."

# Warning
"⚠️ Produto com estoque limitado. {quantity} unidades disponíveis."

# Info
"🔍 Buscando produtos para '{query}'..."
```

---

## File Structure

**New agent structure:**
```
agent_name/
├── agent_definition.yaml
└── tools/
    └── toolName/
        ├── main.py
        └── requirements.txt
```

**Tool file naming:** Always `main.py`  
**Class naming:** Must match tool name in YAML

---

## Testing

**Before committing:**
1. Test locally: `weni run --verbose`
2. Check logs for errors
3. Validate edge cases (empty inputs, timeouts, API errors)
4. Test with real data when possible

---

## Documentation

**When creating new features:**
- Add docstrings to classes and methods
- Update relevant documentation in /docs
- Add examples to QUICK-REFERENCE.md if applicable
- Update AI-CONTEXT.md if changing architecture

---

## Commit Messages

Use semantic commits:
- `feat: Add new SearchProduct tool`
- `fix: Handle timeout in VTEX Region API`
- `docs: Update API integration guide`
- `refactor: Simplify error handling in tools`
- `test: Add validation tests for CEP format`

---

## Priority References

1. **AI-CONTEXT.md** - Quick project overview
2. **QUICK-REFERENCE.md** - Commands and API endpoints
3. **docs/08-visao-360-projeto-weni-obramax.md** - Complete reference
4. **.vscode/weni-agent.code-snippets** - Code templates

---

## Common Patterns

### CEP Formatting
```python
import re
cep = re.sub(r'\D', '', str(cep))
if len(cep) != 8:
    # error
```

### Currency Formatting
```python
price = value / 100  # VTEX returns cents
formatted = f"R$ {price:.2f}"
```

### Retry Logic
```python
max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.get(url, timeout=10)
        break
    except requests.exceptions.Timeout:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)
```

---

## Security Checklist

Every tool MUST:
- [ ] Use context.credentials for API keys
- [ ] Validate ALL user inputs
- [ ] Not log sensitive data
- [ ] Use HTTPS only
- [ ] Set request timeouts
- [ ] Handle errors gracefully
- [ ] Return user-friendly messages

---

## Performance

**Optimize:**
- Set appropriate timeouts (10s default)
- Limit API results (_to=2 for search)
- Cache when applicable
- Use async for parallel calls (if needed)

**Avoid:**
- Blocking operations
- Infinite loops
- Large payload responses
- Unnecessary API calls

---

**Last Updated:** 12/02/2026  
**For:** Cursor AI v0.40+
