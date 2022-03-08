from com.nttdata.dgi.persistence.virtuoso_persistor import VirtuosoPersistor
from com.nttdata.dgi.persistence.persistor_type import PersistorType
from com.nttdata.dgi.persistence.ipersistor import IPersistor
# from com.nttdata.dgi.crud.FilePersistor import FilePersistor
from com.nttdata.dgi.persistence.elastic_persistor import ElasticPersistor


class PersistenceFactory:

    def __init__(self):
        pass

    @staticmethod
    def __get_persistor_type(persistor_details: dict, persistor_type: PersistorType) -> PersistorType:
        """
        Prioritizes from where to take the persistor type.
        Maximum priority is given to the type passed as an argument to new()
        """
        try:
            return persistor_type if persistor_type else eval('PersistorType.' + persistor_details.get('store'))
        except ValueError:
            raise ValueError("FAILED: A wrong value was passed as a Persistor Type. Check the documentation.")

    def new(self, persistor_details: dict, persistor_type: PersistorType = None) -> IPersistor:

        _type = self.__get_persistor_type(persistor_details, persistor_type)
        p: IPersistor = None

        if _type is PersistorType.FILE:
            pass
            # p = FilePersistor(**persistor_details)
        elif _type is PersistorType.ELASTIC:
            p = ElasticPersistor(**persistor_details)
        elif _type is PersistorType.VIRTUOSO:
            p = VirtuosoPersistor(**persistor_details)
        p.type = _type
        return p

    # def new(persistor_type: PersistorType, **persistor_configuration) -> IPersistor:
        # persistor: IPersistor = None
        # if PersistorType.VIRTUOSO is persistor_type:
            # persistor: VirtuosoPersistor = VirtuosoPersistor(persistor_configuration)
        # return persistor
