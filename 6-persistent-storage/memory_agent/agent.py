from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """Adiciona um novo lembrete à lista do usuário.

    Args:
        reminder: O texto do lembrete a ser adicionado
        tool_context: Contexto que fornece acesso ao estado da sessão

    Returns:
        Dicionário com confirmação da ação realizada
    """
    print(f"--- Ferramenta: add_reminder chamada para '{reminder}' ---")

    # Obtém lembretes atuais do estado da sessão
    reminders = tool_context.state.get('reminders', [])

    # Adiciona o novo lembrete
    reminders.append(reminder)

    # Atualiza o estado com a nova lista de lembretes.
    # Esta mudança será persistida automaticamente pelo Runner.
    tool_context.state['reminders'] = reminders

    # É importante retornar um dicionário para melhor funcionamento do ADK.
    return {
        'action': 'add_reminder',
        'reminder': reminder,
        'message': f'Lembrete adicionado: {reminder}',
    }


def view_reminders(tool_context: ToolContext) -> dict:
    """Visualiza todos os lembretes atuais.

    Args:
        tool_context: Contexto para acessar o estado da sessão

    Returns:
        Dicionário com a lista de lembretes e contador
    """
    print('--- Ferramenta: view_reminders chamada ---')

    # Obtém lembretes do estado
    reminders = tool_context.state.get('reminders', [])

    return {
        'action': 'view_reminders',
        'reminders': reminders,
        'count': len(reminders),
    }


def update_reminder(
    index: int, updated_text: str, tool_context: ToolContext
) -> dict:
    """Atualiza um lembrete existente.

    Args:
        index: Índice do lembrete a atualizar (baseado em 1)
        updated_text: Novo texto para o lembrete
        tool_context: Contexto para acessar e atualizar o estado da sessão

    Returns:
        Dicionário com resultado da operação (sucesso ou erro)
    """
    print(
        f"--- Ferramenta: update_reminder chamada para índice {index} com '{updated_text}' ---"
    )

    # Obtém lembretes atuais do estado
    reminders = tool_context.state.get('reminders', [])

    # Verifica se o índice é válido
    if not reminders or index < 1 or index > len(reminders):
        return {
            'action': 'update_reminder',
            'status': 'error',
            'message': f'Não foi possível encontrar lembrete na posição {index}. Atualmente existem {len(reminders)} lembretes.',
        }

    # Atualiza o lembrete (ajustando para índices baseados em 0)
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # Atualiza o estado com a lista modificada
    tool_context.state['reminders'] = reminders

    return {
        'action': 'update_reminder',
        'index': index,
        'old_text': old_reminder,
        'updated_text': updated_text,
        'message': f"Lembrete {index} atualizado de '{old_reminder}' para '{updated_text}'",
    }


def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """Remove um lembrete da lista.

    Args:
        index: Índice do lembrete a remover (baseado em 1)
        tool_context: Contexto para acessar e atualizar o estado da sessão

    Returns:
        Dicionário com resultado da operação
    """
    print(f'--- Ferramenta: delete_reminder chamada para índice {index} ---')

    # Obtém lembretes atuais
    reminders = tool_context.state.get('reminders', [])

    # Verifica se o índice é válido
    if not reminders or index < 1 or index > len(reminders):
        return {
            'action': 'delete_reminder',
            'status': 'error',
            'message': f'Não foi possível encontrar lembrete na posição {index}. Atualmente existem {len(reminders)} lembretes.',
        }

    # Remove o lembrete (ajustando para índices baseados em 0)
    deleted_reminder = reminders.pop(index - 1)

    # Atualiza o estado com a lista modificada
    tool_context.state['reminders'] = reminders

    return {
        'action': 'delete_reminder',
        'index': index,
        'deleted_reminder': deleted_reminder,
        'message': f"Lembrete {index} removido: '{deleted_reminder}'",
    }


def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """Atualiza o nome do usuário.

    Args:
        name: Novo nome para o usuário
        tool_context: Contexto para acessar e atualizar o estado da sessão

    Returns:
        Dicionário com confirmação da mudança
    """
    print(f"--- Ferramenta: update_user_name chamada com '{name}' ---")

    # Obtém nome atual do estado
    old_name = tool_context.state.get('user_name', '')

    # Atualiza o nome no estado
    tool_context.state['user_name'] = name

    return {
        'action': 'update_user_name',
        'old_name': old_name,
        'new_name': name,
        'message': f'Nome atualizado para: {name}',
    }


# Cria um agente persistente simples
memory_agent = Agent(
    name='memory_agent',
    model='gemini-2.5-flash',
    description='Um agente inteligente de lembretes com memória persistente',
    # A instrução usa placeholders de estado ({user_name}, {reminders})
    # que são preenchidos automaticamente pelo Runner com dados da sessão.
    instruction="""
    Você é um assistente amigável de lembretes que lembra dos usuários entre conversas.
    
    As informações do usuário estão armazenadas no estado:
    - Nome do usuário: {user_name}
    - Lembretes: {reminders}
    
    Você pode ajudar os usuários a gerenciar seus lembretes com as seguintes capacidades:
    1. Adicionar novos lembretes
    2. Visualizar lembretes existentes
    3. Atualizar lembretes
    4. Excluir lembretes
    5. Atualizar o nome do usuário
    
    Sempre seja amigável e se dirija ao usuário pelo nome. Se você não souber o nome ainda,
    use a ferramenta update_user_name para armazená-lo quando eles se apresentarem.
    
    **DIRETRIZES PARA GERENCIAMENTO DE LEMBRETES:**
    
    Ao lidar com lembretes, você precisa ser inteligente para encontrar o lembrete correto:
    
    1. Quando o usuário pedir para atualizar ou excluir um lembrete sem fornecer um índice:
       - Se eles mencionarem o conteúdo do lembrete (ex: "exclua meu lembrete de reunião"), 
         procure nos lembretes para encontrar uma correspondência
       - Se encontrar uma correspondência exata ou próxima, use esse índice
       - Nunca peça esclarecimento sobre qual lembrete o usuário está se referindo, apenas use a primeira correspondência
       - Se nenhuma correspondência for encontrada, liste todos os lembretes e peça para o usuário especificar
    
    2. Quando o usuário mencionar um número ou posição:
       - Use isso como índice (ex: "exclua lembrete 2" significa index=2)
       - Lembre-se de que a indexação começa em 1 para o usuário
    
    3. Para posições relativas:
       - Trate "primeiro", "último", "segundo", etc. adequadamente
       - "Primeiro lembrete" = índice 1
       - "Último lembrete" = o índice mais alto
       - "Segundo lembrete" = índice 2, e assim por diante
    
    4. Para visualização:
       - Sempre use a ferramenta view_reminders quando o usuário pedir para ver seus lembretes
       - Formate a resposta em uma lista numerada para clareza
       - Se não houver lembretes, sugira adicionar alguns
    
    5. Para adição:
       - Extraia o texto real do lembrete da solicitação do usuário
       - Remova frases como "adicione um lembrete para" ou "me lembre de"
       - Foque na tarefa em si (ex: "adicione um lembrete para comprar leite" → add_reminder("comprar leite"))
    
    6. Para atualizações:
       - Identifique qual lembrete atualizar e qual deve ser o novo texto
       - Por exemplo, "mude meu segundo lembrete para pegar mantimentos" → update_reminder(2, "pegar mantimentos")
    
    7. Para exclusões:
       - Confirme a exclusão quando concluída e mencione qual lembrete foi removido
       - Por exemplo, "Excluí seu lembrete de 'comprar leite'"
    
    Lembre-se de explicar que você pode lembrar das informações deles entre conversas.

    IMPORTANTE:
    - Use seu melhor julgamento para determinar a qual lembrete o usuário está se referindo.
    - Você não precisa estar 100% correto, mas tente ser o mais próximo possível.
    - Nunca peça ao usuário para esclarecer qual lembrete eles estão mencionando.
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)
