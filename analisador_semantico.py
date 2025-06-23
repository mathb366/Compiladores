from analisador_sintatico import AnalisadorSintatico

class AnalisadorSemantico:
    def __init__(self):
        self.tabela_semantica = {}
        self.tem_erro_semantico = False
        self.arquivo_saida_path = "saida.txt"
        self.arquivo_saida = open(self.arquivo_saida_path, 'w')

    def carregar_tabelas(self, tabelas):
        self.tabela_semantica = tabelas
        self.registro_tab = tabelas.get("registro", {})
        self.constantes_tab = tabelas.get("constantes", {})
        self.variaveis_globais_tab = tabelas.get("variaveisGlobais", {})
        self.funcoes_tab = tabelas.get("funcoes", {})
        self.algoritmo_tab = tabelas.get("algoritmo", {})

    def analisa(self):
        # Regras simples
        self.verificar_duplicidade_globais()
        self.verificar_constantes_iniciais()
        self.verificar_registros()

        if self.tem_erro_semantico:
            self.arquivo_saida.write("Verifique os erros semânticos e tente compilar novamente.\n")
            print("Verifique os erros semânticos e tente compilar novamente.")
        else:
            self.arquivo_saida.write("Análise semântica realizada com sucesso.\n")
            print("Análise semântica realizada com sucesso.")

        self.arquivo_saida.write("\n=== TABELAS SEMÂNTICAS ===\n")
        for nome, tabela in self.tabela_semantica.items():
            self.arquivo_saida.write(f"\n>>> {nome.upper()} <<<\n")
            for chave, valor in tabela.items():
                self.arquivo_saida.write(f"{chave}: {valor}\n")

        self.arquivo_saida.close()

    def verificar_duplicidade_globais(self):
        nomes = set()
        for nome in self.variaveis_globais_tab:
            if nome in nomes:
                self.erro(f"Variável global '{nome}' declarada mais de uma vez.")
            nomes.add(nome)
        for nome in self.constantes_tab:
            if nome in nomes:
                self.erro(f"Constante '{nome}' duplicada com variável global '{nome}'.")
            nomes.add(nome)

    def verificar_constantes_iniciais(self):
        for nome, dados in self.constantes_tab.items():
            tipo, categoria, escopo = dados
            if tipo not in ["inteiro", "real", "char", "cadeia", "booleano"]:
                self.erro(f"Constante '{nome}' possui tipo inválido: '{tipo}'.")

    def verificar_registros(self):
        for nome_registro, campos in self.registro_tab.items():
            vistos = set()
            for campo, dados in campos.items():
                tipo, categoria = dados
                if campo in vistos:
                    self.erro(f"Campo '{campo}' duplicado no registro '{nome_registro}'.")
                vistos.add(campo)

    def erro(self, msg):
        print(f"Erro semântico: {msg}")
        self.arquivo_saida.write(f"Erro semântico: {msg}\n")
        self.tem_erro_semantico = True

# =================== EXECUÇÃO DIRETA ===================
if __name__ == "__main__":
    print("=== ANÁLISE SINTÁTICA ===")
    sintatico = AnalisadorSintatico()
    sintatico.start()
    tabelas = sintatico.get_tabelas()

    print("\n=== ANÁLISE SEMÂNTICA ===")
    semantico = AnalisadorSemantico()
    semantico.carregar_tabelas(tabelas)
    semantico.analisa()
