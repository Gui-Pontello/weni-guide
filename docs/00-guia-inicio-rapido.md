# Guia de Início Rápido - Desenvolvimento de Agentes na Weni

## 🚀 Bem-vindo!

Este guia te ajudará a criar seu primeiro agente de IA na plataforma Weni em menos de 30 minutos.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conhecimento básico de Python
- Acesso à plataforma Weni
- Credenciais VTEX (se for integrar com VTEX)

## ⚡ Quick Start (5 minutos)

### 1. Criar Estrutura do Projeto

```bash
mkdir meu-agente
cd meu-agente
mkdir -p tools/minha_tool
```

### 2. Criar `main.py`

```python
# tools/minha_tool/main.py
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse

class MinhaTool(Tool):
    def run(self, context: Context):
        # Recebe parâmetro
        nome = context.params.get("nome", "Visitante")
        
        # Retorna resposta
        return TextResponse(data={
            "mensagem": f"Olá, {nome}! Bem-vindo à Weni."
        })
```

### 3. Criar `requirements.txt`

```txt
weni>=1.0.0
requests>=2.28.0
```

### 4. Testar Localmente (opcional)

```bash
pip install -r tools/minha_tool/requirements.txt
```

### 5. Deploy na Plataforma Weni

Via CLI da Weni (consulte documentação oficial da plataforma).

---

## 📚 Próximos Passos

Agora que você tem um agente básico funcionando, vamos adicionar funcionalidades:

### Adicionando Validação de Parâmetros

```python
def run(self, context: Context):
    # Parâmetro obrigatório
    nome = context.params.get("nome")
    
    if not nome:
        return TextResponse(data={
            "error": "Parâmetro 'nome' é obrigatório"
        })
    
    # Parâmetro opcional com padrão
    idade = context.params.get("idade", 18)
    
    return TextResponse(data={
        "mensagem": f"Olá, {nome}! Você tem {idade} anos."
    })
```

### Adicionando Credenciais (Secrets)

```python
def run(self, context: Context):
    # Extrai secret configurada na plataforma
    api_key = context.secrets.get("API_KEY")
    
    if not api_key:
        return TextResponse(data={
            "error": "Configuração incompleta"
        })
    
    # Usa a API key...
    return TextResponse(data={"status": "success"})
```

### Fazendo Requisições HTTP

```python
import requests

def run(self, context: Context):
    url = "https://api.exemplo.com/dados"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return TextResponse(data=data)
    
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return TextResponse(data={
            "error": "Erro ao consultar API externa"
        })
```

---

## 🛒 Exemplo Prático: Busca de Produtos VTEX

### Estrutura Completa

```
busca-produtos/
├── tools/
│   └── search_product/
│       ├── main.py
│       └── requirements.txt
└── README.md
```

### Implementação

```python
# tools/search_product/main.py
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests

class SearchProduct(Tool):
    def run(self, context: Context):
        # 1. Parâmetros
        product_name = context.params.get("product_name")
        postal_code = context.params.get("postal_code")
        
        # Validação
        if not product_name or not postal_code:
            return TextResponse(data={
                "error": "Parâmetros obrigatórios: product_name e postal_code"
            })
        
        # 2. Secrets
        base_url = context.secrets.get("BASE_URL")
        store_url = context.secrets.get("STORE_URL")
        
        # 3. Busca regionalização
        region_id, error = self.get_region(postal_code, base_url)
        
        if error:
            return TextResponse(data={"error": error})
        
        # 4. Busca produtos
        products = self.search_products(product_name, store_url, region_id)
        
        # 5. Retorna
        return TextResponse(data={"products": products})
    
    def get_region(self, cep, base_url):
        """Consulta regionalização"""
        url = f"{base_url}/api/checkout/pub/regions?country=BRA&postalCode={cep}&sc=1"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return None, "Região não atendida"
            
            region_id = data[0].get("id")
            return region_id, None
        
        except Exception as e:
            print(f"ERROR: {e}")
            return None, "Erro ao consultar regionalização"
    
    def search_products(self, query, url, region_id):
        """Busca produtos"""
        search_url = f"{url}/api/io/_v/api/intelligent-search/product_search/"
        params = {
            "query": query,
            "hideUnavailableItems": "true",
            "regionId": region_id
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            products = []
            for product in data.get("products", []):
                products.append({
                    "name": product.get("productName"),
                    "brand": product.get("brand"),
                    "description": product.get("description")
                })
            
            return products
        
        except Exception as e:
            print(f"ERROR: {e}")
            return []
```

### Configurar Secrets

Na plataforma Weni, adicione:
```
BASE_URL=https://sualoja.vtexcommercestable.com.br
STORE_URL=https://www.sualoja.com.br
```

### Testar

**Input:**
```json
{
  "product_name": "cimento",
  "postal_code": "01310-100"
}
```

**Output:**
```json
{
  "products": [
    {
      "name": "Cimento CP II - 50kg",
      "brand": "Votorantim",
      "description": "Cimento de alta qualidade..."
    }
  ]
}
```

---

## 🎓 Conceitos Importantes

### 1. Tool vs Flow

- **Tool**: Código Python que executa lógica (nossa responsabilidade)
- **Flow**: Fluxo conversacional na plataforma Weni (configurado visualmente)

### 2. Context

Contém tudo que você precisa:
- `params`: Dados do usuário
- `secrets`: Credenciais
- `user`: Info do usuário (URN, canal, etc.)

### 3. TextResponse

Sempre retorne via `TextResponse`:
```python
return TextResponse(data={...})
```

### 4. Logging

Use prints para debug:
```python
print(f"DEBUG: Processando {product_name}")
print(f"INFO: {len(products)} produtos encontrados")
print(f"ERROR: Falha na requisição: {error}")
```

---

## ✅ Checklist do Primeiro Agente

- [ ] Estrutura de pastas criada
- [ ] `main.py` com classe herdando de `Tool`
- [ ] Método `run()` implementado
- [ ] Validação de parâmetros obrigatórios
- [ ] Tratamento de erros em requisições HTTP
- [ ] `requirements.txt` criado
- [ ] Secrets configuradas na plataforma
- [ ] Testado com dados reais
- [ ] README.md documentando uso

---

## 🐛 Troubleshooting Rápido

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Erro: "Parâmetro ausente"
```python
# Sempre validar
param = context.params.get("param")
if not param:
    return TextResponse(data={"error": "..."})
```

### Erro: "Timeout"
```python
# Adicionar timeout
response = requests.get(url, timeout=30)
```

### Payload muito grande
```python
# Limitar quantidade de produtos
products = products[:10]  # Primeiros 10
```

---

## 📖 Documentação Completa

Agora que você criou seu primeiro agente, aprofunde-se:

### 📚 Guias Essenciais
1. [Estrutura de Projetos](01-estrutura-projetos.md) - Organização profissional
2. [Padrões e Boas Práticas](02-padroes-boas-praticas.md) - Código de qualidade
3. [APIs e Integrações](03-apis-integracoes.md) - VTEX e Weni Flows

### 🔍 Referências
- [API Reference](reference/api-reference.md) - Consulta rápida
- [Troubleshooting](reference/troubleshooting.md) - Solução de problemas
- [Glossário](reference/glossario.md) - Terminologia

### 💡 Exemplos
- [Concierge com Regionalização](exemplos/concierge-regionalizacao.md) - Busca avançada
- Mais exemplos na pasta `exemplos/`

---

## 🎯 Próximos Desafios

1. **Adicionar mais parâmetros** ao seu agente
2. **Integrar com API externa** (VTEX, etc.)
3. **Implementar validação de estoque** via cart simulation
4. **Disparar Weni Flow** para notificações
5. **Adicionar enriquecimento de dados** (preços, dimensões)
6. **Implementar controle de payload** (< 20KB)

---

## 💬 Comunidade

- Consulte a documentação oficial da Weni
- Revise os exemplos do repositório Obramax
- Participe de treinamentos técnicos

---

**Parabéns!** 🎉 Você está pronto para desenvolver agentes de IA na Weni!

Comece simples e vá adicionando complexidade gradualmente. Boa sorte!
