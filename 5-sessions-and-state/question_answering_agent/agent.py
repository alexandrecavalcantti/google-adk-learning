from google.adk.agents import LlmAgent

question_answering_agent = LlmAgent(
    name='question_answering_agent',
    model='gemini-2.5-flash',
    description='Agente de resposta a perguntas',
    # A instrução contém placeholders como {user_name} e {user_preferences}.
    # O ADK os substitui automaticamente pelos valores do estado da sessão
    # durante a execução, permitindo que o agente seja ciente do contexto.
    instruction="""
    Você é um assistente prestativo que responde a perguntas sobre as preferências do usuário.

    Aqui estão algumas informações sobre o usuário:
    Nome:
    {user_name}
    Preferências:
    {user_preferences}
    """,
)
