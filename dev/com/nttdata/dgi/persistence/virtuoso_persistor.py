from com.nttdata.dgi.persistence.persistor import Persistor
import requests
from requests.auth import HTTPBasicAuth


class VirtuosoPersistor(Persistor):

    def __init__(self, persistor_configuration: dict):
        super(VirtuosoPersistor, self).__init__(persistor_configuration)
        self.url = self.persistor_configuration.get("endpoint")
        self.url += self.persistor_configuration.get("method") + "="
        self.url += self.persistor_configuration.get("graph")
        self.user = self.persistor_configuration.get("user")
        self.password = self.persistor_configuration.get("password")

    def __load(self):

        file = self.persistor_configuration.get("source")
        with open(file, 'r') as myfile:
            content_file = myfile.read()
        result = requests.put(url=self.url, data=content_file, auth=HTTPBasicAuth(self.user, self.password))
        if not result.ok:
            self.report = {"message": f"FAILED: The file {file} could not be loaded onto the Virtuoso repository."
                                      f" Response: {result.content}"}

        return super()

    def persist(self):
        self.__load()
