import requests
from requests.auth import HTTPDigestAuth
from com.nttdata.dgi.persistence.persistor import Persistor
import com.nttdata.dgi.util.io as io


class VirtuosoPersistor(Persistor):
    persistor_details: dict
    url: str
    user: str
    password: str
    report: dict

    def __init__(self, **persistor_details):
        super(VirtuosoPersistor, self).__init__()
        self.persistor_details = persistor_details
        self.url = self.persistor_details.get("endpoint")
        self.user = self.persistor_details.get("user")
        self.password = self.persistor_details.get("password")
        self.report = {"message": [],
                       "warning": [],
                       "error": []}

    def __load(self, lemmatized_thesaurus: str, thesaurus_graph: str):
        t0 = io.now()
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
                                         f"Done in {str(io.now() - t0)}. " \
                                         f"Response: {result.content} // Response code: {result.status_code}"
                io.log(response_error_message, 'e')
                self.report['error'].append(response_error_message)
            else:
                response_correct_message = f"Response from Virtuoso is ok. Done in {str(io.now() - t0)}. " \
                                           f"Status code: {result.status_code}"
                self.report['message'].append(response_correct_message)
        except Exception as ex:
            error_message = f"Exception in method __load from VirtuosoPersistor. Done in {str(io.now() - t0)}. " \
                            f"Exception: {ex}"
            self.report['error'].append(error_message)
            raise Exception(error_message)

        return super()

    def persist(self, *args, **kwargs):
        lemmatized_thesaurus = args[0]
        thesaurus_graph = args[1]
        self.__load(lemmatized_thesaurus, thesaurus_graph)
        return self

    def search_vituoso(self):
        return self

