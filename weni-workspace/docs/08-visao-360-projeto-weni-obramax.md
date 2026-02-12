# 🎯 Visão 360° - Projeto Weni & Obramax

## 📋 Índice
- [Visão Geral do Ecossistema](#visão-geral-do-ecossistema)
- [Arquitetura Completa](#arquitetura-completa)
- [Agentes em Produção](#agentes-em-produção)
- [Fluxo de Mensagens Omni](#fluxo-de-mensagens-omni)
- [Integrações Críticas](#integrações-críticas)
- [Stack Tecnológica](#stack-tecnológica)
- [Guia de Especialização](#guia-de-especialização)

---

## 🌐 Visão Geral do Ecossistema

### O Que É a Weni Platform?

A **Weni Platform** é uma plataforma de desenvolvimento de agentes de IA conversacionais que permite criar assistentes inteligentes com integração a APIs externas, principalmente voltados para e-commerce e atendimento ao cliente.

### Projeto Obramax

**Obramax** é o cliente principal deste workspace, uma rede de lojas de materiais de construção que utiliza a Weni Platform para criar uma experiência de compra conversacional completa via WhatsApp.

### Componentes do Workspace

```
Weni/
├── docs/                    # 19 documentos técnicos
├── Obramax/                 # Agentes em produção
├── weni-cli/                # CLI oficial (v3.5.2)
├── weni-cli-https/          # Variante HTTPS
├── *.pdf (6 arquivos)       # Documentação de APIs externas
└── *.csv                    # Templates de mensagens Omni
```

---

## 🏗️ Arquitetura Completa

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENTE WHATSAPP                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              WENI PLATFORM (ORQUESTRADOR)                │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Manager Agent (Roteamento)              │   │
│  └──┬──────────┬──────────┬──────────┬─────────┬──┘   │
└─────│──────────│──────────│──────────│─────────│──────┘
      │          │          │          │         │
      ▼          ▼          ▼          ▼         ▼
┌─────────┐ ┌─────────┐ ┌────────┐ ┌──────┐ ┌──────────┐
│Concierge│ │ Product │ │Checkout│ │Order │ │ Orçamax  │
│  Agent  │ │ Details │ │ Agent  │ │Agent │ │  Agent   │
└────┬────┘ └────┬────┘ └───┬────┘ └──┬───┘ └────┬─────┘
     │           │           │         │          │
     └───────────┴───────────┴─────────┴──────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  INTEGRAÇÕES EXTERNAS                    │
│  ┌───────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │  VTEX APIs    │  │ Weni Flows   │  │ Sistema     │ │
│  │ - Catalog     │  │ - Eventos    │  │ Omni        │ │
│  │ - Checkout    │  │ - Mensagens  │  │ - Transbordo│ │
│  │ - Order       │  │ - Triggers   │  │ - Humanos   │ │
│  │ - Search      │  └──────────────┘  └─────────────┘ │
│  │ - Region      │                                      │
│  └───────────────┘                                      │
└─────────────────────────────────────────────────────────┘
```

### Camadas da Arquitetura

#### 1. **Camada de Interface (WhatsApp)**
- Canal principal de comunicação com clientes
- Integrado à Weni Platform via Webhook
- Suporta mensagens de texto, imagens, documentos

#### 2. **Camada de Orquestração (Weni Platform)**
- **Manager Agent**: Agente principal que roteia conversas
- **Passive Agents**: Agentes especializados invocados sob demanda
- **Active Agents**: Agentes que podem iniciar conversas proativamente

#### 3. **Camada de Tools (Python)**
- Ferramentas Python que executam lógica de negócio
- Integração com APIs externas
- Processamento de dados e validações

#### 4. **Camada de Integração**
- VTEX: E-commerce e gestão de pedidos
- Weni Flows: Automação e workflows
- Sistema Omni: Atendimento humano e transbordo

---

## 🤖 Agentes em Produção

### 1. Concierge Agent (Busca de Produtos)

**Propósito:** Busca inteligente de produtos com regionalização automática

**Arquivo:** `Obramax/[Atual] Concierge com Regionalização/`

**Características:**
- ✅ Busca por nome, especificações, cor, tamanho
- ✅ Validação de estoque por região (CEP)
- ✅ Sugestão de produtos relacionados
- ✅ Cálculo de quantidade (ex: cerâmica, porcelanato)
- ✅ Preços atacado e varejo
- ✅ Integração completa com VTEX APIs

**Credenciais Necessárias:**
```yaml
BASE_URL: "https://lojaobramax.myvtex.com"
STORE_URL: "https://www.obramax.com.br"
VTEX_API_APPKEY: "vtexappkey-xxxxx"
VTEX_API_APPTOKEN: "xxxxx"
API_TOKEN_WENI: "token-weni-flows"
EVENT_ID_CONCIERGE: "uuid-do-evento"
```

**Tool Principal:** `search_product`
- Parâmetros: `product_name`, `postal_code`, `brand` (opcional), `quantity`, `seller_id`
- Retorna: Lista de produtos com preço, estoque, imagem, specs

**Fluxo de Execução:**
```
1. Cliente solicita produto
2. Agente solicita CEP (se não tiver)
3. GetRegionId() → Valida região e sellers disponíveis
4. IntelligentSearch() → Busca produtos na região
5. FilterByStock() → Remove produtos sem estoque
6. SortByStock() → Prioriza maior estoque para cerâmicas
7. GetSkuDetails() → Busca dimensões e peso
8. FormatResponse() → Monta resposta com imagens e preços
9. TriggerFlow() → Envia dados para Weni Flows
```

**Instruções Críticas:**
- Sempre solicita CEP antes de buscar produtos
- Sempre mostra SKU_ID na resposta (obrigatório para checkout)
- Informa preço de atacado quando disponível
- Calcula quantidade de caixas de cerâmica (área + 10% rodapé + 10% quebra)
- Não inventa marca se não informada

**Guardrails:**
- Nunca inventa preços ou promoções
- Nunca omite SKU_ID
- Nunca oferece desconto em frete
- Nunca confirma promoção sem informação

---

### 2. Product Details Agent (PDP)

**Propósito:** Fornece informações detalhadas de produtos específicos quando já se tem o SKU

**Arquivo:** `Obramax/[Atual] Product Details Agent - PDP/`

**Características:**
- ✅ Informações técnicas completas
- ✅ Especificações, dimensões, peso
- ✅ Manuais e códigos de barras
- ✅ Complementa informações do Concierge

**Quando Usar:**
- Cliente quer detalhes sobre produto específico (já tem SKU)
- Dúvidas técnicas sobre um item
- Comparação de especificações

**Quando NÃO Usar:**
- Busca inicial de produtos (usar Concierge)
- Cliente quer comprar (usar Concierge → Checkout)
- Listar múltiplas opções de produtos

**Tool Principal:** `product_details`
- Parâmetro: `sku` (número do SKU)
- Retorna: Specs completas, imagens, manual, dimensões

---

### 3. Checkout Agent (Pagamento + Frete)

**Propósito:** Gera carrinho de compras e link de pagamento

**Arquivo:** `Obramax/[Atual] Checkout vtex + frete/`

**Características:**
- ✅ Cálculo de frete por produto
- ✅ Múltiplas opções de entrega (SLAs)
- ✅ Geração de checkout URL
- ✅ Adição incremental de itens ao carrinho

**Credenciais Necessárias:**
```yaml
BASE_URL: "URL VTEX"
STORE_URL: "URL da loja"
API_TOKEN_WENI: "token-weni"
EVENT_ID_CHECKOUT: "uuid-evento-checkout"
```

**Tool Principal:** `shipping_value` (SimulateShippingAndCreateCart)

**Parâmetros:**
```python
product_items: "[{id=236, quantity=1, seller=1}, {id=237, quantity=2, seller=1}]"
postal_code: "03001-000"
order_form_id: "abc123..." # Opcional, para adicionar mais itens
```

**Retorno:**
```json
{
  "checkout_url": "https://www.obramax.com.br/checkout/?orderFormId=xxx",
  "total_value": 150.50,
  "shipping_info": [
    {
      "product_id": "236",
      "shipping_value": 25.00,
      "delivery_sla": "Normal - 3 dias úteis"
    }
  ]
}
```

**Instruções Críticas:**
- SEMPRE envia `checkout_url` para o Manager
- Soma valores de frete individuais (não é o maior ou menor)
- Nunca pergunta `deliverytype` ao cliente
- Nunca pede `orderformId` ao cliente
- Se produto sem estoque → informa retirada em loja

**Fluxo de Compra:**
```
Concierge → [Cliente confirma compra] → Checkout Agent → Link de Pagamento
```

---

### 4. Order Status Agent

**Propósito:** Consulta status de pedidos realizados

**Arquivo:** `Obramax/OFICIAL order agent vtex/`

**Características:**
- ✅ Busca pedido por número ou CPF/Email
- ✅ Status de entrega
- ✅ Informações de rastreamento
- ✅ Histórico de pedidos

---

### 5. Orçamax Agent

**Propósito:** Agente especializado para orçamentos (sem compra imediata)

**Arquivo:** `Obramax/Orçamax/`

**Características:**
- ✅ Orçamentos sem compromisso
- ✅ Cálculo de materiais por m²
- ✅ Sugestão de produtos para projetos
- ✅ Exportação de lista de materiais

---

## 📨 Fluxo de Mensagens Omni

### O Que É Omni?

**Omni** é o sistema de transbordo humano da Obramax - quando o agente de IA não consegue resolver, a conversa é transferida para um atendente humano.

### Templates de Mensagens (CSV)

**Arquivo:** `Weni _ Matriz de Funcionalidade _ Transbordo _ Instruções - Mensagens Omni.csv`

#### MENSAGEM 1: Transbordo para Próximo Dia
**Quando:** Alto volume de atendimentos, não consegue responder no dia

```
"Olá, tudo bem?

Devido ao alto volume de atendimentos, nosso tempo de resposta pelo WhatsApp 
está um pouco maior no momento e, infelizmente, não conseguimos dar andamento 
à sua solicitação hoje por este canal. Pedimos desculpas pela demora e por 
qualquer transtorno causado.

Responderemos à sua solicitação até amanhã, às 12h. Caso precise de 
atendimento urgente, pedimos, por gentileza, que entre em contato conosco 
por telefone pelo número 3003-3400, das 8h às 18h.

Agradecemos sua compreensão e a confiança em nosso trabalho!

Abraços,
Obramax 🧡"
```

#### MENSAGEM 2: Início de Atendimento Omni
**Quando:** Retomando conversa após transbordo

```
"Olá, tudo bem?
Pedimos desculpas pela demora - vou dar continuidade ao seu atendimento agora 💬✨

Para te ajudar da melhor forma, você pode me contar como posso te auxiliar hoje?

⚠️ Importante: devido ao alto volume de atendimentos, as conversas que ficarem 
sem resposta por mais de 10 minutos serão encerradas automaticamente.

Agradecemos a compreensão! 🧡"
```

#### MENSAGEM 3: Reagendamento de Entrega
**Quando:** Necessário reagendar data de entrega

```
"Olá, tudo bem? Esperamos que você esteja ótimo(a)!

Somos do time Obramax e, antes de tudo, gostaríamos de pedir sinceras 
desculpas por qualquer inconveniente que possamos ter causado. Esse não 
é o padrão do nosso atendimento, e já estamos trabalhando em melhorias 
internas. Seu feedback é muito importante para nós!

Entramos em contato para informar sobre o agendamento pendente da entrega 
do seu material. A entrega será realizada em {{data}}, dentro do horário 
comercial, das 8h às 18h. Caso haja alguma observação ou orientação 
adicional, é só responder a esta mensagem que ficaremos à disposição 
para ajudar.

Agradecemos por nos dar a oportunidade de solucionar o ocorrido. Seguimos 
trabalhando continuamente para a nossa constante evolução.

Abraços,
Obramax 🧡"
```

**Variável:** `{{data}}` → Substituir pela data agendada

#### MENSAGEM 4: Solicitação de 2ª Via Cupom Fiscal
**Quando:** Cliente precisa reemitir cupom fiscal

```
"Olá {{nome}}, tudo bem?

Para que possamos localizar a via do seu cupom fiscal, por favor, 
nos envie as seguintes informações:

LOJA/UNIDADE:
NOME COMPLETO:
CPF / CNPJ:
DATA DA COMPRA:
TELEFONE:
E-MAIL:
6 PRIMEIROS E 4 ÚLTIMOS N° DO CARTÃO:
VALOR TOTAL DA COMPRA:
CÓDIGO/DESCRIÇÃO DO PRODUTO:
DATA DA SOLICITAÇÃO:
RUA/AVENIDA/TRAVESSA:
COMPLEMENTO:
BAIRRO:
CEP:

Assim que recebermos as informações, encaminharemos ao setor responsável 
e, dentro de até 24h, enviaremos a via do seu cupom fiscal por e-mail 
ou WhatsApp.

Aguardamos seu retorno!

Abraços,
{{atendente}}"
```

**Variáveis:** `{{nome}}`, `{{atendente}}`

#### MENSAGEM 5: Solicitação de Imagens
**Quando:** Cliente precisa enviar fotos de produto danificado

```
"Olá,

Espero que esteja tudo bem com você!

Conforme nosso contato, solicitamos o envio de fotos do material que 
chegou danificado, assim como a quantidade do item, para que possamos 
dar andamento à sua solicitação.

Caso precise de qualquer ajuda para realizar o envio, fico à disposição 
para auxiliar. Agradecemos desde já sua compreensão e colaboração.

Abraços,
Obramax 🧡"
```

#### MENSAGEM 6: Tentativa de Contato Sem Sucesso
**Quando:** Tentou ligar mas cliente não atendeu

```
"Olá, {{nome}}!

Desde já, pedimos desculpas pelo transtorno. Tentamos entrar em contato 
para tratar da sua solicitação, mas não obtivemos retorno até o momento.

Poderia, por gentileza, responder a esta mensagem ou entrar em contato 
com nossa equipe de pós-venda pelo telefone 3003-3400? Nosso atendimento 
funciona de segunda a sexta, das 8h às 18h, e aos sábados, das 8h às 16h.

Ficamos à disposição para ajudar!

Atenciosamente,
{{atendente}}"
```

#### MENSAGEM 7: Disponibilização de Crédito
**Quando:** Oferecendo compensação por problemas

```
"Olá, {{nome}}, tudo bem?

Sentimos muito por todos os transtornos causados. Estamos trabalhando 
continuamente para aprimorar os pontos mencionados e garantir uma 
experiência cada vez melhor em nossas lojas e serviços.

Como forma de compensação pelos inconvenientes, disponibilizamos o valor 
do frete como crédito. Você pode optar pelo estorno desse valor ou 
utilizá-lo em uma nova compra, seja pelo site ou diretamente em nossas lojas.

Permanecemos à disposição para qualquer outra necessidade ou esclarecimento."
```

#### MENSAGEM 8: Confirmação de Dados para Estorno
**Quando:** Precisa confirmar dados bancários para estorno

```
"Olá, {{nome}}! Tudo bem?

Somos do Pós-Vendas da Obramax. Estamos tentando entrar em contato para 
tratar da sua solicitação de estorno, mas não tivemos sucesso até o momento. 
Poderia, por gentileza, entrar em contato com a Central do Cliente pelo 
telefone 3003-3400, opção 3?

Nosso horário de atendimento é de segunda a sexta, das 8h às 18h, e aos 
sábados, das 8h às 16h.

Aguardamos seu retorno o mais breve possível.

PS: Por ora, o protocolo {{protocolo}} foi resolvido.

Abraços,
Obramax 🧡"
```

**E-mail Alternativo:**
```
"Olá! Tudo bem?

Somos do Pós-Vendas da Obramax. Desde já, pedimos desculpas pelo transtorno 
causado com o seu pedido.

Tentamos entrar em contato pelo telefone +55 11 99960-0095, mas não obtivemos 
sucesso. Poderia, por gentileza, entrar em contato com nossa Central de 
Pós-Vendas pelo telefone 3003-3400?

Nosso horário de atendimento é de segunda a sexta, das 8h às 18h, e aos 
sábados, das 8h às 16h.

Aguardamos o seu retorno.

Obs.: Este e-mail é automático. Por favor, não responda a este remetente."
```

#### MENSAGEM 10: Finalização de Protocolo (E-mail)
**Quando:** Protocolo foi resolvido

```
"Olá, {{nome}}! Tudo bem?

Lamentamos que tenha enfrentado algum problema conosco. Nosso objetivo é 
garantir que você tenha sempre uma ótima experiência com a Obramax.

Entendemos que sua solicitação já foi atendida e, por isso, estamos 
concluindo o seu chamado. Caso precise de qualquer outro apoio, ficaremos 
felizes em ajudar por meio da nossa Central de Pós-Vendas, pelo telefone 
3003-3400.

Nosso horário de atendimento é de segunda a sexta, das 8h às 18h, e aos 
sábados, das 8h às 16h.

Ficamos à disposição!

Abraços,"
```

#### MENSAGEM 11: Envio de Comprovante de Estorno
**Quando:** Estorno foi processado

```
"Olá, boa tarde!

Segue em anexo o comprovante do seu estorno.

Caso precise de qualquer outro auxílio, estaremos à disposição por meio 
da nossa Central de Pós-Vendas, pelo telefone 3003-3400. Nosso horário 
de atendimento é de segunda a sexta, das 8h às 18h, e aos sábados, 
das 8h às 16h.

Abraços,
Obramax"
```

### Fluxo de Transbordo

```
┌─────────────────────────────────────────────────────────┐
│  1. Cliente faz solicitação complexa                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  2. Agente de IA tenta resolver                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │ Resolveu?   │
              └──┬───────┬──┘
                 │ SIM   │ NÃO
                 ▼       ▼
        ┌────────────┐  ┌────────────────────────────┐
        │ Finaliza   │  │ 3. Trigger Weni Flow       │
        │ conversa   │  │    "Transbordo Humano"     │
        └────────────┘  └──────────┬─────────────────┘
                                   │
                                   ▼
                        ┌────────────────────────────┐
                        │ 4. Sistema Omni            │
                        │    - Enfileira atendimento │
                        │    - Distribui para humano │
                        └──────────┬─────────────────┘
                                   │
                                   ▼
                        ┌────────────────────────────┐
                        │ 5. Atendente Humano        │
                        │    - Usa templates CSV     │
                        │    - Resolve manualmente   │
                        └────────────────────────────┘
```

### Situações Que Geram Transbordo

1. **Reclamações complexas** → Protocolo manual + compensação
2. **Produtos danificados** → Envio de fotos + análise
3. **Problemas de entrega** → Reagendamento manual
4. **Estornos/Reembolsos** → Validação de dados bancários
5. **Dúvidas técnicas específicas** → Consulta especializada
6. **Insatisfação explícita** → Atendimento personalizado

---

## 🔗 Integrações Críticas

### 1. VTEX APIs

#### API de Regionalização
**Endpoint:** `GET /api/checkout/pub/regions`

**Uso:** Determinar se a loja atende determinado CEP

**Retorno:**
```json
[
  {
    "id": "v2.XXXXXX",
    "sellers": [
      {"id": "lojaobramax1000"},
      {"id": "lojaobramax1003"}
    ]
  }
]
```

**Status:**
- ✅ Região atendida: Retorna `region_id` + lista de sellers
- ❌ CEP não atendido: Array vazio → Cliente deve comprar presencialmente

---

#### Intelligent Search API
**Endpoint:** `GET /_v/api/intelligent-search/product_search/{query}`

**Parâmetros:**
```python
{
  "query": "tinta branca",
  "regionId": "v2.XXXXXX",
  "count": 50,
  "hideUnavailableItems": True
}
```

**Filtros Aplicados:**
- `regionId`: Filtra por região do CEP
- `hideUnavailableItems`: Remove produtos sem estoque
- `count`: Limite de resultados

**Retorno:** Lista de produtos com:
- `productId`, `itemId` (SKU)
- `name`, `brand`
- `price`, `listPrice` (preço de/por)
- `images`: URLs das imagens
- `sellers`: Disponibilidade por seller

---

#### Cart Simulation API
**Endpoint:** `POST /api/checkout/pub/orderforms/simulation`

**Uso:** Calcular frete e validar estoque

**Payload:**
```json
{
  "items": [
    {
      "id": "123",
      "quantity": 2,
      "seller": "1"
    }
  ],
  "postalCode": "03001000",
  "country": "BRA"
}
```

**Retorno Crítico:**
```json
{
  "totals": [
    {"id": "Items", "value": 15000},
    {"id": "Shipping", "value": 2500}
  ],
  "logisticsInfo": [
    {
      "itemId": "123",
      "slas": [
        {
          "id": "Normal",
          "price": 2500,
          "deliveryWindow": null,
          "shippingEstimate": "3bd"
        }
      ]
    }
  ]
}
```

**Tratamento:**
- Se `slas` vazio: Produto não disponível para entrega no CEP
- `shippingEstimate`: "3bd" = 3 business days

---

#### Catalog API - SKU Details
**Endpoint:** `GET /api/catalog/pvt/stockkeepingunit/{skuId}`

**Headers:** Requer `X-VTEX-API-AppKey` + `X-VTEX-API-AppToken`

**Uso:** Obter dimensões, peso, códigos de barras

**Retorno:**
```json
{
  "Id": 123,
  "ProductId": 456,
  "Name": "Tinta Branca 18L",
  "PackagedHeight": 30.0,
  "PackagedLength": 25.0,
  "PackagedWidth": 25.0,
  "PackagedWeightKg": 20.0,
  "CubicWeight": 0.01875,
  "AlternateIds": {
    "Ean": "7891234567890"
  }
}
```

---

#### Order Management API
**Endpoint:** `GET /api/oms/pvt/orders/{orderId}`

**Uso:** Consultar status de pedidos

**Retorno:**
```json
{
  "orderId": "OBR-123456789",
  "status": "invoiced",
  "invoicedDate": "2026-02-10T14:30:00Z",
  "items": [...],
  "clientProfileData": {
    "email": "cliente@email.com",
    "phone": "+5511999999999"
  },
  "shippingData": {
    "address": {...}
  }
}
```

---

### 2. Weni Flows Integration

#### Trigger de Flow via API

**Endpoint:** `POST https://flows.weni.ai/api/v2/flow_starts.json`

**Headers:**
```python
{
    'Authorization': f'Token {API_TOKEN_WENI}',
    'Content-Type': 'application/json'
}
```

**Payload:**
```json
{
  "flow": "EVENT_UUID_AQUI",
  "urns": ["whatsapp:5511999999999"],
  "extra": {
    "product_name": "Tinta Suvinil Branca 18L",
    "product_price": 150.00,
    "product_image": "https://...",
    "postal_code": "03001-000"
  }
}
```

**Uso nos Agentes:**
- Concierge: Envia lista de produtos encontrados
- Checkout: Envia dados do carrinho criado
- PDP: Envia especificações detalhadas

**Prevenção de Loop:**
```python
if not self._weni_flow_triggered:
    # Trigger flow
    self._weni_flow_triggered = True
```

---

## 💻 Stack Tecnológica

### Backend (Tools)

#### Python 3.8+
**Bibliotecas Core:**
```python
from weni import Tool                    # Framework Weni
from weni.context import Context         # Contexto de execução
from weni.responses import TextResponse  # Formato de retorno
import requests                          # HTTP requests
import json                              # Manipulação JSON
import urllib.parse                      # URL encoding
```

**Padrões de Código:**
- Herança de `Tool` class
- Método `execute()` obrigatório
- Retorno via `TextResponse`
- Logging estruturado (DEBUG/INFO/WARN/ERROR)

---

### Weni CLI (Command Line Interface)

**Versão:** 3.5.2

**Instalação:**
```bash
pip install weni-cli
```

**Comandos Essenciais:**
```bash
# Autenticação
weni login

# Gerenciamento de projetos
weni project list
weni project use <PROJECT_ID>
weni project current

# Deploy
weni project push

# Teste local
weni run <tool_name>

# Logs
weni logs <agent_name>
```

**Estrutura de Projeto:**
```
meu-projeto/
├── agent_definition.yaml    # Configuração do agente
└── tools/
    └── minha_tool/
        ├── main.py           # Código da tool
        └── test_definition.yaml  # Testes
```

---

### YAML Configuration

#### agent_definition.yaml

**Estrutura Completa:**
```yaml
agents:
  nome_agente:
    # Credenciais
    credentials:
      VARIAVEL_1:
        label: "Rótulo Amigável"
        placeholder: "valor-exemplo"
        is_confidential: true/false
    
    # Constantes
    constants:
      CONSTANTE_1:
        value: "valor-fixo"
    
    # Metadados
    name: "Nome Display"
    description: "Quando o Manager deve invocar este agente"
    
    # Comportamento
    instructions:
      - "Ação que o agente deve executar"
      - "Regra de comportamento"
    
    # Restrições
    guardrails:
      - "O que o agente NUNCA deve fazer"
      - "Restrições de segurança"
    
    # Tools
    tools:
      - nome_tool:
          name: "Display Name"
          source:
            path: "tools/pasta_tool"
            entrypoint: "main.ClasseTool"
            path_test: "test_definition.yaml"
          description: "Quando usar esta tool"
          parameters:
            - nome_parametro:
                description: "Descrição do parâmetro"
                type: "string|number|boolean"
                required: true/false
                contact_field: false
```

---

### Deployment

#### Ambientes

1. **Desenvolvimento Local:**
   - Teste com `weni run`
   - Validação de payloads
   - Debug com logs

2. **Staging (Homologação):**
   - Deploy via `weni project push`
   - Testes integrados com VTEX sandbox
   - Validação de flows

3. **Produção:**
   - Deploy controlado
   - Monitoramento com `weni logs`
   - Rollback rápido se necessário

---

## 🎓 Guia de Especialização

### Para Iniciantes (0-30 dias)

**Semana 1-2: Fundamentos**
1. Ler [00-guia-inicio-rapido.md](00-guia-inicio-rapido.md)
2. Instalar Weni CLI
3. Criar primeiro agente "Hello World"
4. Entender estrutura YAML completa

**Semana 3-4: Primeiro Projeto Real**
1. Estudar [exemplos/concierge-regionalizacao.md](exemplos/concierge-regionalizacao.md)
2. Replicar busca simples de produtos
3. Adicionar validação de CEP
4. Integrar com API de teste

**Checklist de Conclusão:**
- [ ] CLI instalado e configurado
- [ ] Primeiro agente deployado
- [ ] Tool com integração HTTP funcionando
- [ ] Testes locais executando

---

### Para Desenvolvedores (30-90 dias)

**Mês 2: Integrações VTEX**
1. Estudar [03-apis-integracoes.md](03-apis-integracoes.md)
2. Implementar regionalização completa
3. Integrar Intelligent Search
4. Criar simulação de frete

**Mês 3: Projeto Completo**
1. Estudar [exemplos/projeto-completo-yaml.md](exemplos/projeto-completo-yaml.md)
2. Implementar fluxo Concierge → Checkout
3. Adicionar Weni Flows triggers
4. Implementar transbordo Omni

**Checklist de Conclusão:**
- [ ] 3+ agentes em produção
- [ ] Integração VTEX completa
- [ ] Weni Flows configurado
- [ ] Sistema de transbordo funcionando

---

### Para Especialistas (90+ dias)

**Otimizações Avançadas:**
1. Implementar cache de respostas
2. Otimizar tamanho de payload
3. Criar sistema de retry inteligente
4. Monitoramento e alertas

**Arquitetura:**
1. Padrões de microserviços
2. Escalabilidade horizontal
3. CI/CD automatizado
4. Testes end-to-end

**Liderança Técnica:**
1. Code review de PRs
2. Documentação de padrões
3. Mentoria de novos desenvolvedores
4. Evolução da arquitetura

**Checklist de Conclusão:**
- [ ] 10+ agentes gerenciados
- [ ] Padrões de código documentados
- [ ] CI/CD implementado
- [ ] Equipe treinada e produtiva

---

## 📊 KPIs e Métricas

### Métricas de Agentes

**Taxa de Resolução:**
```
(Conversas Resolvidas por IA / Total de Conversas) * 100
```
**Meta:** >80%

**Tempo Médio de Resposta:**
```
Soma(Tempo de Resposta) / Número de Interações
```
**Meta:** <3 segundos

**Taxa de Transbordo:**
```
(Conversas Transferidas para Humano / Total de Conversas) * 100
```
**Meta:** <20%

---

### Métricas de Negócio

**Taxa de Conversão:**
```
(Checkout Links Gerados / Buscas de Produtos) * 100
```

**Ticket Médio:**
```
Valor Total de Vendas / Número de Pedidos
```

**Produtos por Pedido:**
```
Soma(Itens em Carrinhos) / Número de Carrinhos
```

---

## 🔐 Segurança e Compliance

### Credenciais

**NUNCA commitar:**
- ❌ VTEX App Keys
- ❌ VTEX App Tokens
- ❌ API Tokens Weni
- ❌ Senhas ou secrets

**Como gerenciar:**
- ✅ Usar `credentials` no YAML
- ✅ Marcar com `is_confidential: true`
- ✅ Secrets gerenciados pela Weni Platform
- ✅ Rotação periódica de tokens

---

### Dados Sensíveis

**PII (Personally Identifiable Information):**
- Nome completo
- CPF
- Telefone
- Email
- Endereço completo

**Como tratar:**
- Nunca logar em `print()` statements
- Usar mascaramento: `CPF: ***123456**`
- Não armazenar em variáveis globais
- Transmitir apenas via HTTPS

---

## 🚨 Troubleshooting Comum

### Problema: Região não encontrada para CEP

**Sintoma:** `regions_data` retorna array vazio

**Causa:** CEP não atendido pela loja

**Solução:**
```python
if not regions_data:
    message = "Não atendemos a sua região, mas você pode comprar presencialmente."
    return TextResponse(data={"region_message": message})
```

---

### Problema: Produto não retorna na busca

**Sintoma:** Intelligent Search retorna poucos resultados

**Causa:** Filtros muito restritivos ou nome muito específico

**Solução:**
1. Remover filtro de `brand` se não fornecido
2. Buscar com termo mais genérico
3. Aumentar `count` de 50 para 100

---

### Problema: Payload da tool muito grande

**Sintoma:** Erro "Payload exceeds maximum size"

**Causa:** Retornando muitos produtos ou imagens grandes

**Solução:**
```python
# Limitar número de produtos
if len(filtered_products) > 20:
    filtered_products = filtered_products[:20]

# Remover campos desnecessários
for product in products:
    product.pop('unnecessary_field', None)
```

---

### Problema: Weni Flow não triggando

**Sintoma:** Flow não é executado após tool

**Causa:** 
1. URN incorreta
2. Token inválido
3. UUID do flow errado

**Debug:**
```python
print(f"DEBUG: Triggering flow {event_uuid}")
print(f"DEBUG: URN: {urn}")
print(f"DEBUG: Response: {response.status_code} - {response.text}")
```

---

## 📚 Recursos Adicionais

### Documentação Interna

1. **[00-guia-inicio-rapido.md](00-guia-inicio-rapido.md)** - Primeiro agente em 30min
2. **[01-estrutura-projetos.md](01-estrutura-projetos.md)** - Organização de código
3. **[02-padroes-boas-praticas.md](02-padroes-boas-praticas.md)** - Code style
4. **[03-apis-integracoes.md](03-apis-integracoes.md)** - Integrações externas
5. **[04-weni-cli-guia-completo.md](04-weni-cli-guia-completo.md)** - CLI completa
6. **[05-guia-migracao.md](05-guia-migracao.md)** - Migrar projetos antigos
7. **[06-weni-cli-codigo-oficial.md](06-weni-cli-codigo-oficial.md)** - Source code CLI
8. **[07-avaliacao-gaps-documentacao.md](07-avaliacao-gaps-documentacao.md)** - Roadmap

### Exemplos Práticos

1. **[exemplos/concierge-regionalizacao.md](exemplos/concierge-regionalizacao.md)**
2. **[exemplos/projeto-completo-yaml.md](exemplos/projeto-completo-yaml.md)**

### Referências

1. **[reference/api-reference.md](reference/api-reference.md)** - Quick reference
2. **[reference/troubleshooting.md](reference/troubleshooting.md)** - Problemas comuns
3. **[reference/glossario.md](reference/glossario.md)** - Terminologia

---

## 🎉 Conclusão

Este documento fornece uma **visão 360° completa** do projeto Weni & Obramax, cobrindo:

✅ **Arquitetura completa** - Do WhatsApp às APIs VTEX
✅ **5 agentes em produção** - Código real e documentado
✅ **Fluxo de mensagens Omni** - 11 templates prontos para uso
✅ **Integrações críticas** - VTEX + Weni Flows
✅ **Stack tecnológica** - Python, CLI, YAML
✅ **Guia de especialização** - Do iniciante ao expert
✅ **Troubleshooting** - Problemas reais e soluções
✅ **Segurança e compliance** - Boas práticas obrigatórias

**🚀 Próximos Passos:**

1. Escolha seu nível de especialização
2. Siga o guia correspondente
3. Implemente seu primeiro agente
4. Consulte esta documentação sempre que necessário

**📞 Suporte:**

Para dúvidas técnicas:
- Consulte [reference/troubleshooting.md](reference/troubleshooting.md)
- Revise exemplos práticos
- Analise código em `Obramax/[Atual]...`

---

**Documentação atualizada em:** 12/02/2026
**Versão:** 1.0.0
**Mantido por:** Equipe de Desenvolvimento Weni
