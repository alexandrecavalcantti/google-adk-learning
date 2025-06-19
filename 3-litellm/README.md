# Exemplo de Agente LiteLLM

## O que é LiteLLM?

LiteLLM é uma biblioteca Python que fornece uma interface unificada para interagir com múltiplos provedores de Modelos de Linguagem Grande (LLM) através de uma única API consistente. Ele serve como um adaptador que permite:

- Usar o mesmo código para acessar mais de 100 LLMs diferentes de provedores como OpenAI, Anthropic, Google, AWS Bedrock e mais
- Padronizar entradas e saídas entre diferentes provedores de LLM
- Rastrear custos, gerenciar chaves de API e lidar com erros de forma consistente
- Implementar fallbacks e balanceamento de carga entre diferentes modelos

Em essência, LiteLLM atua como um wrapper unificado que facilita a troca entre diferentes provedores de LLM sem alterar o código da sua aplicação.

## Por que Usar LiteLLM com ADK?

O Kit de Desenvolvimento de Agentes (ADK) é projetado para ser agnóstico a modelos, significando que pode trabalhar com vários provedores de LLM. LiteLLM aprimora essa capacidade ao:

1. **Flexibilidade de Provedor**: Facilita a troca entre provedores de LLM (OpenAI, Anthropic, etc.) sem alterar o código do seu agente
2. **Otimização de Custo**: Escolha o modelo mais econômico para seu caso de uso específico
3. **Exploração de Modelos**: Experimente com diferentes modelos para encontrar a melhor performance para sua tarefa
4. **À Prova de Futuro**: À medida que novos modelos são lançados, você pode adotá-los rapidamente sem grandes mudanças no código

Este exemplo demonstra como usar LiteLLM com ADK para criar um agente alimentado por modelos através do OpenRouter em vez dos modelos Gemini do Google.

## Limitações ao Usar Modelos Não-Google

Ao usar LiteLLM para integrar modelos não-Google com ADK, há algumas limitações importantes a serem consideradas:

1. **Sem Acesso a Ferramentas Pré-construídas do Google**: Modelos não-Google (como OpenAI, Anthropic, etc.) não podem usar as ferramentas pré-construídas do Google do ADK, tais como:
   - Busca do Google
   - Execução de Código
   - Busca do Vertex AI

2. **Apenas Ferramentas de Função Personalizadas**: Ao usar modelos não-Google, você pode usar apenas ferramentas de função personalizadas (como a função `get_current_time()` neste exemplo).

Essas limitações existem porque as ferramentas pré-construídas são especificamente projetadas para trabalhar com modelos e infraestrutura do Google. No entanto, você ainda pode criar agentes poderosos usando ferramentas de função personalizadas e a ampla variedade de modelos disponíveis através do LiteLLM.

## Compreendendo o Código

Este exemplo demonstra:

1. Como usar o adaptador de modelo `LiteLlm` com ADK
2. Como conectar a modelos através do OpenRouter (especificamente GPT 4.1 Nano)
3. Como criar um agente simples com uma ferramenta personalizada

O agente é configurado para fornecer a hora atual usando uma ferramenta de função personalizada `get_current_time()` e alimentado pelo modelo GPT 4.1 Nano da OpenAI através do OpenRouter em vez do Gemini do Google.

### Exemplos de Prompts para Testar

- "Que horas são agora?"

## Modificando o Exemplo

Você pode facilmente modificar este exemplo para usar diferentes modelos de diferentes provedores através do OpenRouter alterando a configuração `LiteLlm`. Por exemplo:

```python
# Para usar Claude 3.5 Sonnet da Anthropic através do OpenRouter
model = LiteLlm(
    model="openrouter/anthropic/claude-3-5-sonnet",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Para usar GPT-4o da OpenAI através do OpenRouter
model = LiteLlm(
    model="openrouter/openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Para usar Llama 3 70B da Meta através do OpenRouter
model = LiteLlm(
    model="openrouter/meta-llama/meta-llama-3-70b-instruct",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Para usar Mistral Large através do OpenRouter
model = LiteLlm(
    model="openrouter/mistral/mistral-large-latest",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
```

## Recursos Adicionais

- [Documentação de Integração LiteLLM do Google ADK](https://google.github.io/adk-docs/tutorials/agent-team/#step-2-going-multi-model-with-litellm-optional)
- [Documentação LiteLLM](https://docs.litellm.ai/docs/)
- [Provedores Suportados LiteLLM](https://docs.litellm.ai/docs/providers)
- [Documentação OpenRouter](https://openrouter.ai/docs)
- [Visão Geral dos Modelos Anthropic Claude](https://docs.anthropic.com/en/docs/about-claude/models/all-models)