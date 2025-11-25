# sistema-loja-online

Uma aplicação de exemplo para gerenciar uma loja online (vendas, produtos, clientes e pedidos) escrita em Python. Este repositório contém a lógica de negócio organizada em models, controller e utilitários para conexão com o banco e validações.

## Visão geral

O projeto implementa um pequeno sistema de loja online para fins didáticos. Permite:

- Gerenciar clientes.
- Gerenciar produtos.
- Criar e listar pedidos e itens de pedido.
- Gerar relatórios simples.

## Integrantes

Desenvolvido por:

- Kaynan de Oliveira Barbosa
- Rafael Covre Vilque
- Ricardo Cardeais
- Renato Oliveira de Jesus
- Yuri Gabriel Amorim dos Santos

<!-- Os nomes acima foram extraídos de `src/main.py` -->

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

Para dúvidas ou sugestões, abra uma issue no repositório..

# Novo modelo C3

# 🛒 Sistema de Loja Online — MongoDB (C3)

Projeto desenvolvido para a disciplina de Banco de Dados (2025/2), sob orientação do Prof. Howard Roatti. Implementa um sistema de loja online com CRUD + relatórios, utilizando MongoDB como banco de dados não relacional.

> ✅ Projeto adaptado da C2 (SQLite) conforme orientação do edital (item 1).

## 🧑‍💻 Integrantes
- Kaynan de Oliveira Barbosa
- Rafael Covre Vilque
- Ricardo Cardeais
- Renato Oliveira de Jesus
- Yuri Gabriel Amorim dos Santos

## 📦 Requisitos
- Python 3.8+
- MongoDB (local ou Atlas)
- Biblioteca pymongo

## ⚙️ Configuração (Linux)

1. Clone o repositório
git clone https://github.com/RenatoOJ-Dev/sistema-loja-online.git
cd sistema-loja-online

2. Crie e ative ambiente virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

3. Instale as dependências
pip install pymongo

4. Configure o MongoDB
Opção A (MongoDB local):
Instale o MongoDB Community e inicie o serviço:
sudo systemctl start mongod

Opção B (MongoDB Atlas):
Edite src/utils/conexao.py e atualize a URI com sua string de conexão:
URI = "mongodb+srv://<usuario>:<senha>@cluster0.xxxxx.mongodb.net/loja"

5. Migre os dados (opcional, mas recomendado)
Execute o script de migração para pré-cadastrar documentos:
python3 src/scripts/sqlite_to_mongo.py
Este script lê loja.db (SQLite) e insere os documentos nas coleções clientes, produtos, pedidos e itens_pedido.

6. Execute a aplicação
python3 -m src.main
O sistema roda 100% no console, com interface amigável e menus intuitivos — atendendo ao edital.

## 📁 Estrutura do Projeto
src/
├── controller/      # Controladores (Cliente, Produto, Pedido, Relatórios)
├── model/           # Modelos de domínio (Cliente, Produto, Pedido, ItemPedido)
├── utils/           # Conexão (MongoDB), validadores, splash screen
├── scripts/         # Script de migração SQLite → MongoDB
└── main.py          # Ponto de entrada

## ✅ Funcionalidades Implementadas (conforme edital)

Item do Edital | Implementação
---------------|---------------
6.b — Splash Screen com contagem de documentos | splash_screen_mongodb() mostra qtd. em clientes, produtos, pedidos, itens_pedido
6.a.1.i — Relatório com agrupamento ($group) | relatorio_pedidos_por_cliente() → total de pedidos/valor por cliente (1,0 pt)
6.a.1.ii — Relatório com junção ($lookup) | relatorio_vendas_por_categoria() → vendas por categoria (0,5 pt)
6.c.5.i — Integridade referencial na exclusão | Ao excluir cliente/produto/pedido: verifica e remove documentos filhos (+0,5 pt)
6.d.vii–viii — Atualização + exibição + repetição | atualizar() exibe registro atualizado e permite repetição (+0,5 pt)
8.a.v — Documentação para Linux | Este README.md (+0,5 pt)


📌 Observação: Este projeto é uma migração da C2 (SQLite) para MongoDB, conforme orientado no edital (item 1).
