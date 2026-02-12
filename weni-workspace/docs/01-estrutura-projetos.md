# Estrutura de Projetos - Agentes de IA na Weni

## 📁 Estrutura de Pastas Padrão

A estrutura organizada dos projetos facilita manutenção e escalabilidade:

```
nome-do-agente/
├── tools/
│   └── nome_funcionalidade/
│       ├── main.py          # Código principal da tool
│       ├── requirements.txt # Dependências Python
│       └── config.json      # Configurações (opcional)
├── flows/                   # Fluxos relacionados (opcional)
├── README.md               # Documentação do agente
└── .env.example           # Exemplo de variáveis de ambiente
```

### Exemplo: Agente de Busca de Produtos

```
Concierge com Regionalização/
└── tools/
    └── productConcierge/
        ├── main.py
        └── requirements.txt
```

## 🔧 Estrutura de uma Tool (main.py)

Toda tool segue um padrão baseado na classe `Tool` da biblioteca Weni:

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests
import json

class NomeDaTool(Tool):
    def __init__(self):
        super().__init__()
        # Inicialização de flags e variáveis de controle
        self._weni_flow_triggered = False
    
    def run(self, context: Context):
        """
        Método principal executado quando a tool é chamada
        
        Args:
            context: Objeto de contexto da Weni contendo:
                - params: Parâmetros de entrada
                - secrets: Variáveis de ambiente/credenciais
                - user: Informações do usuário
        """
        # Extração de parâmetros
        parametro1 = context.params.get("parametro1")
        parametro2 = context.params.get("parametro2", "valor_padrao")
        
        # Extração de secrets/credenciais
        api_key = context.secrets.get("API_KEY")
        
        # Lógica principal
        resultado = self.processar_dados(parametro1, parametro2)
        
        # Retorno estruturado
        return TextResponse(data=resultado)
    
    def processar_dados(self, param1, param2):
        """Métodos auxiliares para organizar a lógica"""
        # Implementação
        pass
```

## 📋 Componentes Essenciais

### 1. Importações Padrão

```python
from weni import Tool
from weni.context import Context
from weni.responses import TextResponse
import requests  # Para chamadas HTTP
import json      # Manipulação de JSON
import sys       # Para debugging
```

### 2. Classe Principal

- **Nome**: Use PascalCase descritivo (ex: `SearchProduct`, `ProductDetails`)
- **Herança**: Sempre herdar de `Tool`
- **Construtor**: Inicialize variáveis de controle no `__init__`

### 3. Método `run()`

Este é o ponto de entrada obrigatório que a Weni chama:

```python
def run(self, context: Context):
    # 1. Validação de parâmetros obrigatórios
    param = context.params.get("param_obrigatorio")
    if not param:
        return TextResponse(data={"error": "Parâmetro obrigatório ausente"})
    
    # 2. Extração de configurações
    base_url = context.secrets.get("BASE_URL")
    api_key = context.secrets.get("API_KEY")
    
    # 3. Processamento
    resultado = self.processar(param, base_url, api_key)
    
    # 4. Retorno
    return TextResponse(data=resultado)
```

## 🔐 Gerenciamento de Credenciais

### Via Context.secrets

```python
# Extração de credenciais
vtex_appkey = context.secrets.get("VTEX_APPKEY")
vtex_apptoken = context.secrets.get("VTEX_APPTOKEN")
base_url = context.secrets.get("BASE_URL")

# Sempre valide antes de usar
if not vtex_appkey or not vtex_apptoken:
    return TextResponse(data={"error": "Credenciais não configuradas"})
```

### Variáveis Comuns

- `BASE_URL`: URL da API principal (ex: VTEX)
- `VTEX_APPKEY`: Chave de aplicação VTEX
- `VTEX_APPTOKEN`: Token de autenticação VTEX
- `STORE_URL`: URL da loja
- `WENI_TOKEN`: Token para chamar flows da Weni
- `WENI_FLOW_ID`: ID do flow para disparar eventos

## 🎯 Métodos Auxiliares

Organize a lógica em métodos reutilizáveis:

```python
class SearchProduct(Tool):
    def __init__(self):
        super().__init__()
    
    def run(self, context: Context):
        # Lógica principal
        pass
    
    def buscar_produto(self, nome, url):
        """Busca produto na API"""
        pass
    
    def validar_estoque(self, sku_id, sellers):
        """Valida disponibilidade em estoque"""
        pass
    
    def formatar_resposta(self, produtos):
        """Formata resposta para o usuário"""
        pass
```

### Convenções de Nomenclatura

- **Métodos públicos**: `camelCase` (ex: `getRegionId`, `cartSimulation`)
- **Métodos privados**: Prefixo `_` (ex: `_validar_dados`)
- **Constantes**: `UPPER_CASE` (ex: `MAX_PRODUCTS`)

## 📦 Requirements.txt

Liste todas as dependências externas:

```txt
weni>=1.0.0
requests>=2.28.0
python-dotenv>=0.19.0
```

## 🧪 Debugging

Use print statements estratégicos:

```python
print(f"DEBUG: Iniciando busca com params: {params}")
print(f"INFO: {len(produtos)} produtos encontrados")
print(f"WARN: Payload excedeu limite: {size_kb:.2f} KB")
print(f"ERROR: Falha na requisição: {error}")
```

### Níveis de Log

- `DEBUG:` Informações detalhadas para desenvolvimento
- `INFO:` Informações gerais do fluxo
- `WARN:` Avisos que não impedem execução
- `ERROR:` Erros que afetam a funcionalidade

## 🚀 Checklist de Estrutura

- [ ] Classe herda de `Tool`
- [ ] Método `run()` implementado
- [ ] Tratamento de erros adequado
- [ ] Validação de parâmetros obrigatórios
- [ ] Extração segura de secrets
- [ ] Logs de debug implementados
- [ ] Retorno via `TextResponse`
- [ ] Métodos auxiliares organizados
- [ ] Documentação inline (docstrings)
- [ ] Requirements.txt atualizado

## 📚 Próximos Passos

Após estruturar seu projeto:

1. Leia [Padrões e Boas Práticas](02-padroes-boas-praticas.md)
2. Consulte [APIs e Integrações](03-apis-integracoes.md) para integrações externas
3. Veja exemplos práticos na pasta `exemplos/`
