
from src.utils.conexao import Conexao
from src.model.produto import Produto

class ControllerProduto:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # INSERIR PRODUTO
    # ==============================
    def inserir(self, produto: Produto):
        sql = """
        INSERT INTO PRODUTO (Nome_Produto, Descricao, Preco, Estoque, Categoria, Data_Cadastro, Status_Produto, URL_Imagem)
        VALUES (?, ?, ?, ?, ?, date('now'), ?, ?)
        """
        parametros = (
            produto.nome,
            produto.descricao,
            produto.preco,
            produto.estoque,
            produto.categoria,
            produto.status,
            produto.url_imagem
        )

        try:
            self.db.executar(sql, parametros, commit=True)
            print("✅ Produto inserido com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao inserir produto: {e}")

    # ==============================
    # LISTAR PRODUTOS
    # ==============================
    def listar(self):
        sql = "SELECT ID_Produto, Nome_Produto, Preco, Estoque, Categoria FROM PRODUTO"
        resultados = self.db.executar(sql, fetch=True)

        if resultados:
            print("\n📦 Lista de Produtos:")
            print("-" * 70)
            for r in resultados:
                print(f"ID: {r[0]} | Nome: {r[1]} | Preço: R${r[2]:.2f} | Estoque: {r[3]} | Categoria: {r[4]}")
        else:
            print("⚠️ Nenhum produto encontrado.")

    # ==============================
    # ATUALIZAR PRODUTO
    # ==============================
    def atualizar(self, produto: Produto):
        sql = """
        UPDATE PRODUTO
        SET Nome_Produto = ?, Descricao = ?, Preco = ?, Estoque = ?, Categoria = ?, Status_Produto = ?, URL_Imagem = ?
        WHERE ID_Produto = ?
        """
        parametros = (
            produto.nome,
            produto.descricao,
            produto.preco,
            produto.estoque,
            produto.categoria,
            produto.status,
            produto.url_imagem,
            produto.id_produto
        )
        self.db.executar(sql, parametros, commit=True)
        print("✅ Produto atualizado com sucesso!")

    # ==============================
    # REMOVER PRODUTO
    # ==============================
    def remover(self, id_produto):
        sql_check = "SELECT * FROM PRODUTO WHERE ID_Produto = ?"
        resultado = self.db.executar(sql_check, (id_produto,), fetch=True)

        if not resultado:
            print("⚠️ Produto não encontrado no banco de dados.")
            return

        sql_delete = "DELETE FROM PRODUTO WHERE ID_Produto = ?"
        self.db.executar(sql_delete, (id_produto,), commit=True)
        print("✅ Produto removido com sucesso!")

    # ==============================
    # BUSCAR PRODUTO POR ID
    # ==============================
    def buscar_por_id(self, id_produto):
        sql = """
        SELECT ID_Produto, Nome_Produto, Descricao, Preco, Estoque, Categoria, Status_Produto, URL_Imagem
        FROM PRODUTO
        WHERE ID_Produto = ?
        """
        resultado = self.db.executar(sql, (id_produto,), fetch=True)

        if resultado:
            r = resultado[0]
            return Produto(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
        return None
