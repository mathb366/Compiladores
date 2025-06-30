from analisador_lexico import AnalisadorLexicoRegex

class AnalisadorSintatico:
    def __init__(self):
        self.tokens = []
        self.index = 0
        self.erros = []
        self.variaveis_globais_tab = {}
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

        self.bloco_declaracoes()
        self.comandos()

        if not self.consumir("tok205_"): return  # }

    def bloco_declaracoes(self):
        while True:
            token, _ = self.token_atual()
            if token.startswith("tok601_"):  # variaveis
                self.index += 1
                self.parse_declaracoes_variaveis()
            elif token.startswith("tok602_"):  # constantes
                self.index += 1
                self.parse_declaracoes_constantes()
            elif token.startswith("tok603_") or token.startswith("tok604_"):  # registros ou registro
                self.index += 1
                self.parse_declaracoes_registros()
            else:
                break

    def parse_declaracoes_variaveis(self):
        while True:
            token, _ = self.token_atual()
            if token.startswith("tok613_") or token.startswith("tok614_") or token.startswith("tok615_") or token.startswith("tok616_") or token.startswith("tok617_"):
                tipo = token.split("_")[1]  # Ex: inteiro
                self.index += 1
                if self.token_atual()[0].startswith("tok500_"):
                    token_nome = self.token_atual()[0]
                    if '_' in token_nome:
                        nome = token_nome.split("_", 1)[1]
                    else:
                        nome = token_nome
                    if nome not in self.variaveis_globais_tab:
                        self.variaveis_globais_tab[nome] = []
                    self.variaveis_globais_tab[nome].append((tipo, "variavel", "global"))
                    self.index += 1
                    self.consumir("tok200_")
                else:
                    break
            else:
                break

    def parse_declaracoes_constantes(self):
        while True:
            token, _ = self.token_atual()
            if token.startswith("tok613_") or token.startswith("tok614_") or token.startswith("tok615_") or token.startswith("tok616_") or token.startswith("tok617_"):
                self.index += 1
                if self.token_atual()[0].startswith("tok500_"):
                    self.index += 1
                    self.consumir("tok115_")
                    self.index += 1  # valor
                    self.consumir("tok200_")
                else:
                    break
            else:
                break

    def parse_declaracoes_registros(self):
        if self.token_atual()[0].startswith("tok604_"):  # registro
            self.index += 1
        if self.token_atual()[0].startswith("tok500_"):
            self.index += 1
            self.consumir("tok204_")
            while True:
                token, _ = self.token_atual()
                if token.startswith("tok613_") or token.startswith("tok614_") or token.startswith("tok615_") or token.startswith("tok616_") or token.startswith("tok617_"):
                    self.index += 1
                    if self.token_atual()[0].startswith("tok500_"):
                        self.index += 1
                        self.consumir("tok200_")
                    else:
                        break
                else:
                    break
            self.consumir("tok205_")

    def comandos(self):
        while self.index < len(self.tokens):
            token, _ = self.token_atual()
            if token.startswith("tok612_"):
                self.cmd_escreva()
            elif token.startswith("tok611_"):
                self.cmd_leia()
            elif token.startswith("tok607_"):
                self.cmd_se()
            elif token.startswith("tok610_"):
                self.cmd_para()
            elif token.startswith("tok205_"):
                break
            else:
                self.erros.append(f"Comando desconhecido ou fora de contexto: {token}")
                break

    def cmd_escreva(self):
        self.consumir("tok612_")
        self.consumir("tok202_")
        self.consumir("tok700_")
        self.consumir("tok203_")
        self.consumir("tok200_")

    def cmd_leia(self):
        self.consumir("tok611_")
        self.consumir("tok202_")
        self.consumir("tok500_")
        self.consumir("tok203_")
        self.consumir("tok200_")

    def cmd_se(self):
        self.consumir("tok607_")
        self.consumir("tok202_")
        self.expressao()
        self.consumir("tok203_")
        self.consumir("tok204_")
        self.comandos()
        self.consumir("tok205_")

    def cmd_para(self):
        self.consumir("tok610_")
        self.consumir("tok202_")
        self.consumir("tok500_")
        self.consumir("tok115_")
        self.expressao()
        self.consumir("tok200_")
        self.expressao()
        self.consumir("tok200_")
        self.expressao()
        self.consumir("tok203_")
        self.consumir("tok204_")
        self.comandos()
        self.consumir("tok205_")

    def expressao(self):
        operadores = (
            "tok100_", "tok101_", "tok102_", "tok103_", "tok104_",
            "tok105_", "tok106_", "tok107_", "tok108_", "tok109_",
            "tok110_", "tok111_", "tok112_", "tok113_", "tok114_",
            "tok115_"
        )
        operandos = ("tok500_", "tok300_", "tok301_")
        expr_ok = False

        while self.index < len(self.tokens):
            token, linha = self.token_atual()
            if token.startswith(operandos):
                expr_ok = True
                self.index += 1
            elif any(token.startswith(op) for op in operadores):
                self.index += 1
            elif token.startswith("tok203_") or token.startswith("tok200_") or token.startswith("tok204_"):
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

    def get_tabelas(self):
        return {
            "registro": getattr(self, "registro_tab", {}),
            "constantes": getattr(self, "constantes_tab", {}),
            "variaveisGlobais": self.variaveis_globais_tab,
            "funcoes": getattr(self, "funcoes_tab", {}),
            "algoritmo": getattr(self, "algoritmo_tab", {})
        }

if __name__ == "__main__":
    analisador = AnalisadorSintatico()
    analisador.start()
