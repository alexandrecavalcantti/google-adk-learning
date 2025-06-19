import asyncio
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()


async def main():
    # `InMemorySessionService` é uma implementação de SessionService que armazena
    # todas as sessões na memória. É ideal para desenvolvimento e testes, mas
    # para produção, é ideal usar outro tipos de serviço de sessões.
    session_service_stateful = InMemorySessionService()

    # 'initial_state' é um dicionário que define o state inicial da sessão.
    # O agente usará estes dados como seu contexto inicial.
    initial_state = {
        'user_name': 'Brandon Hancock',
        'user_preferences': """
            I like to play Pickleball, Disc Golf, and Tennis.
            My favorite food is Mexican.
            My favorite TV show is Game of Thrones.
            Loves it when people like and subscribe to his YouTube channel.
        """,
    }

    # Cada sessão de conversa é unicamente identificada por 'app_name', 'user_id', e 'session_id'.
    APP_NAME = 'Brandon Bot'
    USER_ID = 'brandon_hancock'
    SESSION_ID = str(uuid.uuid4())
    stateful_session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print('NOVA SESSÃO CRIADA:')
    print(f'\tID da Sessão: {SESSION_ID}')

    # No Google ADK, o `Runner` controla todo o fluxo de execução de um agente:
    # ele recebe a mensagem do usuário, inicia o agente, processa as respostas,
    # atualiza o estado da conversa e garante que cada etapa aconteça na ordem certa.
    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )

    new_message = types.Content(
        role='user',
        parts=[
            types.Part(text='Qual é o programa de TV favorito do Brandon?')
        ],
    )

    # `runner.run()` gerencia o "bate-papo interno" entre o agente e os serviços,
    # garantindo que cada passo seja executado na ordem certa e com persistência,
    # usando os IDs para carregar o contexto da sessão.
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        # A iteração processa os eventos gerados pelo agente (ex: respostas parciais, chamadas de ferramenta).
        # Aqui, apenas imprimimos a resposta final.
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f'Resposta Final: {event.content.parts[0].text}')

    print('\n==== Exploração do Estado Final da Sessão ====')
    # Após a conclusão da execução do Runner, podemos recuperar a sessão do
    # `session_service` para inspecionar seu estado final e o histórico de eventos.
    session = await session_service_stateful.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Imprime o estado final da sessão.
    print('=== Estado Final da Sessão ===')
    for key, value in session.state.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    asyncio.run(main())
