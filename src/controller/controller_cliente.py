<<<<<<< HEAD
# src/controller/controller_cliente.py
from src.utils.conexao import Conexao
from src.model.cliente import Cliente
from datetime import datetime

class ControllerCliente:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # INSERIR CLIENTE → 1,0 pt (6.b.1.i–iv)
    # ==============================
    def inserir(self, cliente: Cliente):
        # Verifica se já existe cliente com mesmo email (constraint UNIQUE)
        if self.db.find_one("clientes", {"email": cliente.email}):
            print("❌ Erro: Já existe um cliente com esse e-mail.")
            return None

        # Prepara documento para inserção
        doc = {
            "_id": cliente.id_cliente,  # None será substituído pelo próximo ID livre
            "nome_cliente": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "endereco": cliente.endereco,
            "data_cadastro": datetime.now()
        }

        # Se id_cliente for None, gera próximo ID sequencial (simulando AUTOINCREMENT)
        if cliente.id_cliente is None:
            ultimo = self.db.find_one("clientes", sort=[("_id", -1)])
            proximo_id = 1 if ultimo is None else ultimo["_id"] + 1
            doc["_id"] = proximo_id
            cliente.id_cliente = proximo_id

        # Insere no MongoDB
        self.db.insert_one("clientes", doc)
        print("✅ Cliente inserido com sucesso!")
        return cliente

    # ==============================
    # LISTAR CLIENTES → parte de 1,0 pt
    # ==============================
    def listar(self):
        resultados = self.db.find("clientes")
        if resultados:
            print("\n📋 Lista de Clientes:")
            print("-" * 70)
            for doc in resultados:
                print(f"ID: {doc['_id']} | Nome: {doc['nome_cliente']} | "
                      f"Email: {doc['email']} | Telefone: {doc['telefone']} | "
                      f"Endereço: {doc['endereco']}")
        else:
            print("⚠️ Nenhum cliente encontrado.")

    # ==============================
    # ATUALIZAR CLIENTE → 1,0 pt (6.d.1–vi)
    # ==============================
    def atualizar(self, cliente: Cliente):
        doc = {
            "nome_cliente": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "endereco": cliente.endereco
        }
        resultado = self.db.update_one(
            "clientes",
            {"_id": cliente.id_cliente},
            {"$set": doc}
        )

        if resultado.matched_count > 0:
            print("✅ Cliente atualizado com sucesso!")
            # Exibe o registro atualizado (item 6.d.vii = +0,5 pt)
            atualizado = self.buscar_por_id(cliente.id_cliente)
            if atualizado:
                print("\n📝 Registro atualizado:")
                print(atualizado)
            return True
        else:
            print("⚠️ Cliente não encontrado.")
            return False

    # ==============================
    # REMOVER CLIENTE → 1,0 pt + 0,5 pt (6.c.1–vi + 6.c.5.i)
    # ==============================
    def remover(self, id_cliente):
        # Verifica se cliente existe
        cliente = self.buscar_por_id(id_cliente)
        if not cliente:
            print("⚠️ Cliente não encontrado.")
            return

        # ✅ INTEGRIDADE REFERENCIAL: verifica se há pedidos vinculados
        qtd_pedidos = self.db.count_documents("pedidos", {"id_cliente": id_cliente})
        if qtd_pedidos > 0:
            print(f"❗ Não é possível excluir: cliente #{id_cliente} possui {qtd_pedidos} pedido(s) vinculado(s).")
            opcao = input("Deseja excluir todos os pedidos e seus itens primeiro? (S/N): ").strip().upper()
            if opcao == "S":
                # Remove itens dos pedidos primeiro (integridade: filhos antes do pai)
                self.db.delete_many("itens_pedido", {"id_pedido": {"$in": [
                    p["_id"] for p in self.db.find("pedidos", {"id_cliente": id_cliente}, {"_id": 1})
                ]}})
                # Remove pedidos
                self.db.delete_many("pedidos", {"id_cliente": id_cliente})
                print(f"✅ {qtd_pedidos} pedido(s) e seus itens foram removidos.")
            else:
                print("❌ Remoção cancelada.")
                return

        # Remove o cliente
        self.db.delete_one("clientes", {"_id": id_cliente})
        print("✅ Cliente removido com sucesso!")

        # Pergunta se deseja remover mais (item 6.c.vi = parte do 1,0 pt)
        continuar = input("Deseja remover mais algum cliente? (S/N): ").strip().upper()
        if continuar == "S":
            id_prox = input("ID do próximo cliente: ")
            if id_prox.isdigit():
                self.remover(int(id_prox))

    # ==============================
    # BUSCAR CLIENTE POR ID
    # ==============================
    def buscar_por_id(self, id_cliente):
        doc = self.db.find_one("clientes", {"_id": id_cliente})
        if doc:
            return Cliente(
                id_cliente=doc["_id"],
                nome=doc["nome_cliente"],
                email=doc["email"],
                telefone=doc["telefone"],
                endereco=doc["endereco"]
            )
        return None
=======

from src.utils.conexao import Conexao
from src.model.cliente import Cliente

class ControllerCliente:
    def __init__(self):
        self.db = Conexao()

    # ==============================
    # INSERIR CLIENTE
    # ==============================
    def inserir(self, cliente: Cliente):
        sql = """
        INSERT INTO CLIENTE (Nome_Cliente, Email, Telefone, Endereco, Data_Cadastro)
        VALUES (?, ?, ?, ?, date('now'))
        """
        parametros = (cliente.nome, cliente.email, cliente.telefone, cliente.endereco)
        self.db.executar(sql, parametros, commit=True)

        # Recupera o ID gerado automaticamente
        resultado = self.db.executar("SELECT last_insert_rowid()", fetch=True)
        id_gerado = resultado[0][0]
        cliente.id_cliente = id_gerado
        return cliente

    # ==============================
    # LISTAR CLIENTES
    # ==============================
    def listar(self):
        sql = "SELECT ID_Cliente, Nome_Cliente, Email, Telefone, Endereco FROM CLIENTE"
        resultados = self.db.executar(sql, fetch=True)

        if resultados:
            print("\n📋 Lista de Clientes:")
            print("-" * 70)
            for r in resultados:
                print(f"ID: {r[0]} | Nome: {r[1]} | Email: {r[2]} | Telefone: {r[3]} | Endereço: {r[4]}")
        else:
            print("⚠️ Nenhum cliente encontrado.")

    # ==============================
    # ATUALIZAR CLIENTE
    # ==============================
    def atualizar(self, cliente: Cliente):
        sql = """
        UPDATE CLIENTE
        SET Nome_Cliente = ?, Email = ?, Telefone = ?, Endereco = ?
        WHERE ID_Cliente = ?
        """
        parametros = (cliente.nome, cliente.email, cliente.telefone, cliente.endereco, cliente.id_cliente)
        self.db.executar(sql, parametros, commit=True)
        
        # Verifica se realmente atualizou
        resultado = self.db.executar("SELECT changes()", fetch=True)
        if resultado and resultado[0][0] > 0:
            return True
        return False

    # ==============================
    # REMOVER CLIENTE
    # ==============================
    def remover(self, id_cliente):
        sql_check = "SELECT * FROM CLIENTE WHERE ID_Cliente = ?"
        resultado = self.db.executar(sql_check, (id_cliente,), fetch=True)

        if not resultado:
            print("⚠️ Cliente não encontrado no banco de dados.")
            return

        sql_delete = "DELETE FROM CLIENTE WHERE ID_Cliente = ?"
        self.db.executar(sql_delete, (id_cliente,), commit=True)
        print("✅ Cliente removido com sucesso!")

    # ==============================
    # BUSCAR CLIENTE POR ID
    # ==============================
    def buscar_por_id(self, id_cliente):
        sql = "SELECT ID_Cliente, Nome_Cliente, Email, Telefone, Endereco FROM CLIENTE WHERE ID_Cliente = ?"
        resultado = self.db.executar(sql, (id_cliente,), fetch=True)
        if resultado:
            r = resultado[0]
            return Cliente(r[0], r[1], r[2], r[3], r[4])
        return None
>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
