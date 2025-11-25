<<<<<<< HEAD
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
=======

from src.utils.conexao import Conexao
from src.model.pedido import Pedido
from src.model.pedido import ItemPedido  # Corrigido: o ItemPedido deve vir de model/item_pedido.py

class ControllerPedido:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # INSERIR PEDIDO
    # ==============================
    def inserir_pedido(self, pedido: Pedido):
        sql = """
        INSERT INTO PEDIDO (ID_Cliente, Data_Pedido, Status_Pedido, Valor_Total, Forma_Pagamento, Endereco_Entrega)
        VALUES (?, date('now'), ?, ?, ?, ?)
        """
        parametros = (
            pedido.id_cliente,
            pedido.status_pedido,
            pedido.valor_total,
            pedido.forma_pagamento,
            pedido.endereco_entrega
        )

        try:
            self.db.executar(sql, parametros, commit=True)

            # Obtém o último ID gerado automaticamente
            resultado = self.db.executar("SELECT last_insert_rowid()", fetch=True)
            pedido.id_pedido = resultado[0][0]
            print("✅ Pedido inserido com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao inserir pedido: {e}")

    # ==============================
    # LISTAR PEDIDOS
    # ==============================
    def listar_pedidos(self):
        sql = """
        SELECT P.ID_Pedido, C.Nome_Cliente, P.Data_Pedido, P.Valor_Total, P.Status_Pedido
        FROM PEDIDO P
        INNER JOIN CLIENTE C ON P.ID_Cliente = C.ID_Cliente
        ORDER BY P.Data_Pedido DESC
        """
        resultados = self.db.executar(sql, fetch=True)

        if resultados:
            print("\n🧾 Lista de Pedidos:")
            print("-" * 80)
            for r in resultados:
                print(f"ID: {r[0]} | Cliente: {r[1]} | Data: {r[2]} | Total: R${r[3]:.2f} | Status: {r[4]}")
        else:
            print("⚠️ Nenhum pedido encontrado.")

    # ==============================
    # INSERIR ITEM DO PEDIDO
    # ==============================
    def inserir_item(self, item: ItemPedido):
        sql_insert = """
        INSERT INTO ITENS_PEDIDO (ID_Pedido, ID_Produto, Quantidade, Preco_Unitario, Subtotal)
        VALUES (?, ?, ?, ?, ?)
        """
        parametros_insert = (
            item.id_pedido,
            item.id_produto,
            item.quantidade,
            item.preco_unitario,
            item.subtotal
        )

    # Atualiza o estoque do produto
        sql_update_estoque = """
        UPDATE PRODUTO
        SET Estoque = Estoque - ?
        WHERE ID_Produto = ?
        """

        try:
        # Insere o item
            self.db.executar(sql_insert, parametros_insert, commit=True)

        # Atualiza o estoque
            self.db.executar(sql_update_estoque, (item.quantidade, item.id_produto), commit=True)

            print(f"✅ Item inserido com sucesso! Estoque atualizado (-{item.quantidade}) para o produto {item.id_produto}.")
        except Exception as e:
            print(f"❌ Erro ao inserir item: {e}")




    # ==============================
    # LISTAR ITENS DE UM PEDIDO
    # ==============================
    def listar_itens_pedido(self, id_pedido):
        sql = """
        SELECT I.ID_Item, P.Nome_Produto, I.Quantidade, I.Preco_Unitario, I.Subtotal
        FROM ITENS_PEDIDO I
        INNER JOIN PRODUTO P ON I.ID_Produto = P.ID_Produto
        WHERE I.ID_Pedido = ?
        """
        resultados = self.db.executar(sql, (id_pedido,), fetch=True)

        if resultados:
            print(f"\n📦 Itens do Pedido {id_pedido}:")
            print("-" * 80)
            for r in resultados:
                print(f"Item ID: {r[0]} | Produto: {r[1]} | Qtd: {r[2]} | Unitário: R${r[3]:.2f} | Subtotal: R${r[4]:.2f}")
        else:
            print("⚠️ Nenhum item encontrado para este pedido.")

    # ==============================
    # REMOVER PEDIDO
    # ==============================
    def remover_pedido(self, id_pedido):
        try:
            # Primeiro remove os itens associados
            self.db.executar("DELETE FROM ITENS_PEDIDO WHERE ID_Pedido = ?", (id_pedido,), commit=True)
            # Depois remove o pedido
            self.db.executar("DELETE FROM PEDIDO WHERE ID_Pedido = ?", (id_pedido,), commit=True)
            print("✅ Pedido e itens removidos com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao remover pedido: {e}")
>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
