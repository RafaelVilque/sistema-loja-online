<<<<<<< HEAD
# src/utils/conexao.py
from pymongo import MongoClient
import os

class Conexao:
    """Gerencia a conexão com o MongoDB."""
    
    def __init__(self, uri="mongodb://localhost:27017/", db_name="loja"):
        self.uri = uri
        self.db_name = db_name
        self._client = None
        self._db = None

    def conectar(self):
        if self._client is None:
            self._client = MongoClient(self.uri)
            self._db = self._client[self.db_name]
        return self._db

    def get_collection(self, nome):
        db = self.conectar()
        return db[nome]

    def count_documents(self, colecao):
        coll = self.get_collection(colecao)
        return coll.count_documents({})

    def find(self, colecao, filtro={}, projecao=None):
        coll = self.get_collection(colecao)
        return list(coll.find(filtro, projecao))

    def find_one(self, colecao, filtro={}):
        coll = self.get_collection(colecao)
        return coll.find_one(filtro)

    def insert_one(self, colecao, documento):
        coll = self.get_collection(colecao)
        return coll.insert_one(documento)

    def update_one(self, colecao, filtro, atualizacao):
        coll = self.get_collection(colecao)
        return coll.update_one(filtro, atualizacao)

    def delete_one(self, colecao, filtro):
        coll = self.get_collection(colecao)
        return coll.delete_one(filtro)

    def aggregate(self, colecao, pipeline):
        coll = self.get_collection(colecao)
        return list(coll.aggregate(pipeline))

    def fechar(self):
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
=======
# src/utils/conexao.py
import sqlite3
import os

class Conexao:
    """Gerencia a conexão única com o banco SQLite."""
    def __init__(self, nome_banco="loja.db"):
        self.nome_banco = nome_banco
        self._conexao = None

    def conectar(self):
        if self._conexao is None:
            self._conexao = sqlite3.connect(self.nome_banco)
        return self._conexao

    def executar(self, sql, parametros=(), fetch=False, commit=False):
        conexao = self.conectar()
        try:
            cursor = conexao.cursor()
            cursor.execute(sql, parametros)

            if commit:
                conexao.commit()

            if fetch:
                return cursor.fetchall()

        except sqlite3.Error as e:
            print(f"❌ Erro ao executar SQL: {e}")

    def fechar(self):
        if self._conexao:
            self._conexao.close()
            self._conexao = None


def criar_tabelas():
    """Cria as tabelas do banco se ainda não existirem."""
    caminho_script = os.path.join("scripts", "script.sql")

    if not os.path.exists("loja.db"):
        print("🧱 Criando banco de dados...")
        conexao = sqlite3.connect("loja.db")
        cursor = conexao.cursor()

        if os.path.exists(caminho_script):
            print(f"📄 Executando script SQL: {caminho_script}")
            with open(caminho_script, "r", encoding="utf-8") as arquivo:
                script = arquivo.read()
                cursor.executescript(script)
            conexao.commit()
            conexao.close()
            print("✅ Banco de dados criado com sucesso!")
        else:
            print(f"❌ ERRO: Arquivo {caminho_script} não encontrado.")
    else:
        print("ℹ️ Banco de dados já existe — nenhuma ação necessária.")
>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
