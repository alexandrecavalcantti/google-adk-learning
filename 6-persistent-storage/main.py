import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async

load_dotenv()

# ===== PARTE 1: Inicializar Serviço de Sessão Persistente =====
# Usando banco de dados SQLite para armazenamento persistente.
# O arquivo será criado automaticamente se não existir.
db_url = 'sqlite:///./my_agent_data.db'
session_service = DatabaseSessionService(db_url=db_url)

# ===== PARTE 2: Definir Estado Inicial =====
# Será usado apenas ao criar uma nova sessão.
# Se uma sessão já existir, este estado será ignorado.
initial_state = {
    'user_name': 'Alexandre Cavalcanti',
    'reminders': [],
}


async def main_async():
    # Configurar constantes
    APP_NAME = 'Memory Agent'
    USER_ID = 'alexandrecavalcanti'

    # ===== PARTE 3: Gerenciamento de Sessão - Encontrar ou Criar =====
    # Verifica se existem sessões para este usuário
    existing_sessions = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # Se houver uma sessão existente, usa ela, senão cria uma nova
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Usa a sessão mais recente
        SESSION_ID = existing_sessions.sessions[0].id
        print(f'Continuando sessão existente: {SESSION_ID}')
    else:
        # Cria uma nova sessão com estado inicial
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f'Nova sessão criada: {SESSION_ID}')

    # ===== PARTE 4: Configuração do Runner do Agente =====
    # Cria um runner com o agente de memória.
    # O DatabaseSessionService garante que todas as mudanças sejam persistidas.
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PARTE 5: Loop de Conversa Interativo =====
    print('\nBem-vindo ao Memory Agent Chat!')
    print('Seus lembretes serão lembrados entre conversas.')
    print("Digite 'exit' ou 'quit' para encerrar a conversa.\n")

    while True:
        # Captura entrada do usuário
        user_input = input('Você: ')

        # Verifica se o usuário quer sair
        if user_input.lower() in ['exit', 'quit']:
            print(
                'Encerrando conversa. Seus dados foram salvos no banco de dados.'
            )
            break

        # Processa a consulta do usuário através do agente
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)


if __name__ == '__main__':
    asyncio.run(main_async())
