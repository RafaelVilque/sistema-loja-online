<<<<<<< HEAD
# src/controller/controller_relatorios.py
from src.utils.conexao import Conexao

class ControllerRelatorios:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # RELATÓRIO 1: Total de pedidos e valor por cliente — ✅ 1,0 pt (6.a.1.i)
    # ==============================
    def relatorio_pedidos_por_cliente(self):
        print("\n📊 RELATÓRIO: Total de pedidos e valor por cliente")
        print("=" * 70)

        pipeline = [
            {
                "$lookup": {
                    "from": "clientes",
                    "localField": "id_cliente",
                    "foreignField": "_id",
                    "as": "cliente"
                }
            },
            {"$unwind": "$cliente"},
            {
                "$group": {
                    "_id": "$cliente._id",
                    "nome_cliente": {"$first": "$cliente.nome_cliente"},
                    "total_pedidos": {"$sum": 1},
                    "valor_total": {"$sum": "$valor_total"}
                }
            },
            {"$sort": {"valor_total": -1}}
        ]

        resultados = self.db.aggregate("pedidos", pipeline)

        if not resultados:
            print("⚠️ Nenhum pedido encontrado para agrupar.")
            return

        print(f"{'Cliente':<25} | {'Pedidos'} | {'Valor Total'}")
        print("-" * 70)
        for doc in resultados:
            print(f"{doc['nome_cliente']:<25} | {doc['total_pedidos']:<8} | R${doc['valor_total']:.2f}")

    # ==============================
    # RELATÓRIO 2: Vendas por categoria — ✅ 0,5 pt (6.a.1.ii)
    # Junção: itens_pedido → produtos → agrupar por categoria
    # ==============================
    def relatorio_vendas_por_categoria(self):
        print("\n📊 RELATÓRIO: Total vendido por categoria de produto")
        print("=" * 70)

        pipeline = [
            # Etapa 1: junta itens_pedido com produtos
            {
                "$lookup": {
                    "from": "produtos",
                    "localField": "id_produto",
                    "foreignField": "_id",
                    "as": "produto"
                }
            },
            {"$unwind": "$produto"},

            # Etapa 2: soma subtotal por categoria
            {
                "$group": {
                    "_id": "$produto.categoria",
                    "total_vendido": {"$sum": "$subtotal"},
                    "qtd_itens": {"$sum": "$quantidade"}
                }
            },
            {"$sort": {"total_vendido": -1}}
        ]

        resultados = self.db.aggregate("itens_pedido", pipeline)

        if not resultados:
            print("⚠️ Nenhum item de pedido encontrado para agrupar.")
            return

        print(f"{'Categoria':<20} | {'Itens Vendidos'} | {'Total Vendido'}")
        print("-" * 70)
        for doc in resultados:
            categoria = doc["_id"] or "Sem categoria"
            print(f"{categoria:<20} | {doc['qtd_itens']:<14} | R${doc['total_vendido']:.2f}")
=======
# src/controller/controller_relatorios.py
from src.utils.conexao import Conexao

class ControllerRelatorios:
    def __init__(self):
        self.db = Conexao()

    # 🔹 Relatório 1 — Total de pedidos por cliente
    def relatorio_pedidos_por_cliente(self):
        sql = """
        SELECT 
            C.Nome_Cliente,
            P.ID_Pedido,
            P.Data_Pedido,
            P.Forma_Pagamento,
            P.Endereco_Entrega,
            P.Valor_Total
        FROM PEDIDO P
        INNER JOIN CLIENTE C ON P.ID_Cliente = C.ID_Cliente
        ORDER BY C.Nome_Cliente, P.Data_Pedido DESC
        """
        pedidos = self.db.executar(sql, fetch=True)

        if not pedidos:
            print("⚠️ Nenhum pedido encontrado.")
            return

        print("\n📊 RELATÓRIO DE PEDIDOS POR CLIENTE")
        print("=" * 80)

        for pedido in pedidos:
            nome_cliente = pedido[0]
            id_pedido = pedido[1]
            data_pedido = pedido[2]
            forma_pagamento = pedido[3]
            endereco = pedido[4]
            total = pedido[5]

            print(f"\n👤 Cliente: {nome_cliente}")
            print(f"🧾 Pedido Nº {id_pedido} | Data: {data_pedido}")
            print(f"💳 Pagamento: {forma_pagamento}")
            print(f"📍 Endereço: {endereco}")
            print(f"💰 Valor Total: R${total:.2f}")
            print("🛒 Itens do Pedido:")

        # Buscar itens do pedido
            sql_itens = """
            SELECT PR.Nome_Produto, I.Quantidade, I.Preco_Unitario, I.Subtotal
            FROM ITENS_PEDIDO I
            INNER JOIN PRODUTO PR ON I.ID_Produto = PR.ID_Produto
            WHERE I.ID_Pedido = ?
            """
            itens = self.db.executar(sql_itens, (id_pedido,), fetch=True)

            if itens:
                for item in itens:
                    nome_produto, qtd, preco, subtotal = item
                    print(f"   - {nome_produto} | Qtd: {qtd} | Unitário: R${preco:.2f} | Subtotal: R${subtotal:.2f}")
            else:
                print("   ⚠️ Nenhum item registrado neste pedido.")

            print("-" * 80)


    # 🔹 Relatório 2 — Total de vendas por categoria de produto
    def relatorio_vendas_por_categoria(self):
        sql = """
        SELECT 
            PR.Categoria,
            SUM(I.Quantidade) AS Total_Produtos_Vendidos,
            SUM(I.Subtotal) AS Total_Vendas
        FROM ITENS_PEDIDO I
        INNER JOIN PRODUTO PR ON I.ID_Produto = PR.ID_Produto
        GROUP BY PR.Categoria
        ORDER BY Total_Vendas DESC
        """
        resultados = self.db.executar(sql, fetch=True)

        if not resultados:
            print("⚠️ Nenhuma venda encontrada.")
            return

        print("\n📈 RELATÓRIO DE VENDAS POR CATEGORIA")
        print("=" * 80)
        print(f"{'Categoria':<25} | {'Qtd Vendida':<15} | {'Total de Vendas (R$)':<20}")
        print("-" * 80)

        total_geral = 0

        for categoria, qtd_vendida, total_vendas in resultados:
            total_geral += total_vendas
            print(f"{categoria:<25} | {qtd_vendida:<15} | R${total_vendas:<20.2f}")

        print("-" * 80)
        print(f"{'TOTAL GERAL':<25} | {'':<15} | R${total_geral:<20.2f}")
        print("=" * 80)

>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
