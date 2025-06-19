from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


# Define a estrutura de dados desejada para a saída do LLM.
class EmailContent(BaseModel):
    """Representa o conteúdo estruturado de um e-mail."""

    subject: str = Field(
        description='A linha de assunto do e-mail. Deve ser concisa e descritiva.'
    )
    body: str = Field(
        description='O conteúdo principal do e-mail. Deve ser bem formatado com saudação, parágrafos e assinatura adequados.'
    )


root_agent = LlmAgent(
    name='email_agent',
    model='gemini-2.5-flash',
    # A instrução é FUNDAMENTAL para guiar o agente. Sempre inclua UMA PARTE CLARA
    # na instrução especificando o modelo de saída desejado. isso ajuda a IA a
    # entender exatamente como deve estruturar a resposta, reduz drasticamente a
    # chance de erros de formatação, diminui o número de tentativas necessárias
    # (retries) e evita respostas fora do padrão ("crashs" de parsing). Quando a
    # LLM sabe qual é o modelo de saída esperado, ela tem MUITO MAIS CHANCE de
    # gerar um resultado válido de primeira, o que otimiza o fluxo da aplicação.
    instruction="""
        Você é um Assistente de Geração de E-mail.
        Sua tarefa é gerar um e-mail profissional com base na solicitação do usuário.

        DIRETRIZES:
        - Crie uma linha de assunto apropriada (concisa e relevante)
        - Escreva um corpo de e-mail bem estruturado com:
            * Saudação profissional
            * Conteúdo principal claro e conciso
            * Encerramento apropriado
            * Seu nome como assinatura
        - O tom do e-mail deve corresponder ao propósito (formal para negócios, amigável para colegas)
        - Mantenha os e-mails concisos, mas completos

        IMPORTANTE: Sua resposta DEVE ser um JSON válido que corresponda a esta estrutura:
        {
            "subject": "Assunto aqui",
            "body": "Corpo do e-mail aqui com parágrafos e formatação adequados",
        }

        NÃO inclua nenhuma explicação ou texto adicional fora da resposta JSON.
    """,
    description='Gera e-mails profissionais com assunto e corpo estruturados',
    # 'output_schema' informa ao agente qual é a estrutura de saída esperada.
    # IMPORTANTE: Um agente que define um 'output_schema' para saídas estruturadas
    # não pode ter o parâmetro 'tools' definido ao mesmo tempo e não pode passar o
    # controle para outros agentes.
    output_schema=EmailContent,
    # 'output_key' define a chave sob a qual a resposta JSON validada
    # será armazenada no estado da sessão para uso posterior.
    output_key='email',
)
