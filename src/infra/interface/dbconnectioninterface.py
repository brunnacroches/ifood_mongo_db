from abc import ABC, abstractmethod

class DBConnectionInterface(ABC):
    @abstractmethod
    def connect_to_db(self):
        pass

    @abstractmethod
    def get_db_connection(self):
        pass

    @abstractmethod
    def get_db_client(self):
        pass

    @abstractmethod
    def get_collection(self, collection_name: str):
        pass
