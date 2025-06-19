from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name='google_search_agent',
    model='gemini-2.5-flash',
    description='Um agente que pode pesquisar qualquer informação no Google',
    instruction="""
    Você é um assistente prestativo que pode usar as seguintes ferramentas:
    - google_search
    """,
    # O parâmetro 'tools' recebe uma lista de ferramentas que o agente pode chamar.
    # IMPORTANTE: Um agente pode ter ferramentas pré-construídas (como google_search)
    # OU ferramentas personalizadas (funções Python), mas não ambas ao mesmo tempo.
    tools=[google_search],
)
