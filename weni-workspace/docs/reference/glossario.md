# Glossário - Desenvolvimento de Agentes de IA na Weni

## 📘 Termos da Plataforma Weni

### Weni CLI
Interface de linha de comando para criar, gerenciar e fazer deploy de agentes de IA na plataforma Weni. Permite desenvolvimento local e deploy automatizado.

### Tool
Componente reutilizável que executa uma função específica dentro de um agente de IA. Implementada como uma classe Python que herda de `weni.Tool`.

### Context
Objeto que contém todas as informações contextuais sobre a execução de uma tool:
- `parameters`: Parâmetros de entrada fornecidos pelo usuário
- `credentials`: Credenciais e variáveis de ambiente sensíveis
- `constants`: Valores configuráveis compartilhados entre tools
- `user`: Informações do usuário (URN, canal, etc.)

### TextResponse
Classe usada para retornar dados estruturados de uma tool. Aceita dicionários Python que são serializados para JSON.

### Agent Definition (YAML)
Arquivo YAML que define completamente um agente: nome, instruções, guardrails, tools, credenciais e constantes.

### Passive Agent
Agente reativo que responde a inputs de usuários ou triggers específicos. Otimizado para atendimento ao cliente.

### Active Agent
Agente proativo que inicia conversas ou ações automaticamente. Usado para notificações, follow-ups e ações agendadas.

### Instructions
Regras e diretrizes que o agente deve seguir (mínimo 40 caracteres). Define o comportamento e expertise do agente.

### Guardrails
Limites e restrições do agente (mínimo 40 caracteres). Define tópicos proibidos e boundaries comportamentais.

### Credentials
Valores sensíveis (API keys, tokens) configurados no YAML e acessados via `context.credentials`. Nunca hardcoded.

### Constants
Valores configuráveis definidos no agente e compartilhados entre todas as tools. Acessados via `context.constants`.

### Contact Fields
Campos do contato que podem ser usados como parâmetros de tools, permitindo acesso a informações do perfil do usuário.

### Flow
Fluxo de conversação criado na plataforma Weni que pode ser disparado por tools.

### URN (Uniform Resource Name)
Identificador único do usuário no formato `whatsapp:5511999999999` ou similar.

### Entrypoint
Caminho completo para a classe da tool no formato `module.ClassName` (ex: `main.BuscarProdutos`).

## 🛒 Termos VTEX

### SKU (Stock Keeping Unit)
Unidade específica de um produto. Ex: Camiseta azul tamanho M é um SKU diferente de camiseta azul tamanho G.

### Seller
Loja ou centro de distribuição responsável por vender e/ou entregar produtos. Uma VTEX pode ter múltiplos sellers.

### Region ID
Identificador de região geográfica na VTEX, usado para filtrar produtos disponíveis em determinado CEP.

### Intelligent Search
Sistema de busca da VTEX que indexa produtos e permite filtros avançados, incluindo regionalização.

### Cart Simulation
Simulação de carrinho que valida estoque, preço final e opções de entrega sem criar um pedido real.

### Fixed Price
Preço especial (geralmente atacado) aplicado quando quantidade mínima é atingida.

### OMS (Order Management System)
Sistema de gerenciamento de pedidos da VTEX.

### Catalog API
API privada da VTEX para gerenciar catálogo, produtos e SKUs.

### Checkout API
API pública da VTEX para operações de checkout, incluindo simulação e regionalização.

## 🔧 Termos Técnicos

### Payload
Dados enviados ou recebidos em uma requisição HTTP. No contexto da Weni, geralmente limitado a 20KB.

### Regionalização
Processo de filtrar produtos e sellers baseado na localização (CEP) do cliente.

### AppKey / AppToken
Credenciais de autenticação da VTEX para acessar APIs privadas.

### Base URL
URL principal da loja VTEX (ex: `https://sualoja.vtexcommercestable.com.br`).

### Store URL
URL pública da loja (ex: `https://www.sualoja.com.br`).

## 📦 Estruturas de Dados Comuns

### Product Structure
```python
{
    "product_name": str,
    "description": str,
    "brand": str,
    "categories": [str],
    "specification_groups": [...],
    "variations": [...]  # Lista de SKUs
}
```

### SKU Structure
```python
{
    "sku_id": str,
    "sku_name": str,
    "price": float,
    "spotPrice": float,
    "quantity": int,
    "seller_id": str,
    "imageUrl": str
}
```

### Region Structure
```python
{
    "id": str,  # Ex: "v2.1A2B3C4D"
    "sellers": [
        {"id": str}
    ]
}
```

## 🎯 Conceitos de Negócio

### Categoria Prioritária
Categorias de produtos que exigem tratamento especial, geralmente ordenadas por maior disponibilidade em estoque. Exemplos: pisos, porcelanatos, revestimentos.

### Tipo de Entrega (Delivery Type)
- **Retirada**: Cliente busca em loja física
- **Entrega**: Produto entregue no endereço do cliente

### Simulação de Carrinho
Processo de validar disponibilidade, preço e frete antes de mostrar produtos ao cliente.

### Enriquecimento de Dados
Adicionar informações complementares aos produtos (dimensões, peso, preços especiais, etc.).

### Controle de Payload
Limitação do tamanho da resposta removendo produtos excedentes para respeitar limites da plataforma.

## 🔐 Segurança

### Secrets
Variáveis de ambiente sensíveis (credenciais, tokens, URLs) configuradas na plataforma Weni, nunca hardcoded no código.

### Sanitização
Processo de remover ou ofuscar dados sensíveis de logs e mensagens de erro.

## 🐛 Debugging

### Debug Levels
- **DEBUG**: Informações detalhadas para desenvolvimento
- **INFO**: Informações gerais do fluxo de execução
- **WARN**: Avisos que não impedem funcionamento
- **ERROR**: Erros que afetam funcionalidade

### Print Statement
Comando Python usado para logging durante desenvolvimento. Na produção, considere usar biblioteca de logging apropriada.

## 📊 Métricas e Limites

### 20KB Limit
Limite máximo recomendado para tamanho de payload de resposta.

### Timeout
Tempo máximo de espera para uma requisição HTTP (geralmente 30 segundos).

### Rate Limit
Limite de requisições por segundo/minuto imposto por APIs externas.

## 🔄 Fluxo de Dados

### Request Flow
1. Recebe parâmetros do usuário
2. Valida entradas obrigatórias
3. Extrai credenciais (secrets)
4. Processa lógica de negócio
5. Retorna resposta estruturada

### Response Flow
1. Busca dados de APIs externas
2. Valida e filtra resultados
3. Enriquece com informações adicionais
4. Formata resposta
5. Controla tamanho
6. Retorna via TextResponse

## 📝 Convenções de Código

### Snake Case
`nome_da_variavel` - Usado para variáveis e parâmetros Python.

### Camel Case
`nomeDoMetodo` - Usado para métodos no código analisado (padrão do projeto).

### Pascal Case
`NomeDaClasse` - Usado para nomes de classes.

### UPPER CASE
`CONSTANTE_VALOR` - Usado para constantes.

## 🔗 Recursos Externos

### VTEX Developer Portal
Portal oficial com documentação de todas as APIs VTEX.

### Weni Platform Docs
Documentação oficial da plataforma Weni.

### CLI (Command Line Interface)
Interface de linha de comando para desenvolvimento e deploy de agentes.

---

## 📚 Leitura Complementar

- [Estrutura de Projetos](../01-estrutura-projetos.md)
- [Padrões e Boas Práticas](../02-padroes-boas-praticas.md)
- [APIs e Integrações](../03-apis-integracoes.md)
- [Exemplos Práticos](../exemplos/)
