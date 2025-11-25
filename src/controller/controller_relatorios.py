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