from analisador_sintatico import AnalisadorSintatico

class AnalisadorSemantico:
    def __init__(self):
        self.tabela_semantica = {}
        self.tem_erro_semantico = False
        self.arquivo_saida_path = "saida.txt"
        self.arquivo_saida = open(self.arquivo_saida_path, 'a', encoding='utf-8')  # Modo append

    def carregar_tabelas(self, tabelas):
        self.tabela_semantica = tabelas
        self.registro_tab = tabelas.get("registro", {})
        self.constantes_tab = tabelas.get("constantes", {})
        self.variaveis_globais_tab = tabelas.get("variaveisGlobais", {})
        self.funcoes_tab = tabelas.get("funcoes", {})
        self.algoritmo_tab = tabelas.get("algoritmo", {})

    def analisa(self):
        self.arquivo_saida.write("\nExecutando analisador semântico com as tabelas...\n")
        self.verificar_duplicidade_globais()
        self.verificar_constantes_iniciais()
        self.verificar_registros()
        self.verificar_conflito_tipos()

        self.arquivo_saida.write("\n=== RESULTADO DA ANÁLISE SEMÂNTICA ===\n")
        if self.tem_erro_semantico:
            msg = "Verifique os erros semânticos e tente compilar novamente."
            self.arquivo_saida.write(msg + "\n")
            print(msg)
        else:
            msg = "Análise semântica realizada com sucesso."
            self.arquivo_saida.write(msg + "\n")
            print(msg)

        self.arquivo_saida.write("\n=== TABELAS SEMÂNTICAS ===\n")
        for nome, tabela in self.tabela_semantica.items():
            self.arquivo_saida.write(f"\n>>> {nome.upper()} <<<\n")
            for chave, valor in tabela.items():
                self.arquivo_saida.write(f"{chave}: {valor}\n")

        self.arquivo_saida.close()

    def verificar_duplicidade_globais(self):
        nomes = {}
        for nome, entradas in self.variaveis_globais_tab.items():
            if len(entradas) > 1:
                self.erro(f"Variável global '{nome}' declarada mais de uma vez.")
            nomes[nome] = 'variavel'

        for nome in self.constantes_tab:
            if nome in nomes:
                self.erro(f"Constante '{nome}' duplicada com variável global '{nome}'.")
            nomes[nome] = 'constante'

        for func_nome, dados in self.funcoes_tab.items():
            if "variaveis" in dados:
                vistos = set()
                for var_nome in dados["variaveis"]:
                    if var_nome in vistos:
                        self.erro(f"Variável local '{var_nome}' duplicada na função '{func_nome}'.")
                    vistos.add(var_nome)

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

    def verificar_conflito_tipos(self):
        for func_nome, dados in self.funcoes_tab.items():
            parametros = dados.get("parametros", {})
            variaveis = dados.get("variaveis", {})
            for nome_var, tipo_info in variaveis.items():
                tipo_var, _, _ = tipo_info
                if nome_var in parametros:
                    tipo_param = parametros[nome_var][0]
                    if tipo_param != tipo_var:
                        self.erro(
                            f"Conflito de tipos na função '{func_nome}': parâmetro '{nome_var}' é '{tipo_param}', "
                            f"mas variável com mesmo nome é '{tipo_var}'."
                        )

    def erro(self, msg):
        print(f"Erro semântico: {msg}")
        self.arquivo_saida.write(f"Erro semântico: {msg}\n")
        self.tem_erro_semantico = True


# Execução
if __name__ == "__main__":
    with open("saida.txt", "w", encoding="utf-8") as f:
        f.write("Executando analisador sintático para obter tabelas...\n")
    sintatico = AnalisadorSintatico()
    sintatico.start()

    tabelas = sintatico.get_tabelas()

    semantico = AnalisadorSemantico()
    semantico.carregar_tabelas(tabelas)
    semantico.analisa()
