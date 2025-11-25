# src/controller/controller_pedido.py
from src.utils.conexao import Conexao
from src.model.pedido import Pedido, ItemPedido
from datetime import datetime

class ControllerPedido:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # INSERIR PEDIDO
    # ==============================
    def inserir_pedido(self, pedido: Pedido):
        doc = {
            "_id": pedido.id_pedido,
            "id_cliente": pedido.id_cliente,
            "data_pedido": datetime.now(),
            "status_pedido": pedido.status_pedido or "Em aberto",
            "valor_total": float(pedido.valor_total),
            "forma_pagamento": pedido.forma_pagamento or "Dinheiro",
            "endereco_entrega": pedido.endereco_entrega or ""
        }

        if pedido.id_pedido is None:
            ultimo = self.db.find_one("pedidos", sort=[("_id", -1)])
            proximo_id = 1 if ultimo is None else ultimo["_id"] + 1
            doc["_id"] = proximo_id
            pedido.id_pedido = proximo_id

        self.db.insert_one("pedidos", doc)
        print("✅ Pedido inserido com sucesso!")

    # ==============================
    # INSERIR ITEM DO PEDIDO
    # ==============================
    def inserir_item(self, item: ItemPedido):
        produto = self.db.find_one("produtos", {"_id": item.id_produto})
        if not produto:
            print(f"❌ Produto ID {item.id_produto} não encontrado.")
            return False
        if produto["estoque"] < item.quantidade:
            print(f"❌ Estoque insuficiente para '{produto['nome_produto']}'. Disponível: {produto['estoque']}")
            return False

        doc = {
            "_id": item.id_item,
            "id_pedido": item.id_pedido,
            "id_produto": item.id_produto,
            "quantidade": item.quantidade,
            "preco_unitario": float(item.preco_unitario),
            "subtotal": float(item.subtotal)
        }

        if item.id_item is None:
            ultimo = self.db.find_one("itens_pedido", sort=[("_id", -1)])
            doc["_id"] = 1 if ultimo is None else ultimo["_id"] + 1
            item.id_item = doc["_id"]

        self.db.insert_one("itens_pedido", doc)

        self.db.update_one(
            "produtos",
            {"_id": item.id_produto},
            {"$inc": {"estoque": -item.quantidade}}
        )
        print(f"✅ Item inserido e estoque atualizado (–{item.quantidade}).")
        return True

    # ==============================
    # LISTAR PEDIDOS
    # ==============================
    def listar_pedidos(self):
        pipeline = [
            {"$lookup": {"from": "clientes", "localField": "id_cliente", "foreignField": "_id", "as": "cliente"}},
            {"$unwind": "$cliente"},
            {"$project": {"_id": 1, "cliente_nome": "$cliente.nome_cliente", "data_pedido": 1, "valor_total": 1, "status_pedido": 1}},
            {"$sort": {"data_pedido": -1}}
        ]
        resultados = self.db.aggregate("pedidos", pipeline)
        if resultados:
            print("\n🧾 Lista de Pedidos:")
            print("-" * 80)
            for doc in resultados:
                data_fmt = doc["data_pedido"].strftime("%d/%m/%Y") if isinstance(doc["data_pedido"], datetime) else str(doc["data_pedido"])
                print(f"ID: {doc['_id']} | Cliente: {doc['cliente_nome']} | Data: {data_fmt} | Total: R${doc['valor_total']:.2f} | Status: {doc['status_pedido']}")
        else:
            print("⚠️ Nenhum pedido encontrado.")

    # ==============================
    # LISTAR ITENS DE UM PEDIDO
    # ==============================
    def listar_itens_pedido(self, id_pedido):
        pipeline = [
            {"$match": {"id_pedido": id_pedido}},
            {"$lookup": {"from": "produtos", "localField": "id_produto", "foreignField": "_id", "as": "produto"}},
            {"$unwind": "$produto"},
            {"$project": {"_id": 1, "produto_nome": "$produto.nome_produto", "quantidade": 1, "preco_unitario": 1, "subtotal": 1}}
        ]
        resultados = self.db.aggregate("itens_pedido", pipeline)
        if resultados:
            print(f"\n📦 Itens do Pedido {id_pedido}:")
            print("-" * 80)
            for doc in resultados:
                print(f"Item ID: {doc['_id']} | Produto: {doc['produto_nome']} | Qtd: {doc['quantidade']} | Unitário: R${doc['preco_unitario']:.2f} | Subtotal: R${doc['subtotal']:.2f}")
        else:
            print("⚠️ Nenhum item encontrado para este pedido.")

    # ==============================
    # REMOVER PEDIDO
    # ==============================
    def remover_pedido(self, id_pedido):
        pedido = self.db.find_one("pedidos", {"_id": id_pedido})
        if not pedido:
            print("⚠️ Pedido não encontrado.")
            return

        qtd_itens = self.db.count_documents("itens_pedido", {"id_pedido": id_pedido})
        if qtd_itens > 0:
            self.db.delete_many("itens_pedido", {"id_pedido": id_pedido})
            print(f"✅ {qtd_itens} item(s) removido(s).")
            # Devolve estoque
            itens = self.db.find("itens_pedido", {"id_pedido": id_pedido}, {"id_produto": 1, "quantidade": 1})
            for item in itens:
                self.db.update_one("produtos", {"_id": item["id_produto"]}, {"$inc": {"estoque": item["quantidade"]}})

        self.db.delete_one("pedidos", {"_id": id_pedido})
        print("✅ Pedido removido com sucesso!")

        continuar = input("Deseja remover mais algum pedido? (S/N): ").strip().upper()
        if continuar == "S":
            id_prox = input("ID do próximo pedido: ")
            if id_prox.isdigit():
                self.remover_pedido(int(id_prox))

    # ==============================
    # BUSCAR ÚLTIMO PEDIDO
    # ==============================
    def buscar_ultimo(self):
        doc = self.db.find_one("pedidos", sort=[("_id", -1)])
        if doc:
            return Pedido(
                id_pedido=doc["_id"],
                id_cliente=doc["id_cliente"],
                data_pedido=doc["data_pedido"],
                status_pedido=doc["status_pedido"],
                valor_total=doc["valor_total"],
                forma_pagamento=doc["forma_pagamento"],
                endereco_entrega=doc["endereco_entrega"]
            )
        return None

    # ==============================
    # ATUALIZAR VALOR TOTAL
    # ==============================
    def atualizar_valor_total(self, id_pedido, valor_total):
        self.db.update_one("pedidos", {"_id": id_pedido}, {"$set": {"valor_total": float(valor_total)}})