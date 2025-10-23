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

