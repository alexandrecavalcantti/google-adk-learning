from datetime import datetime

from google.adk.agents import Agent


def get_current_time() -> dict:
    """Retorna a hora atual no formato YYYY-MM-DD HH:MM:SS."""
    # É crucial especificar o tipo de retorno da ferramenta (-> dict) e garantir
    # que a saída seja um dicionário. Se a função retornasse um valor que não seja
    # um dicionário (ex: uma string), o ADK o encapsularia em um dicionário genérico
    # como {'result': 'resultado da tool'}, o que pode ser menos descritivo para o LLM.
    # Retornar um dicionário com chaves bem nomeadas (como 'current_time')
    # fornece um contexto muito mais rico, melhorando o funcionamento do agente.
    return {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


root_agent = Agent(
    name='get_current_time_agent',
    model='gemini-2.5-flash',
    description='Um agente que fornece a hora atual',
    instruction="""
    Você é um assistente prestativo que pode usar as seguintes ferramentas:
    - get_current_time_agent
    """,
    # O parâmetro 'tools' recebe uma lista de ferramentas que o agente pode chamar.
    # IMPORTANTE: Um agente pode ter ferramentas personalizadas (funções Python, como esta)
    # OU ferramentas pré-construídas (como google_search), mas não ambas ao mesmo tempo.
    tools=[get_current_time],
)
