#######################################################
# 
# persistor_type.py
# Python implementation of the Enumeration PersistorType
# Created on:      18-feb-2022 21:05:20
# Original author: SEMBU Team-NTTData
# 
#######################################################
from enum import IntEnum


class PersistorType (IntEnum):
    NONE = 0
    FILE = 1
    VIRTUOSO = 2
    GRAPHDB = 3
    STARDOG = 4
    ELASTIC = 5
