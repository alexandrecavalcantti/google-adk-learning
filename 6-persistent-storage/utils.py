from google.genai import types


# Códigos de cores ANSI para saída colorida no terminal
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Cores de texto
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Cores de fundo
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


async def display_state(
    session_service, app_name, user_id, session_id, label='Current State'
):
    """Exibe o estado atual da sessão de forma formatada."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Formata a saída com seções claras
        print(f'\n{"-" * 10} {label} {"-" * 10}')

        # Exibe o nome do usuário
        user_name = session.state.get('user_name', 'Unknown')
        print(f'👤 Usuário: {user_name}')

        # Exibe os lembretes
        reminders = session.state.get('reminders', [])
        if reminders:
            print('📝 Lembretes:')
            for idx, reminder in enumerate(reminders, 1):
                print(f'  {idx}. {reminder}')
        else:
            print('📝 Lembretes: Nenhum')

        print('-' * (22 + len(label)))
    except Exception as e:
        print(f'Erro ao exibir estado: {e}')


async def process_agent_response(event):
    """Processa e exibe eventos de resposta do agente."""
    # Log de informações básicas do evento
    print(f'ID do Evento: {event.id}, Autor: {event.author}')

    # Verifica tipos específicos de partes primeiro
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, 'executable_code') and part.executable_code:
                # Acessa o código real via .code
                print(
                    f'  Debug: Agente gerou código:\n```python\n{part.executable_code.code}\n```'
                )
                has_specific_part = True
            elif (
                hasattr(part, 'code_execution_result')
                and part.code_execution_result
            ):
                # Acessa resultado e saída corretamente
                print(
                    f'  Debug: Resultado da Execução: {part.code_execution_result.outcome} - Saída:\n{part.code_execution_result.output}'
                )
                has_specific_part = True
            elif hasattr(part, 'tool_response') and part.tool_response:
                # Imprime informações da resposta da ferramenta
                print(f'  Resposta da Ferramenta: {part.tool_response.output}')
                has_specific_part = True
            # Também imprime qualquer parte de texto encontrada em qualquer evento para debug
            elif (
                hasattr(part, 'text') and part.text and not part.text.isspace()
            ):
                print(f"  Texto: '{part.text.strip()}'")

    # Verifica resposta final após partes específicas
    final_response = None
    if event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], 'text')
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # Usa cores e formatação para destacar a resposta final
            print(
                f'\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ RESPOSTA DO AGENTE ═════════════════════════════════════════{Colors.RESET}'
            )
            print(f'{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}')
            print(
                f'{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n'
            )
        else:
            print(
                f'\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Resposta Final do Agente: [Sem conteúdo de texto no evento final]{Colors.RESET}\n'
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Chama o agente de forma assíncrona com a consulta do usuário."""
    content = types.Content(role='user', parts=[types.Part(text=query)])
    print(
        f'\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Executando Consulta: {query} ---{Colors.RESET}'
    )
    final_response_text = None

    # Exibe estado antes do processamento
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        'Estado ANTES do processamento',
    )

    try:
        # O Google ADK recomenda sempre usar 'run_async' ao invés de 'run' para melhor performance.
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Processa cada evento e obtém a resposta final se disponível
            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f'Erro durante chamada do agente: {e}')

    # Exibe estado após processar a mensagem
    await display_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        'Estado DEPOIS do processamento',
    )

    return final_response_text
