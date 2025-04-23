# Compiladores

## Especificações do Código
**1. Leitura de Arquivo:**

Lê o conteúdo de um arquivo chamado programa.txt.
Os resultados da análise são gravados em resp-lex.txt.

**2. Definição de Tokens:**

Os tokens são definidos com base em expressões regulares, categorizados como:
- Comentários (//, /* */)

- Operadores compostos (como ++, ==, &&)

- Operadores simples (+, -, *, /, >, <, =, etc.)

- Delimitadores (;, ,, (, ), {, }, [, ])

- Números inteiros e reais

- Constantes de caractere e cadeia

- Palavras reservadas (como algoritmo, se, para, inteiro, etc.)

- Identificadores (nomes de variáveis, funções, etc.)

- Espaços em branco e quebras de linha

- Caracteres inválidos

**3. Tratamento de Erros:**

Detecta e reporta:

- Caracteres inválidos

- Comentários de bloco não fechados

- Constantes de caractere vazias ('')

## Limitações do Código

- Embora o padrão de regex para comentário de bloco use [\s\S]*? (que inclui novas linhas), a implementação trata linha por linha, então não consegue validar corretamente comentários de bloco que se estendem por várias linhas.

- As palavras reservadas são fixadas no código. Não há suporte para extensão dinâmica do vocabulário da linguagem analisada.

- O programa apenas grava a saída em arquivo, sem feedback imediato ao usuário.

## Licença

Este projeto está licenciado sob os termos de Licença MIT. Veja o arquivo [LICENSE](./MIT%20License.txt) para mais detalhes.