# 🚀 Quick Start - Do Zero ao Primeiro Agente

> **Objetivo:** Em 10 minutos, do zero até seu primeiro agente Weni funcionando!

---

## ✅ Passo 1: Pré-requisitos (2 min)

### Verificar Python

```bash
python --version
```

**Precisa:** Python 3.8 ou superior  
**Não tem?** Baixe em: https://www.python.org/downloads/

---

## 📦 Passo 2: Instalar Weni CLI (1 min)

```bash
pip install weni-cli
```

**Verificar instalação:**
```bash
weni --version
```

**Se der erro "weni não reconhecido":**
- Windows: Use `python -m weni` ao invés de `weni`
- OU adicione Python/Scripts ao PATH

---

## 🔐 Passo 3: Login na Plataforma (2 min)

```bash
weni login
```

**O que acontece:**
1. CLI abre navegador automaticamente
2. Faça login em: https://accounts.weni.ai/
3. Autorize o CLI no site
4. Aguarde mensagem: **"Successfully logged in, you can close this window now"**
5. Volta pro terminal → Login completo! ✅

**Navegador não abriu?**
1. Copie a URL que apareceu no terminal
2. Cole no navegador
3. Faça login e autorize

**⚠️ Erro SSL Certificate (Rede Corporativa)?**
- Esse erro ocorre em redes corporativas com certificados próprios
- **Solução:** Execute o login **conectado na rede da empresa** (VPN ou presencialmente)
- O login funciona no navegador, mas o CLI precisa da conexão corporativa para capturar o token

**Verificar login:**
```bash
weni project list
```

Deve listar seus projetos da Weni.

---

## 🏗️ Passo 4: Criar Primeiro Agente (3 min)

### 4.1. Criar pasta do projeto

```bash
mkdir meu-primeiro-agente
cd meu-primeiro-agente
```

### 4.2. Criar arquivo `agent_definition.yaml`

**Copie e cole este código:**

```yaml
agent:
  name: "MeuPrimeiroAgente"
  version: "1.0.0"
  description: "Agente de teste - responde oi e consulta CEP"

instructions: |
  Você é um assistente amigável chamado Bot Teste.
  
  Quando o usuário disser "oi", responda educadamente.
  
  Quando o usuário pedir para consultar um CEP, use a ferramenta ConsultaCEP.
  
  Seja sempre educado e prestativo.

guardrails:
  - type: check_message_limit
    params:
      max_messages: 20

tools:
  - name: ConsultaCEP
    path: tools/consultaCep
```

### 4.3. Criar a ferramenta (tool)

**Criar estrutura:**
```bash
mkdir -p tools/consultaCep
```

**Criar arquivo: `tools/consultaCep/main.py`**

```python
from weni import Tool, Context, TextResponse
import requests

class ConsultaCEP(Tool):
    def execute(self, context: Context, **kwargs) -> TextResponse:
        """Consulta informações de um CEP usando ViaCEP API"""
        
        # 1. Pegar o CEP informado pelo usuário
        cep = kwargs.get("cep", "")
        
        # 2. Validar CEP
        cep_limpo = cep.replace("-", "").replace(".", "").strip()
        
        if not cep_limpo or len(cep_limpo) != 8:
            return TextResponse(
                text="❌ CEP inválido! Por favor, informe 8 dígitos. Exemplo: 01310100",
                should_wait_agent_response=True
            )
        
        # 3. Consultar API ViaCEP
        try:
            print(f"[INFO] Consultando CEP: {cep_limpo}")
            
            url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                dados = response.json()
                
                # Verificar se CEP existe
                if "erro" in dados:
                    return TextResponse(
                        text=f"⚠️ CEP {cep_limpo} não encontrado.",
                        should_wait_agent_response=True
                    )
                
                # Formatar resposta
                resultado = f"""✅ **CEP Encontrado!**

📍 CEP: {dados.get('cep', 'N/A')}
📮 Logradouro: {dados.get('logradouro', 'N/A')}
🏘️ Bairro: {dados.get('bairro', 'N/A')}
🏙️ Cidade: {dados.get('localidade', 'N/A')}
🗺️ Estado: {dados.get('uf', 'N/A')}
"""
                
                return TextResponse(
                    text=resultado,
                    should_wait_agent_response=True
                )
            else:
                return TextResponse(
                    text=f"⚠️ Erro ao consultar CEP. Status: {response.status_code}",
                    should_wait_agent_response=True
                )
                
        except requests.exceptions.Timeout:
            print("[ERROR] Timeout ao consultar ViaCEP")
            return TextResponse(
                text="⚠️ Tempo limite excedido. Tente novamente.",
                should_wait_agent_response=True
            )
        except Exception as e:
            print(f"[ERROR] Erro: {str(e)}")
            return TextResponse(
                text="❌ Erro ao consultar CEP. Tente novamente mais tarde.",
                should_wait_agent_response=True
            )
```

**Criar arquivo: `tools/consultaCep/requirements.txt`**

```
requests==2.31.0
```

---

## 🧪 Passo 5: Testar Localmente (2 min)

**Executar em modo de teste:**

```bash
weni run --verbose
```

**O que vai acontecer:**
1. CLI carrega seu agente
2. Abre interface de chat no terminal
3. Você pode conversar com o agente!

**Teste essas mensagens:**
- `oi`
- `consulte o cep 01310100`
- `qual o cep 20040020`

**Para sair:** Ctrl+C

---

## 🚀 Passo 6: Deploy na Plataforma (5 min)

### 6.1. Escolher projeto

```bash
weni project list
```

Copie o **ID** do projeto onde quer criar o agente.

```bash
weni project use <ID_DO_PROJETO>
```

### 6.2. Fazer push (deploy)

```bash
weni project push
```

**O que acontece:**
1. CLI empacota seu agente
2. Valida YAML e código
3. Faz upload para a plataforma
4. Retorna URL do agente

### 6.3. Testar na plataforma

1. Acesse: https://dash.weni.ai/
2. Entre no projeto
3. Vá em **Agents** ou **Inteligências**
4. Encontre "MeuPrimeiroAgente"
5. Clique em **Test** ou **Testar**
6. Converse com ele!

---

## 🎯 Resumo dos Comandos

```bash
# Instalar
pip install weni-cli

# Login
weni login

# Ver projetos
weni project list

# Usar projeto
weni project use <ID>

# Testar localmente
weni run --verbose

# Deploy
weni project push

# Ver logs (produção)
weni logs --follow
```

---

## 🐛 Troubleshooting Rápido

### Erro: "weni não reconhecido"

**Solução 1:** Use com Python
```bash
python -m weni login
python -m weni run --verbose
```

**Solução 2:** Adicionar ao PATH
- Windows: Adicione `C:\Python3X\Scripts` ao PATH
- Mac/Linux: `export PATH="$PATH:~/.local/bin"`

### Erro: "No module named 'weni'"

```bash
pip install --upgrade weni-cli
```

### Erro: "Tool not found"

Verifique estrutura:
```
├── agent_definition.yaml
└── tools/
    └── consultaCep/
        └── main.py  ← Nome DEVE ser main.py
```

### Erro: "Invalid YAML"

- Use 2 espaços para indentação (não TAB)
- Valide em: https://www.yamllint.com/

---

## 📚 Próximos Passos

Agora que você criou seu primeiro agente, explore:

1. **[AI-CONTEXT.md](AI-CONTEXT.md)** - Entenda a arquitetura completa
2. **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** - Comandos e APIs
3. **[.vscode/weni-agent.code-snippets](.vscode/weni-agent.code-snippets)** - Templates prontos
4. **[docs/02-padroes-boas-praticas.md](docs/02-padroes-boas-praticas.md)** - Code standards

### Crie agentes mais avançados:

- **Integração VTEX:** Veja [docs/03-apis-integracoes.md](docs/03-apis-integracoes.md)
- **Weni Flows:** Automatize mensagens
- **Omni Handoff:** Transbordo para humanos
- **Múltiplas ferramentas:** Combine APIs

---

## 💡 Dicas Pro

1. **Use VS Code:** Temos snippets prontos (type `weni-agent` + Tab)
2. **Teste sempre localmente:** `weni run --verbose` antes de deploy
3. **Veja logs:** `weni logs --follow` para debug em produção
4. **GitHub Copilot:** Já conhece todo o projeto (use `.github/copilot-instructions.md`)
5. **Cursor AI:** Lê `.ai/cursor-rules.md` automaticamente

---

## 🆘 Precisa de Ajuda?

- **Erros comuns:** [docs/reference/troubleshooting.md](docs/reference/troubleshooting.md)
- **Documentação oficial:** https://weni-ai.github.io/weni-cli/
- **Exemplos completos:** [docs/exemplos/](docs/exemplos/)

---

**Parabéns! 🎉 Você criou seu primeiro agente Weni!**

**Tempo estimado:** 10 minutos  
**Resultado:** Agente funcionando na plataforma

**Próximo desafio:** Integre com uma API real (VTEX, WhatsApp, etc.)
