# sistema-loja-online

Uma aplicação de exemplo para gerenciar uma loja online (vendas, produtos, clientes e pedidos) escrita em Python. Este repositório contém a lógica de negócio organizada em models, controller e utilitários para conexão com o banco e validações.

## Visão geral

O projeto implementa um pequeno sistema de loja online para fins didáticos. Permite:

- Gerenciar clientes.
- Gerenciar produtos.
- Criar e listar pedidos e itens de pedido.
- Gerar relatórios simples.

O foco é demonstrar organização de código, acesso a banco de dados e separação entre camadas (controllers, models, utils).

## Requisitos

- Python 3.8 ou superior.
- Bibliotecas padrão do Python (o projeto usa sqlite3 pela conveniência; nenhuma dependência externa obrigatória está listada).

> Se você usar um ambiente virtual (recomendado), ative-o antes de executar a aplicação.

## Preparando o ambiente (Windows / PowerShell)

1. Criar e ativar um ambiente virtual:

powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1


2. (Opcional) Instalar dependências, se houver um requirements.txt no futuro:

powershell
pip install -r requirements.txt


## Banco de dados

O projeto inclui um script de criação das tabelas em scripts/create_tables.sql.

Para criar o esquema no SQLite você pode usar uma ferramenta gráfica (ex: DB Browser for SQLite) ou executar o SQL por um cliente compatível. Exemplo usando Python (exemplo genérico):

powershell
python -c "import sqlite3, pathlib; sql = pathlib.Path('scripts/create_tables.sql').read_text(); conn=sqlite3.connect('loja.db'); conn.executescript(sql); conn.commit(); conn.close()"


Após criar o banco, a aplicação espera encontrar/usar o arquivo de banco (por padrão loja.db se a conexão estiver configurada assim no projeto).

Consulte src/utils/conexao.py para detalhes de configuração de conexão com o banco.

## Estrutura do projeto

Principais diretórios e arquivos:

- src/ - código fonte da aplicação
	- main.py - ponto de entrada da aplicação
	- controller/ - controladores que orquestram operações e interagem com os models
		- controller_cliente.py
		- controller_produto.py
		- controller_pedido.py
		- controller_item_pedido.py
		- controller_relatorios.py
	- model/ - modelos de domínio
		- cliente.py, produto.py, pedido.py, item_pedido.py
	- utils/ - utilitários e helpers
		- conexao.py - gerenciamento de conexão com o banco
		- menu.py, splash_screen.py, validadores.py
	- reports/relatorios.py - gerador de relatórios simples

- scripts/create_tables.sql - script para criar as tabelas do banco de dados

## Como executar

Execute a partir da raiz do repositório. Exemplo (PowerShell):

powershell
python .\src\main.py


Ou execute como módulo (dependendo de como seu ambiente está configurado):

powershell
python -m src.main


Ao iniciar, o aplicativo exibe um menu (implementado em src/utils/menu.py) com opções para gerenciar clientes, produtos, pedidos e relatórios.

## Exemplos de uso rápido

- Criar clientes e produtos usando as opções do menu.
- Criar um pedido associando itens (produto + quantidade).
- Gerar relatórios simples através da opção de relatórios.

Os controllers expõem a lógica utilizada pelo menu. Para automatizar fluxos ou integrar com outras interfaces, importe e reutilize os controllers em src/controller/.

## Testes

Não há uma suíte de testes automatizada incluída por enquanto. Sugestões futuras:

- Adicionar testes unitários com pytest para models e controllers.
- Mockar conexões com banco para testes isolados.

## Como contribuir

- Abra uma issue para discutir mudanças ou registrar bugs.
- Envie pull requests pequenos e focados.
- Mantenha a consistência de estilo do código e adicione testes quando possível.

## Licença

Este repositório não contém uma licença explícita. Adicione um arquivo LICENSE se desejar torná-lo open-source sob uma licença específica.

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.
