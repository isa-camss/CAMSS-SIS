#######################################################
# 
# PersistenceFactory.py
# Python implementation of the Class PersistenceFactory
# Generated by Enterprise Architect
# Created on:      18-feb-2022 21:05:20
# Original author: SEMBU Team - NTTData - Barcelona
# 
#######################################################

from com.nttdata.sembu.crud.PersistorType import PersistorType
from com.nttdata.sembu.crud.Persistor import Persistor
from com.nttdata.sembu.crud.FilePersistor import FilePersistor
from com.nttdata.sembu.crud.ElasticPersistor import ElasticPersistor


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

    def new(self, persistor_details: dict, persistor_type: PersistorType = None) -> Persistor:

        _type = self.__get_persistor_type(persistor_details, persistor_type)
        p = None

        if _type is PersistorType.FILE:
            p = FilePersistor(**persistor_details)
        elif _type is PersistorType.ELASTIC:
            p = ElasticPersistor(**persistor_details)

        p.type = _type
        return p
