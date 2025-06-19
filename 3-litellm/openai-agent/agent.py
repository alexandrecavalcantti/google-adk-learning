import os
from datetime import datetime

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


def get_current_time() -> dict:
    """Retorna a hora atual no formato YYYY-MM-DD HH:MM:SS."""
    return {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


# Para usar um modelo de outro provedor, instanciamos a classe 'LiteLlm'.
model = LiteLlm(
    # 'model' especifica o modelo que você deseja usar.
    model='openrouter/openai/gpt-4.1-nano',
    api_key=os.getenv('OPENROUTER_API_KEY'),
)

root_agent = Agent(
    name='openai_agent',
    model=model,
    description='Um agente que usa o OpenAI GPT 4.1 Nano como LLM',
    instruction="""
    Você é um assistente prestativo que pode usar as seguintes ferramentas:
    - get_current_time
    """,
    tools=[get_current_time],
)
