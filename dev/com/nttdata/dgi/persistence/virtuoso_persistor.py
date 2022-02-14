from com.nttdata.dgi.persistence.persistor import Persistor
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class VirtuosoPersistor(Persistor):

    def __init__(self, persistor_configuration: dict):
        super(VirtuosoPersistor, self).__init__(persistor_configuration)
        self.url = self.persistor_configuration.get("endpoint")
        # self.url += self.persistor_configuration.get("method") + "="
        # self.url += self.persistor_configuration.get("graph")
        self.user = self.persistor_configuration.get("user")
        self.password = self.persistor_configuration.get("password")

    def __load(self):

        # file = self.persistor_configuration.get("source")
        file = "C:/SEMBUdev/Github/CAMSS/CAMSS-SIS/dev/arti/rdf/eira_thesaurus.rdf"
        with open(file, 'r', encoding='utf8') as myfile:
            content_file = myfile.read()
        try:
            result = requests.post(url=self.url, data=content_file.encode('utf-8'),
                                  auth=HTTPDigestAuth(self.user, self.password))
            if not result.ok:
                self.report = {"message": f"FAILED: The file {file} could not be loaded onto the Virtuoso repository."
                                          f" Response: {result.content}"}
        except Exception as x:
            print(x)

        return super()

    def persist(self):
        self.__load()
