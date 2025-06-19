from google.adk.agents import Agent

# Cria uma instância de um agente. No Google ADK, um "Agent" é a unidade fundamental
# que encapsula um modelo de linguagem (LLM) e a lógica para interagir com ele.
root_agent = Agent(
    # 'name' é um identificador único para o agente.
    name='greeting_agent',
    # 'model' especifica qual modelo de linguagem o agente usará.
    model='gemini-2.5-flash',
    # 'description' fornece uma breve explicação sobre a finalidade do agente
    # e é usado para que outros agentes possam entender o que ele faz.
    description='Agente de saudação',
    # 'instruction' é o prompt do sistema que define o comportamento do agente.
    instruction="""
    Você é um assistente prestativo que cumprimenta o usuário.
    Pergunte o nome do usuário e cumprimente-o pelo nome.
    """,
)
