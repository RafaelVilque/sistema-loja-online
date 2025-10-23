import sqlite3

# Conecte ao mesmo banco usado no sistema
conexao = sqlite3.connect("loja.db")
cursor = conexao.cursor()

print("📋 Tabelas existentes:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
for tabela in cursor.fetchall():
    print(" -", tabela[0])

print("\n📋 Registros da tabela CLIENTE:")
cursor.execute("SELECT * FROM CLIENTE;")
registros = cursor.fetchall()
for r in registros:
    print(r)

conexao.close()
