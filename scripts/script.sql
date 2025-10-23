CREATE TABLE CLIENTE (
    ID_Cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome_Cliente VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Telefone VARCHAR(20),
    Endereco VARCHAR(500),
    Data_Cadastro DATE NOT NULL,
);


CREATE TABLE PRODUTO (
    ID_Produto INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome_Produto VARCHAR(255) NOT NULL,
    Descricao TEXT,
    Preco DECIMAL(10, 2) NOT NULL,
    Estoque INT NOT NULL,
    Categoria VARCHAR(100),
    Data_Cadastro DATE NOT NULL,
    Status_Produto VARCHAR(50),
    URL_Imagem VARCHAR(500)
);

CREATE TABLE PEDIDO (
    ID_Pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Cliente INT NOT NULL,
    Data_Pedido DATE NOT NULL,
    Status_Pedido VARCHAR(50),
    Valor_Total DECIMAL(10, 2) NOT NULL,
    Forma_Pagamento VARCHAR(100),
    Endereco_Entrega VARCHAR(500),
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);

CREATE TABLE ITENS_PEDIDO (
    ID_Item INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Pedido INT NOT NULL,
    ID_Produto INT NOT NULL,
    Quantidade INT NOT NULL,
    Preco_Unitario DECIMAL(10, 2) NOT NULL,
    Subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (ID_Pedido) REFERENCES PEDIDO(ID_Pedido),
    FOREIGN KEY (ID_Produto) REFERENCES PRODUTO(ID_Produto)
);
