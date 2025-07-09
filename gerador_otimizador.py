import re

class GeradorCodigo:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.codigo = []
        self.temp_count = 0
        self.label_count = 0

    def novo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def novo_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def token_atual(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        return ("EOF", -1)

    def consumir(self, prefixo):
        tok, _ = self.token_atual()
        if tok.startswith(prefixo):
            self.index += 1
            return True
        return False

    def gerar(self):
        while self.index < len(self.tokens):
            token, _ = self.token_atual()
            if token.startswith("tok611_"):
                self.cmd_leia()
            elif token.startswith("tok612_"):
                self.cmd_escreva()
            elif token.startswith("tok607_"):
                self.cmd_se()
            elif token.startswith("tok610_"):
                self.cmd_para()
            else:
                self.index += 1
        return self.codigo

    def cmd_leia(self):
        self.consumir("tok611_")
        self.consumir("tok202_")
        var = self.tokens[self.index][0].split("_")[1]
        self.index += 1
        self.consumir("tok203_")
        self.consumir("tok200_")
        self.codigo.append(f"LEIA {var}")

    def cmd_escreva(self):
        self.consumir("tok612_")
        self.consumir("tok202_")
        val = self.tokens[self.index][0].split("_", 1)[1]
        self.index += 1
        self.consumir("tok203_")
        self.consumir("tok200_")
        self.codigo.append(f"ESCREVA {val}")

    def cmd_se(self):
        self.consumir("tok607_")
        self.consumir("tok202_")
        cond = self.expressao()
        self.consumir("tok203_")
        self.consumir("tok204_")
        label_fim = self.novo_label()
        self.codigo.append(f"IF_FALSE {cond} GOTO {label_fim}")
        self.gerar()
        self.consumir("tok205_")
        self.codigo.append(f"{label_fim}:")

    def cmd_para(self):
        self.consumir("tok610_")
        self.consumir("tok202_")
        var = self.tokens[self.index][0].split("_")[1]
        self.index += 1
        self.consumir("tok115_")
        inicio = self.expressao()
        self.consumir("tok200_")
        cond = self.expressao()
        self.consumir("tok200_")
        passo = self.expressao()
        self.consumir("tok203_")
        self.consumir("tok204_")

        label_inicio = self.novo_label()
        label_fim = self.novo_label()

        self.codigo.append(f"{var} = {inicio}")
        self.codigo.append(f"{label_inicio}:")
        self.codigo.append(f"IF_FALSE {cond} GOTO {label_fim}")
        self.gerar()
        self.codigo.append(f"{var} = {passo}")
        self.codigo.append(f"GOTO {label_inicio}")
        self.consumir("tok205_")
        self.codigo.append(f"{label_fim}:")

    def expressao(self):
        token, _ = self.token_atual()
        if token.startswith("tok500_") or token.startswith("tok300_"):
            valor = token.split("_")[1]
            self.index += 1
            return valor
        return "?"


class OtimizadorCodigo:
    def __init__(self, codigo_intermediario):
        self.codigo = codigo_intermediario

    def otimizar(self):
        otimizados = []
        vistos = set()
        for linha in self.codigo:
            if " = " in linha:
                var, expr = linha.split(" = ")
                if expr.isdigit() and var in vistos:
                    continue  # código morto
                vistos.add(var)
            otimizados.append(linha)
        return otimizados


class GeradorMIPS:
    def __init__(self, codigo_intermediario):
        self.codigo = codigo_intermediario
        self.saida = []

    def traduzir(self):
        for linha in self.codigo:
            if linha.startswith("LEIA"):
                var = linha.split()[1]
                self.saida.append(f"# LEIA {var}")
                self.saida.append("li $v0, 5")
                self.saida.append("syscall")
                self.saida.append(f"move ${var}, $v0")

            elif linha.startswith("ESCREVA"):
                val = linha.split()[1]
                self.saida.append(f"# ESCREVA {val}")
                self.saida.append(f"li $a0, {val}")
                self.saida.append("li $v0, 1")
                self.saida.append("syscall")

            elif " = " in linha:
                var, expr = linha.split(" = ")
                if expr.isdigit():
                    self.saida.append(f"li ${var}, {expr}")
                else:
                    self.saida.append(f"move ${var}, ${expr}")

            elif "IF_FALSE" in linha:
                partes = linha.split()
                cond, label = partes[1], partes[3]
                self.saida.append(f"# IF_FALSE {cond} GOTO {label}")
                self.saida.append(f"beq ${cond}, $zero, {label}")

            elif linha.endswith(":"):
                self.saida.append(f"{linha}")

            elif linha.startswith("GOTO"):
                _, label = linha.split()
                self.saida.append(f"j {label}")

        return self.saida


# Execução principal
if __name__ == "__main__":
    from analisador_lexico import AnalisadorLexicoRegex

    # Análise léxica
    analisador = AnalisadorLexicoRegex()
    analisador.analisa()

    tokens = []
    with open("saida.txt", "r", encoding="utf-8") as f:
        for linha in f:
            if "->" in linha:
                tok, linha_n = linha.strip().split("->")
                tokens.append((tok, int(linha_n)))

    # Geração de código intermediário
    gerador = GeradorCodigo(tokens)
    codigo = gerador.gerar()
    with open("codigo_intermediario.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(codigo))

    # Otimização
    otimizador = OtimizadorCodigo(codigo)
    otimizados = otimizador.otimizar()
    with open("codigo_otimizado.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(otimizados))

    # Geração de código MIPS
    gerador_mips = GeradorMIPS(otimizados)
    mips = gerador_mips.traduzir()
    with open("codigo_mips.asm", "w", encoding="utf-8") as f:
        f.write("\n".join(mips))
