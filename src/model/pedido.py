from datetime import datetime

# ==============================
# CLASSE ITEM DO PEDIDO
# ==============================
class ItemPedido:
    def __init__(self, id_item=None, id_pedido=None, id_produto=None, quantidade=0, preco_unitario=0.0, subtotal=0.0):
        self.id_item = id_item
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = subtotal

    def __str__(self):
        return f"Produto {self.id_produto} | Qtd: {self.quantidade} | Unitário: R${self.preco_unitario:.2f} | Subtotal: R${self.subtotal:.2f}"


# ==============================
# CLASSE PEDIDO
# ==============================
class Pedido:
    def __init__(
        self,
        id_pedido=None,
        id_cliente=None,
        data_pedido=None,
        status_pedido="Em aberto",
        valor_total=0.0,
        forma_pagamento="",
        endereco_entrega=""
    ):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido or datetime.now()
        self.status_pedido = status_pedido
        self.valor_total = valor_total
        self.forma_pagamento = forma_pagamento
        self.endereco_entrega = endereco_entrega

        # inicializa lista de itens
        self.itens = []

    # ==============================
    # ADICIONAR ITEM AO PEDIDO
    # ==============================
    def adicionar_item(self, item: ItemPedido):
        self.itens.append(item)
        self.valor_total += item.subtotal

    # ==============================
    # REPRESENTAÇÃO TEXTUAL
    # ==============================
    def __str__(self):
        itens_str = "\n".join([f" - {item}" for item in self.itens]) if self.itens else "Nenhum item adicionado."
        return (
            f"🧾 Pedido #{self.id_pedido or 'N/I'}\n"
            f"Cliente ID: {self.id_cliente}\n"
            f"Data: {self.data_pedido.strftime('%d/%m/%Y %H:%M')}\n"
            f"Status: {self.status_pedido}\n"
            f"Itens:\n{itens_str}\n"
            f"Total: R${self.valor_total:.2f}"
        )
