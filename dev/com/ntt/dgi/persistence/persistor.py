from com.ntt.dgi.util.report import Report


class Persistor:
    report: Report
    persistor_configuration: dict

    def __init__(self, persistor_configuration):
        self.persistor_configuration = persistor_configuration
        return

    def persist(self) -> Report:
        persist_report = Report()
        return persist_report
