"""
Interface for all Resource Keyword Workers
"""


class KeywordWorkerInterface:

    def __init__(self):
        pass

    def extract(self, phrase: str, rsc_part: str):
        return self
