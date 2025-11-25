<<<<<<< HEAD
# src/controller/controller_produto.py
from src.utils.conexao import Conexao
from src.model.produto import Produto
from datetime import datetime

class ControllerProduto:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # INSERIR PRODUTO → 1,0 pt (6.b.1.i–iv)
    # ==============================
    def inserir(self, produto: Produto):
        # Verifica duplicidade de nome (opcional — não obrigatório, mas bom UX)
        if self.db.find_one("produtos", {"nome_produto": produto.nome}):
            print("⚠️ Aviso: Já existe um produto com esse nome.")

        doc = {
            "_id": produto.id_produto,
            "nome_produto": produto.nome,
            "descricao": produto.descricao,
            "preco": float(produto.preco),
            "estoque": int(produto.estoque),
            "categoria": produto.categoria,
            "data_cadastro": datetime.now(),
            "status_produto": produto.status or "Ativo",
            "url_imagem": produto.url_imagem or ""
        }

        # Gera próximo ID se necessário (simulando AUTOINCREMENT)
        if produto.id_produto is None:
            ultimo = self.db.find_one("produtos", sort=[("_id", -1)])
            proximo_id = 1 if ultimo is None else ultimo["_id"] + 1
            doc["_id"] = proximo_id
            produto.id_produto = proximo_id

        self.db.insert_one("produtos", doc)
        print("✅ Produto inserido com sucesso!")
        return produto

    # ==============================
    # LISTAR PRODUTOS
    # ==============================
    def listar(self):
        resultados = self.db.find("produtos")
        if resultados:
            print("\n📦 Lista de Produtos:")
            print("-" * 70)
            for doc in resultados:
                print(f"ID: {doc['_id']} | Nome: {doc['nome_produto']} | "
                      f"Categoria: {doc['categoria']} | "
                      f"Preço: R${doc['preco']:.2f} | Estoque: {doc['estoque']}")
        else:
            print("⚠️ Nenhum produto encontrado.")

    # ==============================
    # ATUALIZAR PRODUTO → 1,0 pt + 0,5 pt (6.d.vii–viii)
    # ==============================
    def atualizar(self, produto: Produto):
        doc = {
            "nome_produto": produto.nome,
            "descricao": produto.descricao,
            "preco": float(produto.preco),
            "estoque": int(produto.estoque),
            "categoria": produto.categoria,
            "status_produto": produto.status or "Ativo",
            "url_imagem": produto.url_imagem or ""
        }
        resultado = self.db.update_one(
            "produtos",
            {"_id": produto.id_produto},
            {"$set": doc}
        )

        if resultado.matched_count > 0:
            print("✅ Produto atualizado com sucesso!")
            # Exibe o registro atualizado (item 6.d.vii = +0,5 pt)
            atualizado = self.buscar_por_id(produto.id_produto)
            if atualizado:
                print("\n📝 Registro atualizado:")
                print(atualizado)
            return True
        else:
            print("⚠️ Produto não encontrado.")
            return False

    # ==============================
    # REMOVER PRODUTO → 1,0 pt + 0,5 pt (6.c.5.i — integridade referencial)
    # ==============================
    def remover(self, id_produto):
        produto = self.buscar_por_id(id_produto)
        if not produto:
            print("⚠️ Produto não encontrado.")
            return

        # ✅ INTEGRIDADE REFERENCIAL: verifica se há itens vinculados
        qtd_itens = self.db.count_documents("itens_pedido", {"id_produto": id_produto})
        if qtd_itens > 0:
            print(f"❗ Não é possível excluir: produto #{id_produto} está em {qtd_itens} item(s) de pedido.")
            opcao = input("Deseja remover todos os itens vinculados primeiro? (S/N): ").strip().upper()
            if opcao == "S":
                # Remove itens de pedido que usam este produto
                self.db.delete_many("itens_pedido", {"id_produto": id_produto})
                print(f"✅ {qtd_itens} item(s) removido(s).")
            else:
                print("❌ Remoção cancelada.")
                return

        # Remove o produto
        self.db.delete_one("produtos", {"_id": id_produto})
        print("✅ Produto removido com sucesso!")

        # Loop de repetição (item 6.c.vi)
        continuar = input("Deseja remover mais algum produto? (S/N): ").strip().upper()
        if continuar == "S":
            id_prox = input("ID do próximo produto: ")
            if id_prox.isdigit():
                self.remover(int(id_prox))

    # ==============================
    # BUSCAR PRODUTO POR ID
    # ==============================
    def buscar_por_id(self, id_produto):
        doc = self.db.find_one("produtos", {"_id": id_produto})
        if doc:
            return Produto(
                id_produto=doc["_id"],
                nome=doc["nome_produto"],
                descricao=doc["descricao"],
                preco=doc["preco"],
                estoque=doc["estoque"],
                categoria=doc["categoria"],
                status=doc["status_produto"],
                url_imagem=doc["url_imagem"]
            )
        return None
=======

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
>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
