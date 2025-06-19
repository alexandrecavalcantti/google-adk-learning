# Sessões e Gerenciamento de Estado no ADK

Este exemplo demonstra como criar e gerenciar sessões com estado no Kit de Desenvolvimento de Agentes (ADK), permitindo que seus agentes mantenham contexto e lembrem informações do usuário entre interações.

## O que são Sessões no ADK?

Sessões no ADK fornecem uma maneira de:

1. **Manter Estado**: Armazenar e acessar dados do usuário, preferências e outras informações entre interações
2. **Rastrear Histórico de Conversas**: Automaticamente registrar e recuperar histórico de mensagens
3. **Personalizar Respostas**: Usar informações armazenadas para criar experiências de agente mais contextuais e personalizadas

Ao contrário de agentes conversacionais simples que esquecem interações anteriores, agentes com estado podem construir relacionamentos com usuários ao longo do tempo lembrando detalhes e preferências importantes.

## Visão Geral do Exemplo

Este diretório contém um exemplo básico de sessão com estado que demonstra:

- Criar uma sessão com preferências do usuário
- Usar variáveis de template para acessar estado da sessão nas instruções do agente
- Executar o agente com uma sessão para manter contexto

O exemplo usa um agente simples de perguntas e respostas que responde baseado em informações do usuário armazenadas no estado da sessão.

## Estrutura do Projeto

```
5-sessions-and-state/
│
├── basic_stateful_session.py      # Script de exemplo principal
│
└── question_answering_agent/      # Implementação do agente
    ├── __init__.py
    └── agent.py                   # Definição do agente com variáveis de template
```

## Componentes Principais

### Serviço de Sessão

O exemplo usa o `InMemorySessionService` que armazena sessões na memória:

```python
session_service = InMemorySessionService()
```

### Estado Inicial

Sessões são criadas com um estado inicial contendo informações do usuário:

```python
initial_state = {
    "user_name": "Brandon Hancock",
    "user_preferences": """
        Gosto de jogar Pickleball, Disc Golf e Tênis.
        Minha comida favorita é mexicana.
        Meu programa de TV favorito é Game of Thrones.
        Adora quando as pessoas curtem e se inscrevem no seu canal do YouTube.
    """,
}
```

### Criando uma Sessão

O exemplo cria uma sessão com um identificador único:

```python
stateful_session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
```

### Acessando Estado nas Instruções do Agente

O agente acessa o estado da sessão usando variáveis de template em suas instruções:

```python
instruction="""
Você é um assistente prestativo que responde a perguntas sobre as preferências do usuário.

Aqui estão algumas informações sobre o usuário:
Nome: 
{user_name}
Preferências: 
{user_preferences}
"""
```

### Executando com Sessões

Sessões são integradas com o `Runner` para manter estado entre interações:

```python
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
```

## Recursos Adicionais

- [Documentação de Sessões do Google ADK](https://google.github.io/adk-docs/sessions/session/)
- [Gerenciamento de Estado no ADK](https://google.github.io/adk-docs/sessions/state/)