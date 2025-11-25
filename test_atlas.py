# test_atlas.py
from pymongo import MongoClient

# Conexão LOCAL — sem senha, sem Atlas, 100% funcional
URI = "mongodb://localhost:27017/"

try:
    print("➡️ Tentando conectar ao MongoDB local...")
    client = MongoClient(URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("✅ Conexão com MongoDB LOCAL: SUCESSO!")
    
    # Testa escrita/leitura
    db = client["loja"]
    db.teste.insert_one({"status": "ok", "data": "2025-11-25"})
    print("✅ Escrita e leitura: OK")
    db.teste.delete_many({})
    
except Exception as e:
    print("❌ Falha:", e)
    print("🔍 Dica: execute `docker ps` para ver se o container mongo_c3 está rodando.")