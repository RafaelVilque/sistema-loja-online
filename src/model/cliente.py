# ==========================
# MODELO DE DADOS: CLIENTE
# ==========================

# Essa classe representa a tabela "cliente"
# Ela serve como um molde para criar objetos que guardam os dados do cliente.

class Cliente:
    def __init__(self, id_cliente=None, nome=None, email=None, telefone=None, endereco=None):
        # Cada atributo aqui corresponde a uma coluna da tabela no banco
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    # Esse método define como o cliente será exibido quando você der "print()"
    def __str__(self):
        return f"[{self.id_cliente}] Nome: {self.nome} - Email: {self.email} - Tel: {self.telefone} - Endereço: {self.endereco}"
