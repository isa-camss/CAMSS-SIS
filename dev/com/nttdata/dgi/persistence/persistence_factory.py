from com.nttdata.dgi.persistence.ipersistor import IPersistor
from com.nttdata.dgi.persistence.virtuoso_persistor import VirtuosoPersistor
from enum import Enum


class PersistorType(Enum):
    FILE = 1
    VIRTUOSO = 2
    STARDOG = 3


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
