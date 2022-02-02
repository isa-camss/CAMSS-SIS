from enum import Enum


class IPersistor:

    def persist(self):
        return self


class PersistorTypes(Enum):
    FILE = 1
    VIRTUOSO = 2
    STARDOG = 3
