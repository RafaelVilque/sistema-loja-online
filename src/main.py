<<<<<<< HEAD
# ==========================
# SISTEMA DE LOJA ONLINE — MongoDB
# ==========================

from src.controller import *
from src.model import *
from src.utils import *
from src.utils.conexao import Conexao


# ==========================
# MENU PRINCIPAL
# ==========================
def menu_principal():
    controller_cliente = ControllerCliente()
    controller_produto = ControllerProduto()
    controller_pedido = ControllerPedido()
    controller_relatorios = ControllerRelatorios()

    while True:
        print("\n===== SISTEMA DE LOJA ONLINE =====")
        print("1 - Menu de Clientes")
        print("2 - Menu de Produtos")
        print("3 - Menu de Pedidos")
        print("4 - Relatórios")
        print("5 - Sair")

        print("\nDesenvolvido por:")
        print("👤 Kaynan de Oliveira Barbosa")
        print("👤 Rafael Covre Vilque")
        print("👤 Ricardo Cardeais")
        print("👤 Renato Oliveira de Jesus")
        print("👤 Yuri Gabriel Amorim dos Santos\n")

        print("Disciplina: Banco de Dados 2025/2")
        print("Professor: Howard Roatti\n")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_clientes(controller_cliente)
        elif opcao == "2":
            menu_produtos(controller_produto)
        elif opcao == "3":
            menu_pedidos(controller_pedido, controller_cliente, controller_produto)
        elif opcao == "4":
            menu_relatorios(controller_relatorios)
        elif opcao == "5":
            print("Saindo... 👋")
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# MENU CLIENTES
# ==========================
def menu_clientes(controller):
    while True:
        print("\n--- MENU CLIENTES ---")
        print("1 - Inserir cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Remover cliente")
        print("5 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = ler_telefone("Telefone (somente números, com DDD): ")
            telefone = formatar_telefone(telefone)
            endereco = input("Endereço: ")

            cliente = Cliente(None, nome, email, telefone, endereco)
            cliente_inserido = controller.inserir(cliente)

            print("\n✅ Cliente cadastrado com sucesso! Comprovante:")
            print("---------------------------------------------")
            print(cliente_inserido)
            print("---------------------------------------------")

        elif opcao == "2":
            controller.listar()

        elif opcao == "3":
            id_cliente = int(input("ID do cliente a atualizar: "))
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            telefone = ler_telefone("Novo telefone (somente números, com DDD): ")
            telefone = formatar_telefone(telefone)
            endereco = input("Novo endereço: ")

            cliente_obj = Cliente(id_cliente, nome, email, telefone, endereco)
            controller.atualizar(cliente_obj)

        elif opcao == "4":
            id_cliente = int(input("ID do cliente a remover: "))
            confirmar = input("Tem certeza que deseja remover este cliente? (S/N): ").strip().upper()
            if confirmar == "S":
                controller.remover(id_cliente)
            else:
                print("❌ Remoção cancelada.")

        elif opcao == "5":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# MENU PRODUTOS
# ==========================
def menu_produtos(controller):
    while True:
        print("\n--- MENU PRODUTOS ---")
        print("1 - Inserir produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Remover produto")
        print("5 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            categoria = input("Categoria: ")
            preco = ler_numero_decimal("Preço: ")
            estoque = ler_numero_inteiro("Quantidade em estoque: ")

            controller.inserir(Produto(None, nome, descricao, preco, estoque, categoria))

        elif opcao == "2":
            controller.listar()

        elif opcao == "3":
            id_produto = int(input("ID do produto a atualizar: "))
            nome = input("Novo nome: ")
            descricao = input("Nova descrição: ")
            categoria = input("Nova categoria: ")
            preco = ler_numero_decimal("Novo preço: ")
            estoque = ler_numero_inteiro("Nova quantidade em estoque: ")

            produto = Produto(id_produto, nome, descricao, preco, estoque, categoria)
            controller.atualizar(produto)

        elif opcao == "4":
            id_produto = int(input("ID do produto a remover: "))
            confirmar = input("Tem certeza que deseja remover este produto? (S/N): ").strip().upper()
            if confirmar == "S":
                controller.remover(id_produto)
            else:
                print("❌ Remoção cancelada.")

        elif opcao == "5":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# MENU PEDIDOS
# ==========================
def menu_pedidos(controller_pedido, controller_cliente, controller_produto):
    while True:
        print("\n--- MENU PEDIDOS ---")
        print("1 - Criar novo pedido")
        print("2 - Listar pedidos")
        print("3 - Ver itens de um pedido")
        print("4 - Remover pedido")
        print("5 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            criar_pedido(controller_pedido, controller_cliente, controller_produto)
        elif opcao == "2":
            controller_pedido.listar_pedidos()
        elif opcao == "3":
            id_pedido = int(input("ID do pedido: "))
            controller_pedido.listar_itens_pedido(id_pedido)
        elif opcao == "4":
            id_pedido = int(input("ID do pedido a remover: "))
            controller_pedido.remover_pedido(id_pedido)
        elif opcao == "5":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# CRIAR PEDIDO
# ==========================
def criar_pedido(controller_pedido, controller_cliente, controller_produto):
    print("\n📦 Criando novo pedido...")
    controller_cliente.listar()
    id_cliente = int(input("\nDigite o ID do cliente: "))
    
    print("\n💳 Formas de pagamento disponíveis:")
    formas_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix"]
    for i, forma in enumerate(formas_pagamento, start=1):
        print(f"{i} - {forma}")

    opcao_pagamento = int(input("Escolha a forma de pagamento: "))
    if opcao_pagamento not in range(1, len(formas_pagamento) + 1):
        print("❌ Opção inválida! Usando padrão: Dinheiro.")
        forma_pagamento = "Dinheiro"
    else:
        forma_pagamento = formas_pagamento[opcao_pagamento - 1]

    # Buscar endereço do cliente automaticamente
    cliente = controller_cliente.buscar_por_id(id_cliente)
    if cliente and cliente.endereco:
        endereco = cliente.endereco
        print(f"📍 Endereço de entrega: {endereco}")
    else:
        print("⚠️ Endereço não encontrado no cadastro do cliente.")
        endereco = input("Informe manualmente o endereço de entrega: ")

    pedido = Pedido(None, id_cliente, None, "Em aberto", 0.0, forma_pagamento, endereco)
    controller_pedido.inserir_pedido(pedido)

    # Recupera o ID gerado
    ultimo_pedido = controller_pedido.buscar_ultimo()
    if not ultimo_pedido:
        print("❌ Falha ao recuperar ID do pedido.")
        return
    ultimo_id = ultimo_pedido.id_pedido
    total = 0.0

    while True:
        controller_produto.listar()
        id_produto = int(input("\nDigite o ID do produto (ou 0 para finalizar): "))
        if id_produto == 0:
            break

        quantidade = int(input("Quantidade: "))
        produto = controller_produto.buscar_por_id(id_produto)
        if not produto:
            print("❌ Produto não encontrado.")
            continue

        preco_unitario = produto.preco
        subtotal = preco_unitario * quantidade
        total += subtotal

        item = ItemPedido(None, ultimo_id, id_produto, quantidade, preco_unitario, subtotal)
        controller_pedido.inserir_item(item)

    # Atualiza valor total do pedido
    controller_pedido.atualizar_valor_total(ultimo_id, total)

    print(f"\n✅ Pedido criado com sucesso! Valor total: R${total:.2f}")


# ==========================
# MENU RELATÓRIOS
# ==========================
def menu_relatorios(controller_relatorios):
    while True:
        print("\n--- MENU RELATÓRIOS ---")
        print("1 - Total de pedidos por cliente")
        print("2 - Total de vendas por categoria")
        print("3 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            controller_relatorios.relatorio_pedidos_por_cliente()
        elif opcao == "2":
            controller_relatorios.relatorio_vendas_por_categoria()
        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# SPLASH SCREEN ATUALIZADA (MongoDB)
# ==========================
def splash_screen_mongodb():
    db = Conexao()

    qtd_clientes = db.count_documents("clientes")
    qtd_produtos = db.count_documents("produtos")
    qtd_pedidos = db.count_documents("pedidos")
    qtd_itens = db.count_documents("itens_pedido")

    print("\n" + "="*60)
    print("        🎉 SISTEMA DE LOJA ONLINE — MongoDB 🎉")
    print("="*60)
    print(f"📌 Coleções e documentos:")
    print(f"   • Clientes: {qtd_clientes} documento(s)")
    print(f"   • Produtos: {qtd_produtos} documento(s)")
    print(f"   • Pedidos:  {qtd_pedidos} documento(s)")
    print(f"   • Itens:    {qtd_itens} documento(s)")
    print()
    print("👤 Desenvolvido por:")
    print("   • Kaynan de Oliveira Barbosa")
    print("   • Rafael Covre Vilque")
    print("   • Ricardo Cardeais")
    print("   • Renato Oliveira de Jesus")
    print("   • Yuri Gabriel Amorim dos Santos")
    print()
    print("📚 Disciplina: Banco de Dados 2025/2")
    print("👨‍🏫 Professor: Howard Roatti")
    print("="*60 + "\n")


# ==========================
# EXECUÇÃO PRINCIPAL
# ==========================
if __name__ == "__main__":
    # criar_tabelas()  # ❌ REMOVIDO — não se aplica ao MongoDB
    splash_screen_mongodb()  # ✅ Nova splash com contagem — item 6.c do edital
    menu_principal()
=======
# ==========================
# SISTEMA DE LOJA ONLINE
# ==========================

from src.controller import *
from src.model import *
from src.utils import *


# ==========================
# MENU PRINCIPAL
# ==========================
def menu_principal():
    controller_cliente = ControllerCliente()
    controller_produto = ControllerProduto()
    controller_pedido = ControllerPedido()
    controller_relatorios = ControllerRelatorios()

    while True:
        print("\n===== SISTEMA DE LOJA ONLINE =====")
        print("1 - Menu de Clientes")
        print("2 - Menu de Produtos")
        print("3 - Menu de Pedidos")
        print("4 - Relatórios")
        print("5 - Sair")

        print("\nDesenvolvido por:")
        print("👤 Kaynan de Oliveira Barbosa")
        print("👤 Rafael Covre Vilque")
        print("👤 Ricardo Cardeais")
        print("👤 Renato Oliveira de Jesus")
        print("👤 Yuri Gabriel Amorim dos Santos\n")

        print("Disciplina: Banco de Dados 2025/2")
        print("Professor: Howard Roatti\n")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_clientes(controller_cliente)
        elif opcao == "2":
            menu_produtos(controller_produto)
        elif opcao == "3":
            menu_pedidos(controller_pedido, controller_cliente, controller_produto)
        elif opcao == "4":
            menu_relatorios(controller_relatorios)
        elif opcao == "5":
            print("Saindo... 👋")
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# MENU CLIENTES
# ==========================
def menu_clientes(controller):
    while True:
        print("\n--- MENU CLIENTES ---")
        print("1 - Inserir cliente")
        print("2 - Listar clientes")
        print("3 - Atualizar cliente")
        print("4 - Remover cliente")
        print("5 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            telefone = ler_telefone("Telefone (somente números, com DDD): ")
            telefone = formatar_telefone(telefone)
            endereco = input("Endereço: ")

            cliente = Cliente(None, nome, email, telefone, endereco)
            cliente_inserido = controller.inserir(cliente)

            print("\n✅ Cliente cadastrado com sucesso! Comprovante:")
            print("---------------------------------------------")
            print(cliente_inserido)
            print("---------------------------------------------")

        elif opcao == "2":
            controller.listar()

        elif opcao == "3":
            id_cliente = int(input("ID do cliente a atualizar: "))
            nome = input("Novo nome: ")
            email = input("Novo email: ")
            telefone = ler_telefone("Novo telefone (somente números, com DDD): ")
            telefone = formatar_telefone(telefone)
            endereco = input("Novo endereço: ")

            cliente_obj = Cliente(id_cliente, nome, email, telefone, endereco)
            controller.atualizar(cliente_obj)

        elif opcao == "4":
            id_cliente = int(input("ID do cliente a remover: "))
            confirmar = input("Tem certeza que deseja remover este cliente? (S/N): ").strip().upper()
            if confirmar == "S":
                controller.remover(id_cliente)
            else:
                print("❌ Remoção cancelada.")

        elif opcao == "5":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# MENU PRODUTOS
# ==========================
def menu_produtos(controller):
    while True:
        print("\n--- MENU PRODUTOS ---")
        print("1 - Inserir produto")
        print("2 - Listar produtos")
        print("3 - Atualizar produto")
        print("4 - Remover produto")
        print("5 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descrição: ")
            categoria = input("Categoria: ")
            preco = ler_numero_decimal("Preço: ")
            estoque = ler_numero_inteiro("Quantidade em estoque: ")

            controller.inserir(Produto(None, nome, descricao, preco, estoque, categoria))

        elif opcao == "2":
            controller.listar()

        elif opcao == "3":
            id_produto = int(input("ID do produto a atualizar: "))
            nome = input("Novo nome: ")
            descricao = input("Nova descrição: ")
            categoria = input("Nova categoria: ")
            preco = ler_numero_decimal("Novo preço: ")
            estoque = ler_numero_inteiro("Nova quantidade em estoque: ")

            produto = Produto(id_produto, nome, descricao, preco, estoque, categoria)
            controller.atualizar(produto)

        elif opcao == "4":
            id_produto = int(input("ID do produto a remover: "))
            confirmar = input("Tem certeza que deseja remover este produto? (S/N): ").strip().upper()
            if confirmar == "S":
                controller.remover(id_produto)
            else:
                print("❌ Remoção cancelada.")

        elif opcao == "5":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# MENU PEDIDOS
# ==========================
def menu_pedidos(controller_pedido, controller_cliente, controller_produto):
    while True:
        print("\n--- MENU PEDIDOS ---")
        print("1 - Criar novo pedido")
        print("2 - Listar pedidos")
        print("3 - Ver itens de um pedido")
        print("4 - Remover pedido")
        print("5 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            criar_pedido(controller_pedido, controller_cliente, controller_produto)
        elif opcao == "2":
            controller_pedido.listar_pedidos()
        elif opcao == "3":
            id_pedido = int(input("ID do pedido: "))
            controller_pedido.listar_itens_pedido(id_pedido)
        elif opcao == "4":
            id_pedido = int(input("ID do pedido a remover: "))
            controller_pedido.remover_pedido(id_pedido)
        elif opcao == "5":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# CRIAR PEDIDO
# ==========================
def criar_pedido(controller_pedido, controller_cliente, controller_produto):
    print("\n📦 Criando novo pedido...")
    controller_cliente.listar()
    id_cliente = int(input("\nDigite o ID do cliente: "))
    # Exibir opções de pagamento
    print("\n💳 Formas de pagamento disponíveis:")
    formas_pagamento = ["Dinheiro", "Cartão de Crédito", "Cartão de Débito", "Pix"]
    for i, forma in enumerate(formas_pagamento, start=1):
        print(f"{i} - {forma}")

    opcao_pagamento = int(input("Escolha a forma de pagamento: "))
    if opcao_pagamento not in range(1, len(formas_pagamento) + 1):
        print("❌ Opção inválida! Usando padrão: Dinheiro.")
        forma_pagamento = "Dinheiro"
    else:
        forma_pagamento = formas_pagamento[opcao_pagamento - 1]

    # Buscar endereço do cliente automaticamente
    sql_endereco = "SELECT Endereco FROM CLIENTE WHERE ID_Cliente = ?"
    resultado = controller_pedido.db.executar(sql_endereco, (id_cliente,), fetch=True)
    if resultado and resultado[0][0]:
        endereco = resultado[0][0]
        print(f"📍 Endereço de entrega: {endereco}")
    else:
        print("⚠️ Endereço não encontrado no cadastro do cliente.")
        endereco = input("Informe manualmente o endereço de entrega: ")


    pedido = Pedido(None, id_cliente, None, "Em aberto", 0.0, forma_pagamento, endereco)
    controller_pedido.inserir_pedido(pedido)

    sql_ultimo_id = "SELECT MAX(ID_Pedido) FROM PEDIDO"
    ultimo_id = controller_pedido.db.executar(sql_ultimo_id, fetch=True)[0][0]
    total = 0.0

    while True:
        controller_produto.listar()
        id_produto = int(input("\nDigite o ID do produto (ou 0 para finalizar): "))
        if id_produto == 0:
            break

        quantidade = int(input("Quantidade: "))
        sql_preco = "SELECT Preco FROM PRODUTO WHERE ID_Produto = ?"
        resultado = controller_pedido.db.executar(sql_preco, (id_produto,), fetch=True)
        if not resultado:
            print("❌ Produto não encontrado.")
            continue

        preco_unitario = resultado[0][0]
        subtotal = preco_unitario * quantidade
        total += subtotal

        item = ItemPedido(None, ultimo_id, id_produto, quantidade, preco_unitario, subtotal)
        controller_pedido.inserir_item(item)

    controller_pedido.db.executar(
        "UPDATE PEDIDO SET Valor_Total = ? WHERE ID_Pedido = ?",
        (total, ultimo_id),
        commit=True
    )

    print(f"\n✅ Pedido criado com sucesso! Valor total: R${total:.2f}")


# ==========================
# MENU RELATÓRIOS
# ==========================
def menu_relatorios(controller_relatorios):
    while True:
        print("\n--- MENU RELATÓRIOS ---")
        print("1 - Total de pedidos por cliente")
        print("2 - Total de vendas por categoria")
        print("3 - Voltar")
        opcao = input("Escolha: ")

        if opcao == "1":
            controller_relatorios.relatorio_pedidos_por_cliente()
        elif opcao == "2":
            controller_relatorios.relatorio_vendas_por_categoria()
        elif opcao == "3":
            break
        else:
            print("❌ Opção inválida!")


# ==========================
# EXECUÇÃO PRINCIPAL
# ==========================
if __name__ == "__main__":
    criar_tabelas()
    splash_screen()
    menu_principal()
>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
