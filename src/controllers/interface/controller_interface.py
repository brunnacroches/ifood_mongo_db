from abc import ABC, abstractmethod


class ControllerInterface(ABC):

    @abstractmethod
    def controllerinterface(self, *args, **kwargs):
        pass