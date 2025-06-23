from analisador_lexico import AnalisadorLexicoRegex

class AnalisadorSintatico:
    def __init__(self):
        self.tokens = []
        self.index = 0
        self.erros = []

        self.executar_lexico()

    def executar_lexico(self):
        analisador = AnalisadorLexicoRegex()
        analisador.mudaEntrada("entrada.txt")
        analisador.analisa()

        with open(analisador.getSaida(), 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha == "$":
                    continue
                if "Erro Lexico" in linha:
                    continue
                if "->" in linha:
                    token, linha_info = linha.split("->")
                    self.tokens.append((token.strip(), int(linha_info)))

    def token_atual(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return ("EOF", -1)

    def consumir(self, esperado_prefixo):
        atual, linha = self.token_atual()
        if atual.startswith(esperado_prefixo):
            self.index += 1
            return True
        else:
            self.erros.append(f"Erro sintático na linha {linha}: encontrado {atual}")
            return False

    def start(self):
        print("Iniciando análise sintática...")
        self.algoritmo()
        if self.index < len(self.tokens):
            token_restante, linha = self.token_atual()
            self.erros.append(f"Erro: tokens restantes após o fim do programa (linha {linha}, token {token_restante})")
        self.reportar()

    def algoritmo(self):
        if not self.consumir("tok600_"): return  # algoritmo
        if not self.consumir("tok500_"): return  # identificador
        if not self.consumir("tok204_{"): return  # {
        self.comandos()
        if not self.consumir("tok205_"): return  # }

    def comandos(self):
        while self.index < len(self.tokens):
            token, _ = self.token_atual()
            if token.startswith("tok612_"):       # escreva
                self.cmd_escreva()
            elif token.startswith("tok611_"):     # leia
                self.cmd_leia()
            elif token.startswith("tok607_"):     # se
                self.cmd_se()
            elif token.startswith("tok610_"):     # para
                self.cmd_para()
            elif token.startswith("tok205_"):     # }
                break
            else:
                self.erros.append(f"Comando desconhecido ou fora de contexto: {token}")
                break

    def cmd_escreva(self):
        self.consumir("tok612_")
        self.consumir("tok202_")  # (
        self.consumir("tok700_")  # cadeia
        self.consumir("tok203_")  # )
        self.consumir("tok200_")  # ;

    def cmd_leia(self):
        self.consumir("tok611_")
        self.consumir("tok202_")  # (
        self.consumir("tok500_")  # identificador
        self.consumir("tok203_")  # )
        self.consumir("tok200_")  # ;

    def cmd_se(self):
        self.consumir("tok607_")  # se
        self.consumir("tok202_")  # (
        self.expressao()
        self.consumir("tok203_")  # )
        self.consumir("tok204_")  # {
        self.comandos()
        self.consumir("tok205_")  # }

    def cmd_para(self):
        self.consumir("tok610_")  # para
        self.consumir("tok202_")  # (
        self.consumir("tok500_")  # id
        self.consumir("tok115_")  # =
        self.expressao()
        self.consumir("tok200_")  # ;
        self.expressao()
        self.consumir("tok200_")  # ;
        self.expressao()
        self.consumir("tok203_")  # )
        self.consumir("tok204_")  # {
        self.comandos()
        self.consumir("tok205_")  # }

    def expressao(self):
        operadores = (
            "tok100_", "tok101_", "tok102_", "tok103_", "tok104_",  # . + - * /
            "tok105_", "tok106_", "tok107_", "tok108_", "tok109_",  # ++ -- == != >
            "tok110_", "tok111_", "tok112_", "tok113_", "tok114_",  # >= < <= && ||
            "tok115_"  # =
        )
        operandos = ("tok500_", "tok300_", "tok301_")  # id, int, real
        expr_ok = False

        while self.index < len(self.tokens):
            token, linha = self.token_atual()

            if token.startswith(operandos):
                expr_ok = True
                self.index += 1
            elif any(token.startswith(op) for op in operadores):
                self.index += 1
            elif token.startswith("tok203_") or token.startswith("tok200_") or token.startswith("tok204_"):
                # fim da expressão esperada
                break
            else:
                self.erros.append(f"Expressão mal formada na linha {linha}")
                break

        if not expr_ok:
            _, linha = self.token_atual()
            self.erros.append(f"Expressão mal formada na linha {linha}")


    def reportar(self):
        if not self.erros:
            print("Análise sintática concluída com sucesso.")
        else:
            print("Erros sintáticos encontrados:")
            for erro in self.erros:
                print(erro)


# Execução
if __name__ == "__main__":
    analisador = AnalisadorSintatico()
    analisador.start()

def get_tabelas(self):
        return {
            "registro": self.registro_tab if hasattr(self, 'registro_tab') else {},
            "constantes": self.constantes_tab if hasattr(self, 'constantes_tab') else {},
            "variaveisGlobais": self.variaveis_globais_tab if hasattr(self, 'variaveis_globais_tab') else {},
            "funcoes": self.funcoes_tab if hasattr(self, 'funcoes_tab') else {},
            "algoritmo": self.algoritmo_tab if hasattr(self, 'algoritmo_tab') else {}
        }