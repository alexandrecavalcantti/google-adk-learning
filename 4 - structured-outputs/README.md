# Saídas Estruturadas no ADK

Este exemplo demonstra como implementar saídas estruturadas no Kit de Desenvolvimento de Agentes (ADK) usando modelos Pydantic. O agente principal neste exemplo, `email_agent`, usa o parâmetro `output_schema` para garantir que suas respostas estejam em conformidade com um formato estruturado específico.

## O que são Saídas Estruturadas?

O ADK permite que você defina formatos de dados estruturados para entradas e saídas de agentes usando modelos Pydantic:

1. **Formato de Saída Controlado**: Usar `output_schema` garante que o LLM produza respostas em uma estrutura JSON consistente
2. **Validação de Dados**: Pydantic valida que todos os campos obrigatórios estão presentes e corretamente formatados
3. **Processamento Downstream Melhorado**: Saídas estruturadas são mais fáceis de lidar em aplicações downstream ou por outros agentes

Use saídas estruturadas quando precisar de consistência de formato garantida para integração com outros sistemas ou agentes.

## Exemplo de Gerador de E-mail

Neste exemplo, criamos um agente gerador de e-mail que produz saída estruturada com:

1. **Assunto do E-mail**: Uma linha de assunto concisa e relevante
2. **Corpo do E-mail**: Conteúdo de e-mail bem formatado com saudação, parágrafos e assinatura

O agente usa um modelo Pydantic chamado `EmailContent` para definir esta estrutura, garantindo que toda resposta siga o mesmo formato.

### Definição do Schema de Saída

O modelo Pydantic define exatamente quais campos são obrigatórios e inclui descrições para cada um:

```python
class EmailContent(BaseModel):
    """Schema para conteúdo de e-mail com assunto e corpo."""
    
    subject: str = Field(
        description="A linha de assunto do e-mail. Deve ser concisa e descritiva."
    )
    body: str = Field(
        description="O conteúdo principal do e-mail. Deve ser bem formatado com saudação, parágrafos e assinatura adequados."
    )
```

### Como Funciona

1. O usuário fornece uma descrição do e-mail que precisa
2. O agente LLM processa esta solicitação e gera tanto assunto quanto corpo
3. O agente formata sua resposta como um objeto JSON correspondente ao schema `EmailContent`
4. O ADK valida a resposta contra o schema antes de retorná-la
5. A saída estruturada é armazenada no estado da sessão sob a `output_key` especificada

## Limitações Importantes

Ao usar `output_schema`:

1. **Sem Uso de Ferramentas**: Agentes com um schema de saída não podem usar ferramentas durante sua execução
2. **Resposta JSON Direta**: O LLM deve produzir uma resposta JSON correspondente ao schema como sua saída final
3. **Instruções Claras**: As instruções do agente devem orientar explicitamente o LLM a produzir JSON adequadamente formatado

## Estrutura do Projeto

```
4-structured-outputs/
│
├── email_agent/                   # Pacote do Agente Gerador de E-mail
│   └── agent.py                   # Definição do agente com schema de saída
│
└── README.md                      # Esta documentação
```

## Exemplos de Interações

Experimente estes prompts de exemplo:

```
Escreva um e-mail profissional para minha equipe sobre o prazo do projeto que foi estendido por duas semanas.
```

```
Rascunhe um e-mail para um cliente explicando que precisamos de informações adicionais antes de prosseguir com seu pedido.
```

```
Crie um e-mail para agendar uma reunião com o departamento de marketing para discutir a estratégia de lançamento do novo produto.
```

## Conceitos Principais: Troca de Dados Estruturados

Saídas estruturadas fazem parte do suporte mais amplo do ADK para troca de dados estruturados, que inclui:

1. **input_schema**: Define formato de entrada esperado (não usado neste exemplo)
2. **output_schema**: Define formato de saída obrigatório (usado neste exemplo)
3. **output_key**: Armazena o resultado no estado da sessão para uso por outros agentes (usado neste exemplo)

Este padrão permite passagem confiável de dados entre agentes e integração com sistemas externos que esperam formatos de dados consistentes.

## Recursos Adicionais

- [Documentação de Dados Estruturados do ADK](https://google.github.io/adk-docs/agents/llm-agents/#structuring-data-input_schema-output_schema-output_key)
- [Documentação Pydantic](https://docs.pydantic.dev/latest/) 