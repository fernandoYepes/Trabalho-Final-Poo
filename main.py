import os
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from database import engine, create_tables
from models import Pessoa, Cidade, Categoria, Produto, Pedido

#bd
Session = sessionmaker(bind=engine)
session = Session()

# Fun CRUD
def create_item(model, **kwargs):
    """Cria novo item no bd"""
    try:
        item = model(**kwargs)
        session.add(item)
        session.commit()
        
        # Busca o ID correto do item (ex: idPedido)
        display_identifier = kwargs.get('nome')
        if not display_identifier:
            pk_attribute_name = f'id{model.__name__}'
            display_identifier = getattr(item, pk_attribute_name, 'ID desconhecido')

        print(f"\n✅ {model.__name__} '{display_identifier}' cadastrado com sucesso!")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Erro ao cadastrar {model.__name__}: {e}")

def list_items(model):
    """Lista todos os itens de um modelo."""
    try:
        items = session.query(model).all()
        if not items:
            print(f"\nℹ️ Nenhuma(a) {model.__name__} cadastrado(a).")
            return
        
        print(f"\n--- Lista de {model.__name__}s ---")
        for item in items:
            if hasattr(item, 'nome'):
                print(f"ID: {getattr(item, f'id{model.__name__}')}, Nome: {item.nome}")
            elif isinstance(item, Pedido):
                cliente_nome = item.cliente.nome if item.cliente else "Cliente não encontrado"
                print(f"ID Pedido: {item.idPedido}, Cliente: {cliente_nome}, Endereço: {item.endereco}, Horário: {item.horario.strftime('%Y-%m-%d %H:%M')}")
            else:
                 print(item)

    except Exception as e:
        print(f"\n❌ Erro ao listar {model.__name__}s: {e}")

def find_item_by_id(model, item_id):
    """Busca um item pelo seu ID."""
    try:
        item = session.query(model).get(item_id)
        if item:
            return item
        else:
            print(f"\nℹ️ {model.__name__} com ID {item_id} não encontrado(a).")
            return None
    except Exception as e:
        print(f"\n❌ Erro ao buscar {model.__name__}: {e}")
        return None

def update_item(model, item_id, **kwargs):
    """Atualiza um item existente."""
    try:
        item = find_item_by_id(model, item_id)
        if item:
            for key, value in kwargs.items():
                if value is not None and value != '':
                    setattr(item, key, value)
            session.commit()
            print(f"\n✅ {model.__name__} com ID {item_id} atualizado(a) com sucesso!")
        else:
            # Função find_item_by_id imprime a mensagem de "não encontrado"
            pass
    except Exception as e:
        session.rollback()
        print(f"\n❌ Erro ao atualizar {model.__name__}: {e}")

def delete_item(model, item_id):
    """Exclui um item."""
    try:
        item = find_item_by_id(model, item_id)
        if item:
            session.delete(item)
            session.commit()
            print(f"\n✅ {model.__name__} com ID {item_id} excluído(a) com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"\n❌ Erro ao excluir {model.__name__}: {e}. Verifique se não há dependências (ex: um cliente em um pedido).")

# --- Funções Específicas para cada Menu ---

def menu_pessoa():
    while True:
        print("\n-- Gerenciar Pessoas 🧑 ( Clientes ) --")
        print("1. Cadastrar Cliente")
        print("2. Listar Clientes")
        print("3. Atualizar Cliente")
        print("4. Excluir Cliente")
        print("0. Voltar ao Menu")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do cliente: ")
            altura = input("Altura (opcional): ")
            nascimento_str = input("Data de Nascimento (AAAA-MM-DD): ")
            endereco = input("Endereço (opcional): ")
            codCidade = input("ID da Cidade: ")

            # Converte
            altura = float(altura) if altura else 1.75
            nascimento = datetime.strptime(nascimento_str, '%Y-%m-%d').date() if nascimento_str else datetime(2004, 11, 19).date()
            
            create_item(Pessoa, nome=nome, altura=altura, nascimento=nascimento, endereco=endereco, codCidade=int(codCidade))

        elif opcao == '2':
            list_items(Pessoa)

        elif opcao == '3':
            item_id = int(input("ID do Cliente a ser atualizado: "))
            print("Em branco para não alterar.")
            nome = input(f"Novo nome: ")
            altura = input(f"Nova altura: ")
            nascimento_str = input(f"Nova data de nascimento (AAAA-MM-DD): ")
            endereco = input(f"Novo endereço: ")
            codCidade = input(f"Novo ID da Cidade: ")

            # Converte apenas se for alterado
            altura = float(altura) if altura else None
            nascimento = datetime.strptime(nascimento_str, '%Y-%m-%d').date() if nascimento_str else None
            codCidade = int(codCidade) if codCidade else None
            
            update_item(Pessoa, item_id, nome=nome, altura=altura, nascimento=nascimento, endereco=endereco, codCidade=codCidade)

        elif opcao == '4':
            item_id = int(input("ID do Cliente a ser excluído: "))
            delete_item(Pessoa, item_id)

        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida, tente novamente")

def menu_cidade():
    while True:
        print("\n-- Gerenciar Cidades 🌆 --")
        print("1. Cadastrar Cidade")
        print("2. Listar Cidades")
        print("3. Atualizar Cidade")
        print("4. Excluir Cidade")
        print("0. Voltar ao Menu")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome da cidade: ")
            create_item(Cidade, nome=nome)
        elif opcao == '2':
            list_items(Cidade)
        elif opcao == '3':
            item_id = int(input("ID da Cidade a ser atualizada: "))
            nome = input("Novo nome da cidade: ")
            update_item(Cidade, item_id, nome=nome)
        elif opcao == '4':
            item_id = int(input("ID da Cidade a ser excluída: "))
            delete_item(Cidade, item_id)
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida, tente novamente")


def menu_categoria():
    while True:
        print("\n-- Gerenciar Categorias 💾 --")
        print("1. Cadastrar Categoria")
        print("2. Listar Categorias")
        print("3. Atualizar Categoria")
        print("4. Excluir Categoria")
        print("0. Voltar ao Menu")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome da categoria: ")
            create_item(Categoria, nome=nome)
        elif opcao == '2':
            list_items(Categoria)
        elif opcao == '3':
            item_id = int(input("ID da Categoria a ser atualizada: "))
            nome = input("Novo nome da categoria: ")
            update_item(Categoria, item_id, nome=nome)
        elif opcao == '4':
            item_id = int(input("ID da Categoria a ser excluída: "))
            delete_item(Categoria, item_id)
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida, tente novamente")

def menu_produto():
    while True:
        print("\n-- Gerenciar Produtos 🎁 --")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Excluir Produto")
        print("0. Voltar ao Menu")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome do produto: ")
            preco = input("Preço (opcional, padrão 10.0): ")
            quantidade = input("Quantidade em estoque (opcional, padrão 0.0): ")
            
            preco = float(preco) if preco else 10.0
            quantidade = float(quantidade) if quantidade else 0.0
            
            create_item(Produto, nome=nome, preco=preco, quantidade=quantidade)

        elif opcao == '2':
            list_items(Produto)

        elif opcao == '3':
            item_id = int(input("ID do Produto a ser atualizado: "))
            print("Deixe em branco para não alterar.")
            nome = input("Novo nome: ")
            preco = input("Novo preço: ")
            quantidade = input("Nova quantidade: ")
            
            preco = float(preco) if preco else None
            quantidade = float(quantidade) if quantidade else None

            update_item(Produto, item_id, nome=nome, preco=preco, quantidade=quantidade)

        elif opcao == '4':
            item_id = int(input("ID do Produto a ser excluído: "))
            delete_item(Produto, item_id)

        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida, tente novamente")

def menu_pedido():
    while True:
        print("\n-- Gerenciar Pedidos 📑 --")
        print("1. Registrar Novo Pedido")
        print("2. Listar Todos os Pedidos")
        print("3. Atualizar Pedido")
        print("4. Excluir Pedido")
        print("0. Voltar ao Menu")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            codCliente = input("ID do Cliente para o pedido: ")
            endereco = input("Endereço de entrega: ")
            
            # Horário definido por padrão (func.now())
            create_item(Pedido, codCliente=int(codCliente), endereco=endereco)

        elif opcao == '2':
            list_items(Pedido)

        elif opcao == '3':
            item_id = int(input("ID do Pedido a ser atualizado: "))
            print("Deixe em branco para não alterar.")
            codCliente = input("Novo ID do cliente: ")
            endereco = input("Novo endereço de entrega: ")
            
            codCliente = int(codCliente) if codCliente else None

            update_item(Pedido, item_id, codCliente=codCliente, endereco=endereco)

        elif opcao == '4':
            item_id = int(input("ID do Pedido a ser excluído: "))
            delete_item(Pedido, item_id)

        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida, tente novamente")

def menu_principal():
    """Exibe menu principal e direciona para os submenus."""
    # Limpa tela
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("🌸 Bem-vindo ao Sistema da Floricultura Flores & Sabores 🌺")
    while True:
        print("\n-- MENU --")
        print("1. Gerenciar Clientes")
        print("2. Gerenciar Cidades")
        print("3. Gerenciar Categorias de Produtos")
        print("4. Gerenciar Produtos")
        print("5. Gerenciar Pedidos")
        print("0. Sair do Sistema")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            menu_pessoa()
        elif opcao == '2':
            menu_cidade()
        elif opcao == '3':
            menu_categoria()
        elif opcao == '4':
            menu_produto()
        elif opcao == '5':
            menu_pedido()
        elif opcao == '0':
            print("\n👋 Obrigado por usar o sistema! Te vejo depois!")
            break
        else:
            print("\n❌ Opção inválida, tente novamente")

if __name__ == "__main__":
    # Tabelas são criadas antes de rodar o programa
    create_tables()
    # Inicia menu
    menu_principal()
    # Fecha sessão
    session.close()
