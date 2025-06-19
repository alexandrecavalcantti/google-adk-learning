# Exemplo de Agente com Ferramentas

## O que é um Agente com Ferramentas?

Um Agente com Ferramentas estende o agente básico do ADK incorporando ferramentas que permitem ao agente executar ações além de apenas gerar respostas de texto. As ferramentas habilitam agentes a interagir com sistemas externos, recuperar informações e executar funções específicas para realizar tarefas de forma mais eficaz.

Neste exemplo, demonstramos como construir um agente que pode usar ferramentas pré-construídas (como Busca do Google) e ferramentas de função personalizadas para aprimorar suas capacidades.

## Componentes Principais

### 1. Ferramentas Pré-construídas
O ADK fornece várias ferramentas pré-construídas que você pode usar com seus agentes:

- **Google Search**: Permite que seu agente pesquise informações na web
- **Code Execution**: Habilita seu agente a executar trechos de código
- **Vertex AI Search**: Permite que seu agente pesquise através dos seus próprios dados

**Nota Importante**: Atualmente, para cada agente raiz ou agente único, apenas uma ferramenta pré-construída é suportada. Veja a [documentação do ADK](https://google.github.io/adk-docs/tools/built-in-tools/#use-built-in-tools-with-other-tools) para mais detalhes.

### 2. Ferramentas de Função Personalizadas
Você pode criar suas próprias ferramentas definindo funções Python. Essas ferramentas personalizadas estendem as capacidades do seu agente para executar tarefas específicas.

#### Melhores Práticas para Ferramentas de Função Personalizadas:

- **Parâmetros**: Defina os parâmetros da sua função usando tipos padrão serializáveis em JSON (string, integer, list, dictionary)
- **Sem Valores Padrão**: Valores padrão não são atualmente suportados no ADK
- **Tipo de Retorno**: O tipo de retorno preferido é um dicionário
  - Se você não retornar um dicionário, o ADK o encapsulará em um dicionário `{"result": ...}`
  - Formato de melhor prática: `{"status": "success", "error_message": None, "result": "..."}`
- **Docstrings**: A docstring da função serve como descrição da ferramenta e é enviada para o LLM
  - Foque na clareza para que o LLM entenda como usar a ferramenta eficazmente

## Limitações

Ao trabalhar com ferramentas pré-construídas no ADK, há várias limitações importantes a serem consideradas:

### Restrição de Ferramenta Pré-construída Única

**Atualmente, para cada agente raiz ou agente único, apenas uma ferramenta pré-construída é suportada.**

Por exemplo, esta abordagem usando duas ferramentas pré-construídas dentro de um único agente **não** é atualmente suportada:

```python
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Agente Raiz",
    tools=[built_in_code_execution, google_search],  # NÃO SUPORTADO
)
```

### Ferramentas Pré-construídas vs. Ferramentas Personalizadas

**Você não pode misturar ferramentas pré-construídas com ferramentas de função personalizadas no mesmo agente.**

Por exemplo, esta abordagem **não** é atualmente suportada:

```python
def get_current_time() -> dict:
    """Obter a hora atual no formato YYYY-MM-DD HH:MM:SS"""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

root_agent = Agent(
    name="RootAgent",
    model="gemini-2.5-flash",
    description="Agente Raiz",
    tools=[google_search, get_current_time],  # NÃO SUPORTADO
)
```

Para usar ambos os tipos de ferramentas, você precisaria usar a abordagem de Ferramenta de Agente descrita no exemplo Multi-Agente.

## Exemplo de Implementação

### Compreendendo o Código

O arquivo agent.py define um agente de ferramenta que pode usar a Busca do Google para encontrar informações na web. O agente é configurado com:

1. Um nome e descrição
2. O modelo Gemini a ser usado
3. Instruções que dizem ao agente como se comportar e quais ferramentas pode usar
4. As ferramentas que pode acessar (neste caso, google_search)

O arquivo também inclui um exemplo comentado de uma ferramenta de função personalizada `get_current_time()` que poderia ser descomentada para explorar a funcionalidade de ferramenta personalizada.

### Exemplos de Prompts para Testar

- "Pesquise por notícias recentes sobre inteligência artificial"
- "Encontre informações sobre o Kit de Desenvolvimento de Agentes do Google"
- "Quais são os últimos avanços em computação quântica?"

## Recursos Adicionais

- [Tipos de ferramentas](https://google.github.io/adk-docs/tools/#full-example-tavily-search)
- [Documentação de Ferramentas de Função do ADK](https://google.github.io/adk-docs/tools/function-tools/)
- [Documentação de Ferramentas Pré-construídas do ADK](https://google.github.io/adk-docs/tools/built-in-tools/)