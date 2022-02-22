from com.nttdata.dgi.persistence.ipersistor import IPersistor


class Persistor (IPersistor):
    report: dict
    persistor_configuration: dict

    def __init__(self, persistor_configuration):
        self.persistor_configuration = persistor_configuration
        self.report = {}
        return

    def persist(self, *args, **kwargs):
        return self
