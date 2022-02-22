from com.nttdata.dgi.persistence.persistor import Persistor
import requests
from requests.auth import HTTPDigestAuth


class VirtuosoPersistor(Persistor):

    def __init__(self, persistor_configuration: dict):
        super(VirtuosoPersistor, self).__init__(persistor_configuration)
        self.url = self.persistor_configuration.get("endpoint")
        # self.url += self.persistor_configuration.get("method") + "="
        # self.url += self.persistor_configuration.get("graph")
        self.user = self.persistor_configuration.get("user")
        self.password = self.persistor_configuration.get("password")

    def __load(self, lemmatized_thesaurus: str, thesaurus_graph: str):
        file = lemmatized_thesaurus
        self.url += thesaurus_graph
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

    def persist(self, *args, **kwargs):
        lemmatized_thesaurus = args[0]
        thesaurus_graph = args[1]
        self.__load(lemmatized_thesaurus, thesaurus_graph)
        return self
