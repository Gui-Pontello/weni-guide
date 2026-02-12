# Ready-to-Use Prompts for Common Tasks

> Copy these prompts and adjust variables as needed.

---

## 🤖 Agent Creation

### Create New Agent from Scratch
```
Create a new Weni agent called {AgentName} that {purpose}.

Requirements:
- Follow the standard pattern in AI-CONTEXT.md
- Include proper agent_definition.yaml with credentials and constants
- Create main tool in tools/{toolName}/main.py
- Integrate with {API_NAME} API
- Include error handling and input validation
- Add logging and user-friendly messages

Reference: QUICK-REFERENCE.md for API patterns
```

### Clone Existing Agent Structure
```
Create a new agent similar to the Concierge agent but for {new_purpose}.

Modify:
- Replace product search with {new_functionality}
- Change API integration from {old_api} to {new_api}
- Adjust instructions to handle {use_case}

Keep the same error handling and validation patterns.
```

---

## 🔌 API Integration

### Add VTEX Region API
```
Add VTEX Region API integration to validate CEP.

Requirements:
- Use the pattern from QUICK-REFERENCE.md
- Validate CEP format (8 digits)
- Handle API errors gracefully
- Return user-friendly error messages
- Cache region_id for subsequent calls

Endpoint: GET https://{account}.vtexcommercestable.com.br/api/checkout/pub/regions
Params: country=BRA, postalCode={cep}
```

### Add VTEX Intelligent Search
```
Implement product search using VTEX Intelligent Search API.

Requirements:
- Use vtex-search pattern from snippets
- Filter by regionId (regional stock)
- Limit results to top 3 products
- Format response with: name, price, link, image
- Handle empty results with helpful message

Endpoint: /api/io/_v/api/intelligent-search/product_search
```

### Add Cart Simulation
```
Add VTEX Cart Simulation API to check stock and calculate shipping.

Requirements:
- Validate SKU and quantity
- Include postalCode and country
- Parse response: items, shipping cost, delivery time
- Handle out-of-stock gracefully
- Return formatted totals in R$

Endpoint: POST /api/checkout/pub/orderForms/simulation
```

---

## 🔄 Weni Flows Integration

### Trigger Flow with Data
```
Add Weni Flows trigger to send {message_type} message.

Requirements:
- Use flow UUID: {flow_uuid}
- Pass data: {key1: value1, key2: value2}
- Get token from context.credentials
- Handle trigger failures
- Log success/failure

Pattern from QUICK-REFERENCE.md:
POST https://flows.weni.ai/api/v2/flow_starts.json
```

---

## 🚨 Error Handling

### Add Comprehensive Error Handling
```
Improve error handling in this tool:

[PASTE CODE HERE]

Add:
- Try-except for all external calls
- Specific catches for: Timeout, ConnectionError, HTTPError
- Log errors with [ERROR] prefix
- Return user-friendly messages (no raw exceptions)
- Retry logic for transient failures (max 3 attempts)

Reference: cursor-rules.md error handling pattern
```

---

## ✅ Validation

### Add Input Validation
```
Add robust input validation for these parameters:
- {param1}: {validation_rule}
- {param2}: {validation_rule}

Requirements:
- Validate before processing
- Return clear error messages
- Use validation pattern from AI-CONTEXT.md
- Include examples in error messages
```

### Add CEP Validation
```
Add CEP validation with:
- Remove non-digits (regex)
- Check length = 8
- Format error message
- Example: "❌ CEP inválido. Digite 8 dígitos. Exemplo: 01310100"

Pattern from QUICK-REFERENCE.md: format-cep snippet
```

---

## 📝 Documentation

### Generate Tool Documentation
```
Generate documentation for this tool:

[PASTE CODE HERE]

Include:
- Purpose and use case
- Parameters (type, required/optional, description)
- Return format
- Example usage
- Error scenarios
- API dependencies

Style: Follow docs/02-padroes-boas-praticas.md
```

### Update README
```
Update project README.md to include:
- New agent: {AgentName}
- Purpose: {what_it_does}
- APIs integrated: {VTEX APIs used}
- Status: {in_development / production}

Add to agents table following existing format.
```

---

## 🧪 Testing

### Generate Test Cases
```
Generate test cases for this tool:

[PASTE CODE HERE]

Cover:
- ✅ Happy path (valid inputs)
- ❌ Invalid inputs (empty, wrong type, malformed)
- ⚠️ API errors (timeout, 401, 404, 500)
- 🔄 Edge cases (special characters, max length)
- 📊 Boundary conditions

Format as weni CLI test commands.
```

### Debug Common Error
```
I'm getting this error:

[PASTE ERROR HERE]

Debug it:
1. Check troubleshooting.md for known issues
2. Verify code against standards in cursor-rules.md
3. Suggest specific fixes with code examples
4. Explain root cause
```

---

## 🔍 Code Review

### Review Against Standards
```
Review this code against project standards:

[PASTE CODE HERE]

Check:
- [ ] Follows pattern in AI-CONTEXT.md
- [ ] Uses context.credentials (no hardcoded keys)
- [ ] Has input validation
- [ ] Has error handling (try-except)
- [ ] Has timeout=10 on requests
- [ ] Returns TextResponse with should_wait_agent_response=True
- [ ] Uses proper logging ([INFO], [ERROR])
- [ ] Has user-friendly messages with emojis

Suggest improvements for any violations.
```

### Optimize Performance
```
Optimize this code for performance:

[PASTE CODE HERE]

Focus on:
- Reduce API calls (caching where applicable)
- Set appropriate timeouts
- Limit response sizes
- Remove blocking operations
- Add async if needed for parallel calls

Maintain readability and error handling.
```

---

## 🔄 Refactoring

### Refactor to Use Snippets
```
Refactor this code to use VS Code snippets:

[PASTE CODE HERE]

Replace with:
- weni-tool pattern for class structure
- vtex-* patterns for API calls
- weni-try pattern for error handling
- weni-validate pattern for input checks

Explain which snippets were used where.
```

### Extract Reusable Function
```
Extract this repeated code into a reusable function:

[PASTE CODE HERE]

Create:
- Function name: {function_name}
- Parameters: {params}
- Return type: {return_type}
- Add to: utils.py or helpers.py

Maintain error handling and logging.
```

---

## 🚀 Deployment

### Pre-Deployment Checklist
```
I'm ready to deploy agent {AgentName}. Run pre-deployment checklist:

1. Code review against cursor-rules.md
2. All credentials in YAML (no hardcoded)
3. Input validation on all parameters
4. Error handling on all external calls
5. Timeouts set (10s default)
6. User-friendly messages
7. Logging implemented
8. Local testing passed (weni run --verbose)
9. Documentation updated
10. CHANGELOG.md entry added

Report any issues with specific fixes.
```

### Generate Deployment Notes
```
Generate deployment notes for agent {AgentName} v{version}:

Include:
- What's new / changed
- API integrations
- Configuration required
- Testing checklist
- Rollback plan
- Monitoring points

Format for team review.
```

---

## 📊 Analysis

### Analyze Agent Performance
```
Analyze this agent for performance improvements:

Agent: {AgentName}
Current metrics:
- Response time: {avg_time}s
- Success rate: {percentage}%
- Handoff rate: {percentage}%

Suggest optimizations for:
- Reducing response time
- Improving success rate
- Reducing human handoffs
```

### Compare with Best Practices
```
Compare agent {AgentName} against best practices in docs/02-padroes-boas-praticas.md.

Report:
- ✅ What's following best practices
- ⚠️ What needs improvement
- 🔧 Specific code changes needed
- 📈 Expected impact of changes
```

---

## 🎓 Learning

### Explain Concept
```
Explain how {concept} works in Weni Platform.

Include:
- Purpose and use case
- Code example from this project
- Common pitfalls
- Best practices
- Links to docs for deep dive

Assume reader is familiar with Python but new to Weni.
```

### Generate Tutorial
```
Create a step-by-step tutorial for {task}.

Format:
1. Prerequisites
2. Goal
3. Step-by-step instructions with code
4. Expected output
5. Troubleshooting tips
6. Next steps

Reference existing agents as examples.
```

---

## 🔧 Troubleshooting

### Quick Fix
```
Quick fix needed for:

Error: {error_message}
File: {file_path}
Line: {line_number}

Code:
[PASTE CODE SNIPPET]

Provide:
1. Root cause
2. One-line fix
3. Test to verify fix
```

### Deep Dive Debug
```
Deep dive debug session for:

Problem: {description}
Symptoms: {what's happening}
Expected: {what should happen}
Tried: {what you've tried}

Code:
[PASTE RELEVANT CODE]

Logs:
[PASTE LOGS]

Provide systematic debugging steps with explanations.
```

---

## 💬 Omni Handoff

### Implement Handoff
```
Implement Omni handoff for scenario: {scenario}

Requirements:
- Check condition: {when_to_handoff}
- Use template from MATRIZ-COMPLETA-ANALISE.md: {template_name}
- Trigger Weni Flow: {flow_uuid}
- Pass variables: {{nome}}, {{data}}, {{protocolo}}
- Handle flow trigger failure
- Return confirmation to user

Pattern: weni-flow snippet from QUICK-REFERENCE.md
```

---

## 📚 Documentation Maintenance

### Update After API Change
```
VTEX {API_NAME} API changed:

Old endpoint: {old_endpoint}
New endpoint: {new_endpoint}
Changed params: {params}

Update:
1. Code in relevant tools
2. QUICK-REFERENCE.md API section
3. docs/03-apis-integracoes.md
4. AI-CONTEXT.md if significant
5. Any examples in docs/

List all files that need updates.
```

---

## 🎯 Custom Template

### Your Custom Prompt
```
[Describe your task here]

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Reference:
- [Relevant file or pattern]
- [Coding standards to follow]

Expected output:
- [What you want to get]
```

---

## 💡 Pro Tips for Using These Prompts

1. **Replace placeholders:** `{AgentName}`, `{API_NAME}`, etc.
2. **Add context:** Paste relevant code/logs after the prompt
3. **Be specific:** More details = better results
4. **Reference docs:** Mention specific files (AI-CONTEXT.md, etc.)
5. **Iterate:** Use AI response to refine next prompt

---

**Last Updated:** 12/02/2026  
**Version:** 1.0.0  
**Usage:** Copy prompts, fill placeholders, paste to your AI assistant
