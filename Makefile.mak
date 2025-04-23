# Variáveis
PYTHON = python3
PIP = pip
VENV = venv
VENV_DIR = .venv

# Objetivo principal
all: build

# Criar ambiente virtual
$(VENV_DIR)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/$(PIP) install -r requirements.txt

# Instalar dependências
install: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/$(PIP) install -r requirements.txt

# Executar o código principal
run:
	$(VENV_DIR)/bin/$(PYTHON) analisador_lexico.py

# Rodar os testes (supondo que você use pytest)
test:
	$(VENV_DIR)/bin/pytest tests

# Limpar arquivos de compilação e ambiente virtual
clean:
	rm -rf $(VENV_DIR)

# Build do projeto (instala dependências e prepara o ambiente)
build: install

# Exemplo de alvo "help" para mostrar o que pode ser feito
help:
	@echo "Makefile para um projeto Python"
	@echo ""
	@echo "Objetivos disponíveis:"
	@echo "  make build   - Instala dependências e configura o ambiente virtual"
	@echo "  make run     - Executa o código Python principal"
	@echo "  make test    - Executa os testes automatizados"
	@echo "  make clean   - Limpa o ambiente virtual"
	@echo "  make install - Instala dependências"