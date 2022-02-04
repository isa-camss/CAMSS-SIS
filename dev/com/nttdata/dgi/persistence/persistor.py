from com.nttdata.dgi.util.report import Report
from com.nttdata.dgi.persistence.ipersistor import IPersistor, PersistorTypes


class Persistor (IPersistor):
    report: Report
    persistor_configuration: dict

    def __init__(self, persistor_configuration):
        self.persistor_configuration = persistor_configuration
        return

    def persist(self) -> Report:
        persist_report = Report()
        if self.persistor_configuration.get('type') == PersistorTypes.FILE:
            # copy file from source to target
            return persist_report
        elif self.persistor_configuration.get('type') == PersistorTypes.VIRTUOSO:
            # save to Virtuoso
            return persist_report
        elif self.persistor_configuration.get('type') == PersistorTypes.STARDOG:
            # save to Stardog
            return persist_report
        else:
            # persis report warning with unknown type
            return persist_report
        return persist_report

