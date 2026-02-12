# ✅ Checklist - Primeiro Deploy Weni

Use este checklist para garantir que tudo está pronto antes de fazer o primeiro deploy.

---

## 📋 Pré-Requisitos

- [ ] Python 3.8+ instalado (`python --version`)
- [ ] **Conectado na rede da empresa** (VPN ou presencial) - necessário para login CLI
- [ ] Acesso à plataforma Weni (credenciais válidas)

---

## 🛠️ Setup Inicial (Fazer 1 vez)

- [ ] Instalar Weni CLI: `pip install weni-cli`
- [ ] Verificar instalação: `weni --version`
- [ ] Fazer login: `weni login`
  - [ ] Navegador abre automaticamente
  - [ ] Fazer login no site
  - [ ] Autorizar CLI
  - [ ] Ver mensagem: "Successfully logged in"
- [ ] Testar autenticação: `weni project list`

**⚠️ Importante:** Se der erro SSL, você precisa estar **conectado na rede da empresa**.

---

## 📁 Criar Agente (Para cada novo agente)

- [ ] Criar pasta: `mkdir meu-agente`
- [ ] Navegar: `cd meu-agente`
- [ ] Criar `agent_definition.yaml`
- [ ] Criar estrutura `tools/nomeTool/main.py`
- [ ] Criar `tools/nomeTool/requirements.txt` (se necessário)
- [ ] Testar localmente (se CLI suportar)

---

## 🚀 Deploy

- [ ] Listar projetos: `weni project list`
- [ ] Selecionar projeto: `weni project use <PROJECT_ID>`
- [ ] Fazer push: `weni project push`
- [ ] Aguardar confirmação de sucesso
- [ ] Anotar URL do agente retornada

---

## ✅ Validação

- [ ] Acessar dashboard: https://dash.weni.ai (ou URL da sua empresa)
- [ ] Encontrar agente na lista
- [ ] Testar no chat interno
- [ ] Verificar logs: `weni logs --follow`

---

## 🐛 Troubleshooting

### Login falha com SSL Error
**Problema:** `SSLCertVerificationError: certificate verify failed`  
**Solução:** Conecte-se na rede corporativa (VPN ou presencial)

### "Missing login authorization"
**Problema:** Token expirado ou não autenticado  
**Solução:** Execute `weni login` novamente

### "weni: command not found"
**Problema:** CLI não no PATH  
**Solução:** Use caminho completo ou `python -m weni`

### "No such command"
**Problema:** Comando não existe  
**Solução:** Verifique `weni --help` para comandos disponíveis

---

## 📝 Comandos Rápidos

```bash
# Login inicial
weni login

# Ver projetos
weni project list

# Usar projeto
weni project use <ID>

# Deploy agente
weni project push

# Ver logs
weni logs --follow

# Ajuda
weni --help
```

---

## 🎯 Próximos Passos Após Primeiro Deploy

1. [ ] Testar agente no dashboard
2. [ ] Integrar com canal (WhatsApp, etc.)
3. [ ] Configurar variáveis de ambiente
4. [ ] Documentar fluxos do agente
5. [ ] Criar testes automatizados

---

**Última atualização:** 12/02/2026  
**Status:** Testado e validado
