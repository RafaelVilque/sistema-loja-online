
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
