# src/model/produto.py
class Produto:
    def __init__(self, id_produto=None, nome="", descricao="", preco=0.0, estoque=0, categoria="", status="Ativo", url_imagem=""):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.estoque = estoque
        self.categoria = categoria
        self.status = status
        self.url_imagem = url_imagem

    def __str__(self):
        return f"[{self.id_produto}] {self.nome} - R${self.preco:.2f} ({self.categoria})"
