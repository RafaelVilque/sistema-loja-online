# src/scripts/sqlite_to_mongo.py
import sqlite3
from datetime import datetime
from pymongo import MongoClient

# ==========================
# CONFIGURAÇÕES
# ==========================
SQLITE_DB = "loja.db"
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "loja"


# ==========================
# CONECTA AO MONGODB
# ==========================
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# Limpa coleções anteriores (opcional — útil em testes)
# db.clientes.drop()
# db.produtos.drop()
# db.pedidos.drop()
# db.itens_pedido.drop()

print("➡️ Conectando ao SQLite e MongoDB...")

# ==========================
# CONEXÃO COM SQLITE
# ==========================
conn_sqlite = sqlite3.connect(SQLITE_DB)
cursor = conn_sqlite.cursor()

# ==========================
# FUNÇÃO AUXILIAR: converter DATE para datetime
# ==========================
def str_to_date(date_str):
    if not date_str:
        return datetime.now()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return datetime.now()

# ==========================
# 1. MIGRAR CLIENTES
# ==========================
print("\n📦 Migrando CLIENTES...")
cursor.execute("SELECT ID_Cliente, Nome_Cliente, Email, Telefone, Endereco, Data_Cadastro FROM CLIENTE")
clientes = []
for row in cursor.fetchall():
    doc = {
        "_id": row[0],
        "nome_cliente": row[1],
        "email": row[2],
        "telefone": row[3],
        "endereco": row[4],
        "data_cadastro": str_to_date(row[5])
    }
    clientes.append(doc)

if clientes:
    db.clientes.insert_many(clientes)
    print(f"✅ {len(clientes)} clientes migrados.")
else:
    db.clientes.create_index("email", unique=True)  # mantém constraint UNIQUE
    print("⚠️ Nenhum cliente encontrado.")

# ==========================
# 2. MIGRAR PRODUTOS
# ==========================
print("\n📦 Migrando PRODUTOS...")
cursor.execute("""
    SELECT ID_Produto, Nome_Produto, Descricao, Preco, Estoque, 
           Categoria, Data_Cadastro, Status_Produto, URL_Imagem 
    FROM PRODUTO
""")
produtos = []
for row in cursor.fetchall():
    doc = {
        "_id": row[0],
        "nome_produto": row[1],
        "descricao": row[2],
        "preco": float(row[3]),
        "estoque": row[4],
        "categoria": row[5],
        "data_cadastro": str_to_date(row[6]),
        "status_produto": row[7] or "Ativo",
        "url_imagem": row[8] or ""
    }
    produtos.append(doc)

if produtos:
    db.produtos.insert_many(produtos)
    print(f"✅ {len(produtos)} produtos migrados.")
else:
    print("⚠️ Nenhum produto encontrado.")

# ==========================
# 3. MIGRAR PEDIDOS
# ==========================
print("\n📦 Migrando PEDIDOS...")
cursor.execute("""
    SELECT ID_Pedido, ID_Cliente, Data_Pedido, Status_Pedido, 
           Valor_Total, Forma_Pagamento, Endereco_Entrega 
    FROM PEDIDO
""")
pedidos = []
for row in cursor.fetchall():
    doc = {
        "_id": row[0],
        "id_cliente": row[1],
        "data_pedido": str_to_date(row[2]),
        "status_pedido": row[3] or "Em aberto",
        "valor_total": float(row[4]),
        "forma_pagamento": row[5] or "Dinheiro",
        "endereco_entrega": row[6] or ""
    }
    pedidos.append(doc)

if pedidos:
    db.pedidos.insert_many(pedidos)
    print(f"✅ {len(pedidos)} pedidos migrados.")
else:
    print("⚠️ Nenhum pedido encontrado.")

# ==========================
# 4. MIGRAR ITENS_PEDIDO
# ==========================
print("\n📦 Migrando ITENS_PEDIDO...")
cursor.execute("""
    SELECT ID_Item, ID_Pedido, ID_Produto, Quantidade, 
           Preco_Unitario, Subtotal 
    FROM ITENS_PEDIDO
""")
itens = []
for row in cursor.fetchall():
    doc = {
        "_id": row[0],
        "id_pedido": row[1],
        "id_produto": row[2],
        "quantidade": row[3],
        "preco_unitario": float(row[4]),
        "subtotal": float(row[5])
    }
    itens.append(doc)

if itens:
    db.itens_pedido.insert_many(itens)
    print(f"✅ {len(itens)} itens migrados.")
else:
    print("⚠️ Nenhum item de pedido encontrado.")

# ==========================
# FINALIZAÇÃO
# ==========================
conn_sqlite.close()
client.close()
print("\n🎉 Migração concluída com sucesso!")
print(f"👉 Coleções criadas: clientes, produtos, pedidos, itens_pedido")