# Exemplo de Agente Básico ADK

## O que é um Agente ADK?

O `LlmAgent` (frequentemente chamado simplesmente de `Agent`) é um componente central no ADK que atua como a parte "pensante" da sua aplicação. Ele aproveita o poder de um Modelo de Linguagem Grande (LLM) para:
- Raciocínio
- Compreensão de linguagem natural
- Tomada de decisões
- Geração de respostas
- Interação com ferramentas

Ao contrário de agentes de fluxo de trabalho determinísticos que seguem caminhos predefinidos, o comportamento de um `LlmAgent` é não-determinístico. Ele usa o LLM para interpretar instruções e contexto, decidindo dinamicamente como proceder, quais ferramentas usar (se houver), ou se deve transferir o controle para outro agente.

## Estrutura Obrigatória do Agente

Para que o ADK descubra e execute seus agentes adequadamente (especialmente com `adk web`), seu projeto deve seguir uma estrutura específica:

```
pasta_pai/
    pasta_agente/         # Este é o diretório do pacote do seu agente
        __init__.py       # Deve importar agent.py
        agent.py          # Deve definir root_agent
        .env              # Variáveis de ambiente
```

### Componentes Essenciais:

1. **`__init__.py`**
   - Deve importar o módulo do agente: `from . import agent`
   - Isso torna seu agente descobrível pelo ADK

2. **`agent.py`**
   - Deve definir uma variável chamada `root_agent`
   - Este é o ponto de entrada que o ADK usa para encontrar seu agente

3. **Localização dos Comandos**
   - Sempre execute comandos `adk` do diretório pai, não de dentro do diretório do agente
   - Exemplo: Execute `adk web` da pasta pai que contém a pasta do seu agente

Esta estrutura garante que o ADK possa descobrir e carregar automaticamente seu agente ao executar comandos como `adk web` ou `adk run`.

## Componentes Principais

### 1. Identidade (`name` e `description`)
- **name** (Obrigatório): Um identificador de string único para seu agente
- **description** (Opcional, mas recomendado): Um resumo conciso das capacidades do agente. Usado para outros agentes determinarem se devem encaminhar uma tarefa para este agente.

### 2. Modelo (`model`)
- Especifica qual LLM alimenta o agente (ex: "gemini-2.5-flash")
- Afeta as capacidades, custo e desempenho do agente

### 3. Instruções (`instruction`)
O parâmetro mais crítico para moldar o comportamento do seu agente. Ele define:
- Tarefa ou objetivo principal
- Personalidade ou persona
- Restrições comportamentais
- Como usar ferramentas disponíveis
- Formato de saída desejado

### 4. Ferramentas (`tools`)
Capacidades opcionais além do conhecimento embutido do LLM, permitindo que o agente:
- Interaja com sistemas externos
- Execute cálculos
- Busque dados em tempo real
- Execute ações específicas

## Executando o Exemplo

Para executar este exemplo de agente básico, você usará a ferramenta CLI do ADK que oferece várias maneiras de interagir com seu agente:

1. Navegue até o diretório 1-basic-agent contendo a pasta do seu agente.
2. Inicie a interface web interativa:
```bash
adk web
```

3. Acesse a interface web abrindo a URL mostrada no seu terminal (normalmente http://localhost:8000)

4. Selecione seu agente no menu suspenso no canto superior esquerdo da interface

5. Comece a conversar com seu agente na caixa de texto na parte inferior da tela

### Solução de Problemas

Se seu agente não aparecer no menu suspenso:
- Certifique-se de executar `adk web` do diretório pai (1-basic-agent), não de dentro do diretório do agente
- Verifique se seu `__init__.py` importa adequadamente o módulo do agente
- Confirme se `agent.py` define uma variável chamada `root_agent`

### Métodos Alternativos de Execução

A ferramenta CLI do ADK oferece várias opções:

- **`adk web`**: Lança uma interface web interativa para testar seu agente com uma interface de chat
- **`adk run [nome_agente]`**: Executa seu agente diretamente no terminal
- **`adk api_server`**: Inicia um servidor FastAPI para testar requisições de API para seu agente

Você pode sair da conversa ou parar o servidor pressionando `Ctrl+C` no seu terminal.

Este exemplo demonstra um agente simples que responde a consultas relacionadas a saudações, mostrando os fundamentos da criação de agentes com ADK.