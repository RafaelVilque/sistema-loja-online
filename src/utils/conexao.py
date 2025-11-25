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