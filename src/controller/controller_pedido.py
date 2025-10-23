
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
