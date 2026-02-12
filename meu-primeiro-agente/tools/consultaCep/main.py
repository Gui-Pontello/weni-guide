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
