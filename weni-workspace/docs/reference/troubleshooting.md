# Troubleshooting - Desenvolvimento de Agentes na Weni

## 🔍 Problemas Comuns e Soluções

### 1. Erro: "Parâmetro obrigatório ausente"

**Sintoma:**
```json
{"error": "Parâmetro 'product_name' é obrigatório"}
```

**Causa:** Parâmetro não foi enviado ou está vazio.

**Solução:**
```python
# ✅ Sempre validar parâmetros
param = context.params.get("param_name")
if not param:
    return TextResponse(data={"error": "Parâmetro 'param_name' é obrigatório"})
```

---

### 2. Erro: "Credenciais não configuradas"

**Sintoma:**
```
ERROR: Falha ao autenticar com API
```

**Causa:** Secrets não configuradas ou com nomes incorretos.

**Checklist:**
- [ ] Verificar se secrets estão configuradas na plataforma Weni
- [ ] Confirmar nomes exatos (case-sensitive): `VTEX_APPKEY`, não `vtex_appkey`
- [ ] Validar valores antes de usar

**Solução:**
```python
vtex_appkey = context.secrets.get("VTEX_APPKEY")
vtex_apptoken = context.secrets.get("VTEX_APPTOKEN")

if not vtex_appkey or not vtex_apptoken:
    print(f"ERROR: Credenciais VTEX não configuradas")
    return TextResponse(data={"error": "Configuração incompleta"})
```

---

### 3. Erro: "Payload muito grande"

**Sintoma:**
```
WARN: Payload excede 20KB
```

**Causa:** Resposta com muitos produtos ou dados muito detalhados.

**Solução:**
```python
def control_payload_size(self, products, max_kb=20):
    json_data = json.dumps(products)
    size_kb = len(json_data.encode('utf-8')) / 1024
    
    if size_kb > max_kb:
        while size_kb > max_kb and products:
            products.pop()  # Remove últimos produtos
            json_data = json.dumps(products)
            size_kb = len(json_data.encode('utf-8')) / 1024
    
    return products
```

**Alternativas:**
- Remover campos desnecessários (descrições longas, especificações detalhadas)
- Paginar resultados
- Retornar apenas top N produtos mais relevantes

---

### 4. Timeout em Requisições HTTP

**Sintoma:**
```
ERROR: Timeout na requisição
```

**Causa:** API externa demorou muito para responder.

**Solução:**
```python
try:
    response = requests.get(url, timeout=30)  # 30 segundos
except requests.exceptions.Timeout:
    print(f"ERROR: Timeout ao consultar {url}")
    return TextResponse(data={
        "error": "Serviço temporariamente indisponível. Tente novamente."
    })
```

---

### 5. Região Não Atendida

**Sintoma:**
```json
{"region_message": "Não atendemos sua região"}
```

**Causa:** CEP não tem sellers disponíveis.

**Verificações:**
- [ ] CEP está no formato correto (8 dígitos, com ou sem hífen)
- [ ] API de regionalização retornou dados
- [ ] Há sellers na lista

**Debug:**
```python
print(f"DEBUG: CEP: {postal_code}")
print(f"DEBUG: Dados regionalização: {regions_data}")
print(f"DEBUG: Sellers encontrados: {sellers}")
```

---

### 6. Produtos Sem Estoque

**Sintoma:** Busca retorna produtos mas todos aparecem sem estoque.

**Causas Possíveis:**
1. Sellers incorretos para a região
2. Quantidade solicitada maior que disponível
3. Produto realmente indisponível

**Debug:**
```python
print(f"DEBUG: Simulando carrinho - SKU: {sku_id}, Seller: {seller_id}")
print(f"DEBUG: Resposta simulação: {simulation_data}")
print(f"DEBUG: Availability: {item.get('availability')}")
print(f"DEBUG: Quantity: {item.get('quantity')}")
```

**Solução:**
- Verificar se `sellers` está sendo passado corretamente
- Confirmar que `quantity` não é excessiva
- Validar `availability` contém "available"

---

### 7. Erro de JSON Decode

**Sintoma:**
```
ERROR: Erro ao processar JSON: Expecting value: line 1 column 1
```

**Causa:** Resposta da API não é JSON válido.

**Solução:**
```python
try:
    response = requests.get(url)
    response.raise_for_status()
    
    # Verifica se resposta não está vazia
    if not response.text:
        print(f"WARN: Resposta vazia de {url}")
        return None
    
    data = response.json()
except json.JSONDecodeError as e:
    print(f"ERROR: Resposta não é JSON válido")
    print(f"ERROR: Conteúdo recebido: {response.text[:200]}")  # Primeiros 200 chars
    return None
```

---

### 8. Status Code Não-200

**Sintoma:**
```
WARN: Status code: 404
ERROR: Status code: 500
```

**Tratamento por Status:**

```python
response = requests.get(url)

if response.status_code == 404:
    print(f"INFO: Recurso não encontrado")
    return None

if response.status_code == 401 or response.status_code == 403:
    print(f"ERROR: Erro de autenticação")
    return TextResponse(data={"error": "Credenciais inválidas"})

if response.status_code >= 500:
    print(f"ERROR: Erro no servidor externo")
    return TextResponse(data={"error": "Serviço temporariamente indisponível"})

if response.status_code != 200:
    print(f"WARN: Status inesperado: {response.status_code}")
    return None
```

---

### 9. Múltiplos Triggers de Flow

**Sintoma:** Flow disparado várias vezes na mesma execução.

**Causa:** Não há controle de trigger único.

**Solução:**
```python
class MyTool(Tool):
    def __init__(self):
        super().__init__()
        self._weni_flow_triggered = False  # Flag de controle
    
    def trigger_weni_flow(self, context):
        # Previne múltiplos triggers
        if self._weni_flow_triggered:
            return
        
        # ... lógica de trigger ...
        
        if success:
            self._weni_flow_triggered = True
```

---

### 10. Erro de Importação

**Sintoma:**
```
ModuleNotFoundError: No module named 'requests'
```

**Causa:** Dependência não instalada.

**Solução:**
1. Adicionar ao `requirements.txt`:
```txt
weni>=1.0.0
requests>=2.28.0
```

2. Instalar localmente:
```bash
pip install -r requirements.txt
```

---

## 🧪 Técnicas de Debug

### 1. Prints Estratégicos

```python
def run(self, context: Context):
    print(f"DEBUG: === INÍCIO DA EXECUÇÃO ===")
    print(f"DEBUG: Params recebidos: {context.params}")
    
    # ... processamento ...
    
    print(f"DEBUG: Resultado intermediário: {resultado}")
    
    # ... mais processamento ...
    
    print(f"DEBUG: === FIM DA EXECUÇÃO ===")
    return TextResponse(data=resultado)
```

### 2. Validação de Tipos

```python
# Verificar tipo de variável
print(f"DEBUG: Tipo de products: {type(products)}")
print(f"DEBUG: É lista? {isinstance(products, list)}")
print(f"DEBUG: Tamanho: {len(products) if isinstance(products, (list, dict)) else 'N/A'}")
```

### 3. Dump de JSON

```python
import json

# Visualizar estrutura completa
print(f"DEBUG: Estrutura completa:")
print(json.dumps(data, indent=2, ensure_ascii=False))
```

### 4. Try/Except Abrangente (temporário)

```python
# Use apenas para debug, seja específico em produção
try:
    # ... código problemático ...
except Exception as e:
    print(f"ERROR: Exceção capturada: {type(e).__name__}")
    print(f"ERROR: Mensagem: {str(e)}")
    import traceback
    print(f"ERROR: Traceback: {traceback.format_exc()}")
    raise  # Re-raise após log
```

---

## 📋 Checklist de Debug

Quando encontrar um problema:

- [ ] Ler mensagem de erro completamente
- [ ] Verificar logs (prints DEBUG, INFO, WARN, ERROR)
- [ ] Confirmar valores de parâmetros de entrada
- [ ] Validar secrets estão configuradas
- [ ] Testar endpoints de API manualmente (Postman, curl)
- [ ] Verificar status codes de requisições
- [ ] Confirmar formato de dados (JSON válido, tipos corretos)
- [ ] Isolar o problema (qual método/linha específica)
- [ ] Adicionar prints temporários para rastrear fluxo
- [ ] Testar com dados simplificados

---

## 🔧 Ferramentas Úteis

### 1. Postman / Insomnia
Testar APIs VTEX manualmente antes de implementar.

### 2. JSON Validator
Validar estrutura de payload: https://jsonlint.com/

### 3. CEP API Tester
Testar regionalização: 
```
https://sualoja.vtexcommercestable.com.br/api/checkout/pub/regions?country=BRA&postalCode=01310100&sc=1
```

### 4. Python REPL
Testar lógica Python isoladamente:
```python
>>> import json
>>> data = {"test": "value"}
>>> size_kb = len(json.dumps(data).encode('utf-8')) / 1024
>>> print(f"{size_kb:.2f} KB")
```

---

## 📞 Quando Pedir Ajuda

Se após seguir este guia o problema persistir:

1. **Documente:**
   - Mensagem de erro completa
   - Parâmetros de entrada usados
   - Logs relevantes (DEBUG, ERROR)
   - O que já foi tentado

2. **Prepare ambiente de teste:**
   - Dados de exemplo que reproduzem o problema
   - Versões de dependências (`pip freeze`)

3. **Contextualize:**
   - O que era esperado
   - O que aconteceu
   - Quando começou (se funcionava antes)

---

## 📚 Recursos Adicionais

- [Estrutura de Projetos](../01-estrutura-projetos.md)
- [Padrões e Boas Práticas](../02-padroes-boas-praticas.md)
- [APIs e Integrações](../03-apis-integracoes.md)
- [Glossário](glossario.md)
