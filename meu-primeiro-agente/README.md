# Meu Primeiro Agente Weni

Agente de teste simples que:
- Responde "oi"
- Consulta CEP usando ViaCEP API

## Estrutura

```
meu-primeiro-agente/
├── agent_definition.yaml      # Configuração do agente
├── tools/
│   └── consultaCep/
│       ├── main.py            # Ferramenta de consulta
│       └── requirements.txt   # Dependências
└── README.md                  # Este arquivo
```

## Testar Localmente

```bash
cd meu-primeiro-agente
weni run --verbose
```

## Testar no Chat

1. `oi` → Deve responder educadamente
2. `consulte o cep 01310100` → Retorna dados do CEP
3. `qual o cep 20040020` → Retorna dados do CEP

## Fazer Deploy

```bash
weni project list           # Listar projetos
weni project use <ID>       # Selecionar projeto
weni project push           # Fazer upload
```
