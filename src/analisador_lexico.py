import re
import os

class AnalisadorLexicoRegex:
    def __init__(self):
        self.arquivo_e = "entrada.txt"
        self.arquivo_s = "saida.txt"
        self.tokens = [
            # Comentários
            ('COMENTARIO_LINHA', r'//.*'),
            ('COMENTARIO_BLOCO', r'/\*[\s\S]*?\*/'),
            
            # Operadores compostos
            ('tok105', r'\+\+'), ('tok106', r'--'), ('tok107', r'=='), ('tok108', r'!='), 
            ('tok110', r'>='), ('tok112', r'<='), ('tok113', r'&&'), ('tok114', r'\|\|'),
            
            # Operadores simples
            ('tok100', r'\.'), ('tok101', r'\+'), ('tok102', r'-'), ('tok103', r'\*'), 
            ('tok104', r'/'), ('tok109', r'>'), ('tok111', r'<'), ('tok115', r'='),
            
            # Delimitadores
            ('tok200', r';'), ('tok201', r','), ('tok202', r'\('), ('tok203', r'\)'),
            ('tok204', r'\{'), ('tok205', r'\}'), ('tok206', r'\['), ('tok207', r'\]'),

            # Números
            ('tok301', r'\b\d+\.\d+\b'),
            ('tok300', r'\b\d+\b'),

            # Caracter constante
            ('tok400', r"'[^']'"),

            # Cadeia constante
            ('tok700', r'"[^"\n]*"'),

            # Palavras reservadas
            *[(f'tok60{i}', r'\b' + palavra + r'\b') for i, palavra in enumerate([
                'algoritmo', 'variaveis', 'constantes', 'registro', 'funcao',
                'retorno', 'vazio', 'se', 'senao', 'enquanto', 'para', 'leia',
                'escreva', 'inteiro', 'real', 'booleano', 'char', 'cadeia', 
                'verdadeiro', 'falso'
            ])],

            # Identificadores
            ('tok500', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),

            # Espaços e quebras de linha
            ('WHITESPACE', r'[ \t\r\f\v]+'),
            ('NEWLINE', r'\n'),

            # Caracter inválido
            ('INVALIDO', r'.'),
        ]

        # Compila todos os padrões numa única expressão
        self.regex = re.compile('|'.join(f'(?P<{nome}>{padrao})' for nome, padrao in self.tokens))

    def mudaEntrada(self, arquivo):
        self.arquivo_e = arquivo

    def getEntrada(self):
        return self.arquivo_e

    def getSaida(self):
        return self.arquivo_s

    def analisa(self):
        if not os.path.exists(self.arquivo_e):
            with open(self.arquivo_s, 'w') as out:
                out.write("Arquivo de entrada inexistente")
            return

        with open(self.arquivo_e, 'r', encoding='utf-8') as entrada, \
             open(self.arquivo_s, 'w', encoding='utf-8') as saida:

            numero_linha = 1
            bloco_aberto = False

            for linha in entrada:
                pos = 0
                while pos < len(linha):
                    match = self.regex.match(linha, pos)
                    if not match:
                        break

                    tipo = match.lastgroup
                    lexema = match.group(tipo)

                    # Ignora espaços e novas linhas
                    if tipo == 'WHITESPACE' or tipo == 'NEWLINE':
                        pass
                    elif tipo == 'COMENTARIO_LINHA':
                        break
                    elif tipo == 'COMENTARIO_BLOCO':
                        if '*/' not in lexema:
                            saida.write(f"Erro Lexico - Comentario de bloco nao fechado - linha: {numero_linha}\n")
                            bloco_aberto = True
                            break
                    elif tipo == 'INVALIDO':
                        saida.write(f"Erro Lexico - Caracter Invalido: {lexema} - linha: {numero_linha}\n")
                    elif tipo == 'tok400' and lexema == "''":
                        saida.write(f"Erro Lexico - Caractere nao pode ser vazio - Linha: {numero_linha}\n")
                    else:
                        saida.write(f"{tipo}_{lexema}->"+str(numero_linha)+'\n')

                    pos = match.end()

                if bloco_aberto:
                    break
                numero_linha += 1

            saida.write('$')

analisador = AnalisadorLexicoRegex()
analisador.analisa()