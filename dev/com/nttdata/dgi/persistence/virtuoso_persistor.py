import requests
from requests.auth import HTTPDigestAuth
from com.nttdata.dgi.persistence.persistor import Persistor
import com.nttdata.dgi.util.io as io


class VirtuosoPersistor(Persistor):

    def __init__(self, persistor_configuration: dict):
        super(VirtuosoPersistor, self).__init__(persistor_configuration)
        self.url = self.persistor_configuration.get("endpoint")
        self.user = self.persistor_configuration.get("user")
        self.password = self.persistor_configuration.get("password")

    def __load(self, lemmatized_thesaurus: str, thesaurus_graph: str):
        file = lemmatized_thesaurus
        self.url += thesaurus_graph
        with open(file, 'r', encoding='utf8') as my_file:
            content_file = my_file.read()
        try:
            result = requests.post(url=self.url,
                                   data=content_file.encode('utf-8'),
                                   auth=HTTPDigestAuth(self.user, self.password))
            if not result.ok:
                response_error_message = f"FAILED: The file {file} could not be loaded onto the Virtuoso repository. " \
                                         f"Response: {result.content} // Response code: {result.status_code}"
                io.log(response_error_message, 'e')
                self.report = {"message": response_error_message}

        except Exception as ex:
            error_message = f"Exception in method __load from VirtuosoPersistor. Exception: {ex}"
            raise Exception(error_message)

        return super()

    def persist(self, *args, **kwargs):
        lemmatized_thesaurus = args[0]
        thesaurus_graph = args[1]
        self.__load(lemmatized_thesaurus, thesaurus_graph)
        return self
