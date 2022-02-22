from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.virtuoso_persistor import VirtuosoPersistor
from enum import IntEnum


class PersistorType(IntEnum):
    NONE = 0
    FILE = 1
    VIRTUOSO = 2
    STARDOG = 3
    GRAPHDB = 4
    ELASTIC = 5


class PersistenceFactory:
    configuration: dict

    def __init__(self):
        pass

    @staticmethod
    def new(persistor_type: PersistorType, **persistor_configuration) -> IPersistor:
        persistor: IPersistor = None
        if PersistorType.VIRTUOSO is persistor_type:
            persistor: VirtuosoPersistor = VirtuosoPersistor(persistor_configuration)
        return persistor
