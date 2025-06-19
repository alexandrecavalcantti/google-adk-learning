# Armazenamento Persistente no ADK

Este exemplo demonstra como implementar armazenamento persistente para seus agentes ADK, permitindo que eles lembrem informações e mantenham histórico de conversas através de múltiplas sessões, reinicializações da aplicação e até mesmo implantações de servidor.

## O que é Armazenamento Persistente no ADK?

Nos exemplos anteriores, usamos `InMemorySessionService` que armazena dados de sessão apenas na memória - esses dados são perdidos quando a aplicação para. Para aplicações do mundo real, você frequentemente precisará que seus agentes lembrem informações do usuário e histórico de conversas a longo prazo. É aqui que o armazenamento persistente entra.

O ADK fornece o `DatabaseSessionService` que permite armazenar dados de sessão em um banco de dados SQL, garantindo:

1. **Memória de Longo Prazo**: Informações persistem através de reinicializações da aplicação
2. **Experiências de Usuário Consistentes**: Usuários podem continuar conversas de onde pararam
3. **Suporte Multi-usuário**: Dados de diferentes usuários permanecem separados e seguros
4. **Escalabilidade**: Funciona com bancos de dados de produção para implantações de alta escala

Este exemplo mostra como implementar um agente de lembretes que lembra seu nome e tarefas através de diferentes conversas usando um banco de dados SQLite.

## Estrutura do Projeto

```
6-persistent-storage/
│
├── memory_agent/               # Pacote do agente
│   ├── __init__.py             # Obrigatório para o ADK descobrir o agente
│   └── agent.py                # Definição do agente com ferramentas de lembretes
│
├── main.py                     # Ponto de entrada da aplicação com configuração de sessão de banco
├── utils.py                    # Funções utilitárias para UI do terminal e interação do agente
├── .env                        # Variáveis de ambiente
├── my_agent_data.db            # Arquivo de banco SQLite (criado na primeira execução)
└── README.md                   # Esta documentação
```

## Componentes Principais

### 1. DatabaseSessionService

O componente central que fornece persistência é o `DatabaseSessionService`, que é inicializado com uma URL de banco de dados:

```python
from google.adk.sessions import DatabaseSessionService

db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)
```

Este serviço permite ao ADK:
- Armazenar dados de sessão em um arquivo de banco SQLite
- Recuperar sessões anteriores para um usuário
- Gerenciar automaticamente esquemas de banco de dados

### 2. Gerenciamento de Sessão

O exemplo demonstra gerenciamento adequado de sessão:

```python
# Verificar sessões existentes para este usuário
existing_sessions = session_service.list_sessions(
    app_name=APP_NAME,
    user_id=USER_ID,
)

# Se há uma sessão existente, use-a, senão crie uma nova
if existing_sessions and len(existing_sessions.sessions) > 0:
    # Use a sessão mais recente
    SESSION_ID = existing_sessions.sessions[0].id
    print(f"Continuando sessão existente: {SESSION_ID}")
else:
    # Criar uma nova sessão com estado inicial
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initialize_state(),
    )
```

### 3. Gerenciamento de Estado com Ferramentas

O agente inclui ferramentas que atualizam o estado persistente:

```python
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    # Obter lembretes atuais do estado
    reminders = tool_context.state.get("reminders", [])
    
    # Adicionar o novo lembrete
    reminders.append(reminder)
    
    # Atualizar estado com a nova lista de lembretes
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Lembrete adicionado: {reminder}",
    }
```

Cada mudança em `tool_context.state` é automaticamente salva no banco de dados.

## Exemplos de Interações

Experimente estas interações para testar a memória persistente do agente:

1. **Primeira execução:**
   - "Qual é o meu nome?"
   - "Meu nome é João"
   - "Adicione um lembrete para comprar mantimentos"
   - "Adicione outro lembrete para terminar o relatório"
   - "Quais são os meus lembretes?"
   - Saia do programa com "exit"

2. **Segunda execução:**
   - "Qual é o meu nome?"
   - "Que lembretes eu tenho?"
   - "Atualize meu segundo lembrete para entregar o relatório até sexta-feira"
   - "Delete o primeiro lembrete"
   
O agente lembrará seu nome e lembretes entre execuções!

## Usando Armazenamento de Banco em Produção

Embora este exemplo use SQLite por simplicidade, `DatabaseSessionService` suporta vários backends de banco de dados através do SQLAlchemy:

- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`
- MS SQL Server: `mssql://user:password@localhost/dbname`

Para uso em produção:
1. Escolha um sistema de banco de dados que atenda suas necessidades de escalabilidade
2. Configure pooling de conexão para eficiência
3. Implemente segurança adequada para credenciais de banco de dados
4. Considere backups de banco de dados para dados críticos do agente

## Recursos Adicionais

- [Documentação de Sessões do ADK](https://google.github.io/adk-docs/sessions/session/)
- [Implementações de Session Service](https://google.github.io/adk-docs/sessions/session/#sessionservice-implementations)
- [Gerenciamento de Estado no ADK](https://google.github.io/adk-docs/sessions/state/)
- [Documentação SQLAlchemy](https://docs.sqlalchemy.org/) para configuração avançada de banco de dados 