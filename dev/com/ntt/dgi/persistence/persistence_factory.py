from com.ntt.dgi.persistence.persistor import Persistor


class PersistenceFactory:
    configuration: dict

    def __init__(self, persistence_factory_configuration):
        self.configuration = persistence_factory_configuration
        return

    def new_persistor(self, configuration: dict) -> Persistor:
        persistor = Persistor(configuration)
        return persistor
