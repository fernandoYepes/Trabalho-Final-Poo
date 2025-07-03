import datetime
from sqlalchemy import (Column, Integer, String, Float, Date, DateTime, Text,
                        ForeignKey, func)
from sqlalchemy.orm import relationship
from database import Base

class Cidade(Base):
    """
    Modelo ORM para a tabela 'Cidade'.
    Armazena as cidades de onde os clientes vêm.
    """
    __tablename__ = "cidade"

    idCidade = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    # uma cidade pode ter várias pessoas
    pessoas = relationship("Pessoa", back_populates="cidade")

    def __repr__(self):
        return f"<Cidade(id={self.idCidade}, nome='{self.nome}')>"

class Pessoa(Base):
    """
    Modelo ORM para a tabela 'Pessoa' (Clientes).
    """
    __tablename__ = "pessoa"

    idPessoa = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    altura = Column(Float, default=1.76)
    nascimento = Column(Date, default=datetime.date(1989, 12, 19))
    endereco = Column(Text)
    
    # Chave Estrangeira -> tabela Cidade
    codCidade = Column(Integer, ForeignKey("cidade.idCidade"))

    # pessoa pertence a uma cidade
    cidade = relationship("Cidade", back_populates="pessoas")
    
    # Uma pessoa pode ter vários pedidos
    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"<Pessoa(id={self.idPessoa}, nome='{self.nome}')>"

class Categoria(Base):
    """
    Modelo ORM para a tabela 'Categoria'.
    Categoriza os produtos (e.g., Flores, Arranjos, Doces).
    """
    __tablename__ = "categoria"

    idCategoria = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Categoria(id={self.idCategoria}, nome='{self.nome}')>"

class Produto(Base):
    """
    Modelo ORM para a tabela 'Produto'.
    Armazena os itens vendidos pela floricultura.
    """
    __tablename__ = "produto"

    idProduto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    preco = Column(Float, default=10.0)
    quantidade = Column(Float, default=0.0)
    
    # idCategoria = Column(Integer, ForeignKey("categoria.idCategoria"))

    def __repr__(self):
        return f"<Produto(id={self.idProduto}, nome='{self.nome}', preco={self.preco})>"

class Pedido(Base):
    """
    Modelo ORM para a tabela 'Pedido'.
    Registra os pedidos feitos pelos clientes.
    """
    __tablename__ = "pedido"

    idPedido = Column(Integer, primary_key=True, autoincrement=True)
    horario = Column(DateTime, default=func.now()) # Usa função NOW() do bd
    endereco = Column(Text)
    
    # Chave Estrangeira para tabela Pessoa
    codCliente = Column(Integer, ForeignKey("pessoa.idPessoa"))

    # Um pedido pertence a um cliente
    cliente = relationship("Pessoa", back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(id={self.idPedido}, cliente_id={self.codCliente}, horario='{self.horario}')>"
