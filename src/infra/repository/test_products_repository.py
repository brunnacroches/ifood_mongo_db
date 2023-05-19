from bson.objectid import ObjectId
from typing import Dict, List
import pytest
from ...infra.configs.connection import DBConnectionHandler
from ...infra.repository.products_repository import ProductsRepository

@pytest.fixture
def product_repository():
    # Configura a conexão com o banco de dados de teste
    db_connection = DBConnectionHandler()
    db_connection.connect_to_db()
    connection = db_connection.get_db_connection()

    # Retorna um ProductsRepository com a conexão do banco de dados de teste
    return ProductsRepository(connection)


def test_insert_product(product_repository):
    name_product = "Torta de Maçã"
    type_product = "Doce"
    quantity_product = 5

    # Insere um produto
    result = product_repository.insert_product(name_product, type_product, quantity_product)

    # Verifica se o produto foi inserido corretamente
    assert result["name_product"] == name_product
    assert result["type_product"] == type_product
    assert result["quantity_product"] == quantity_product

@pytest.mark.usefixtures("product_repository")
def test_insert_list_of_product(product_repository):
    products = [
        {"name_product": "Torta de Maçã", "type_product": "Doce", "quantify_product": 5},
        {"name_product": "Torta de Morango", "type_product": "Doce", "quantify_product": 10},
        {"name_product": "Torta Salgada", "type_product": "Salgado", "quantify_product": 8},
    ]

    # Insere uma lista de produtos
    result = product_repository.insert_list_of_product(products)

    # Verifica se a lista de produtos foi inserida corretamente
    assert len(result) == len(products)

def test_select_many(product_repository):
    filter = {"type_product": "Doce"}

    # Realiza a consulta na coleção de produtos
    result = product_repository.select_many(filter)

    # Verifica se a consulta retornou os produtos corretos
    assert len(result) > 0

def test_select_one(product_repository):
    filter = {"name_product": "Torta de Maçã"}

    # Realiza a consulta na coleção de produtos
    result = product_repository.select_one(filter)

    # Verifica se a consulta retornou um produto válido
    assert result is not None

def test_select_if_property_exists(product_repository):
    # Realiza a consulta na coleção de produtos
    product_repository.select_if_property_exists()

def test_select_many_order(product_repository):
    # Realiza a consulta na coleção de produtos
    product_repository.select_many_order()

def test_select_or(product_repository):
    # Realiza a consulta na coleção de produtos
    product_repository.select_or()

def test_select_by_object_id(product_repository):
    # Realiza a consulta na coleção de produtos
    product_repository.select_by_object_id()

def test_search_product(product_repository):
    name_product = "Torta de Maçã"

    # Realiza a busca do produto pelo nome
    result = product_repository.search_product(name_product)

    # Verifica se o produto foi encontrado corretamente
    assert result is not None

# @pytest.mark.usefixtures("product_repository")
# def test_delete_product(product_repository):
#     name_product = "Torta de Frango"
    
#     # Deleta o produto pelo nome
#     result = product_repository.delete_product(name_product)
    
#     # Verifica se o produto foi deletado com sucesso
#     assert result is True
