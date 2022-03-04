from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.persistor_type import PersistorType


class PersistorArgumentError(ValueError):
    pass


class Persistor (IPersistor):

    type: PersistorType

    def __init__(self):
        self.type = PersistorType.NONE
        return

    def persist(self, *args, **kwargs):
        return self

    def drop(self, *args, **kwargs):
        return self

    def select(self, *args, **kwargs):
        return self
