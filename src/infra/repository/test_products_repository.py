import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import mongomock
print(mongomock.__file__)
from unittest.mock import MagicMock

import pytest
from pymongo import MongoClient
from mongomock import MongoClient as MockedClient
from faker import Faker
from src.infra.configs.connection import DBConnectionHandler
from src.infra.repository.products_repository import ProductsRepository
from typing import Dict

faker = Faker()

def get_faker_product() -> Dict:
    return {
        "name_product": faker.name(),
        "description": faker.text(),
        "price": faker.random_number(digits=3),
    }

@pytest.fixture
def product_repository():
    # Cria um objeto Database mock
    db_mock = MagicMock()

    # Configura o MockedClient para retornar o objeto Database mock quando get_database é chamado
    connection = MockedClient()
    connection.get_database = MagicMock(return_value=db_mock)

    # Retorna um ProductsRepository com a conexão mock
    return ProductsRepository(connection)

def test_insert_product(product_repository):
    product = get_faker_product()
    result = product_repository.insert_product(product)
    assert product['name_product'] == result['name_product']
    assert product['description'] == result['description']
    assert product['price'] == result['price']

def test_insert_list_product():
    pass

def test_select_many():
    pass

def test_select_one():
    pass

def test_search_products():
    pass


