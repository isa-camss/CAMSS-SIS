from elasticsearch import Elasticsearch
from com.nttdata.dgi.persistence.persistor import Persistor, PersistorArgumentError
from elasticsearch.helpers import scan


class ElasticPersistorException(ValueError):
    pass


class ElasticPersistor(Persistor):
    persistor_details: dict
    elastic: Elasticsearch
    index: str

    def __init__(self, **persistor_details,
                 # elastic_host: str = None,
                 # elastic_query: dict = None,
                 # scroll_resources: str = None,
                 # elastic_index: str = None
                 ):
        super(ElasticPersistor, self).__init__()

        self.persistor_details = persistor_details
        self.__checkers()
        # Defaults to one ES host
        self.elastic = Elasticsearch(self.persistor_details.get("host"))
        return

    def __checkers(self):
        if self.persistor_details is None or self.persistor_details.get('host') is None:
            raise ElasticPersistorException("FAILED: A persistor could not be created because no host URI has "
                                            "been passed to the constructor. Please check the persistor "
                                            "details and documentation.")

        # Elasticsearch requires lowered case for index names
        self.index = self.persistor_details.get('def_index')
        self.index = self.index.lower() if self.index else None
        return

    @staticmethod
    def __exception_no_index():
        raise ElasticPersistorException("FAILED: a document could not dropped because an index name has "
                                        "not been provided, either in the constructor nor via method. "
                                        "Check the documentation.")

    def drop(self, *args, **kwargs):
        """
        Drops and index, a document with id or multiple documents using a query.
        Usage:
        1. The url of the ElasticPersistor host has been provided via the constructor
        2. If no argument -> Exception is raised
        3. If only index in kwargs -> it deleted all the documents in the elastic index
        4. If id in kwargs -> this document id will be drop and the default index is used, if
            it has been provided at construction time, otherwise an Exception is raised
        5. If query in kwargs -> all documents returned by the query will be drop and the default index is used, if
            it has been provided at construction time, otherwise an Exception is raised
        6. If no kwargs and only one argument -> the expected parameter is the document id and the default index is
            used, if it has been provided at construction time, otherwise an Exception is raised
        7. The recommended option is to pass the index, the id or query as named arguments in kwarg

        Usage:
            (3) drop(index="index-name"),
            (4) drop(index="index-name", id="document-id"),
            (5) drop(index="index-name", query="elastic-query"),
            (6) drop(document_id)
        :return: self
        """
        '''
        Checkers
        '''
        if args is None and kwargs is None:
            raise ElasticPersistorException('FAILED: drop needs arguments. Check the documentation.')
        ''''
        Priority is given to kwargs: if kwargs, then args are dismissed;
        '''
        if kwargs and kwargs.get('id') is None and kwargs.get('query') is None and kwargs.get('index') is not None:
            self.elastic.indices.delete(index=kwargs.get('index'))
        elif kwargs and kwargs.get('id') is not None:
            id_ = kwargs.get('id')
            index = kwargs.get('index')
            index = index if index else self.index if self.index else self.__exception_no_index()
            self.elastic.delete(index=index, id=id_)
        elif kwargs and kwargs.get('query') is not None:
            query = kwargs.get('query')
            index = kwargs.get('index')
            index = index if index else self.index if self.index else self.__exception_no_index()
            self.elastic.delete_by_query(index=index, body=query)
        elif args:
            '''
            If no kwargs ... document is expected
            '''
            id_ = args[0]
            self.elastic.delete(index=self.index, id=id_)
        return self

    def persist(self, *args, **kwargs):
        """
        Persists in ElasticPersistor a dictionary passed in the arguments.
        Usage:
        1. The url of the ElasticPersistor host has been provided via the constructor
        2. If no argument -> Exception is raised
        3. If only one argument -> the expected parameter is the document to persist and the default index is used, if
            it has been provided at construction time, otherwise an Exception is raised
        4. The recommended option is to pass the index, the document and the document id as named arguments in kwarg
        5. If no id is provided as an argument and an attribute 'id' is found inside the document, this id is used.

        Usage:
            persist(json_object: dict)     # The default index provided in the constructor is used
            persist(index="index-name", content={..}, id=12123)
        :return: self
        """
        '''
        checkers
        '''
        if not args and not kwargs:
            raise PersistorArgumentError(f"FAILED: a document could not be persisted in ElasticPersistor because no "
                                         "arguments in the method persist() were provided. Check the documentation.")

        p = self.elastic
        ''' 
        If args but no kwargs, args are taken, obviously, otherwise ... 
        '''
        if args and len(args) == 1 and not kwargs:
            if not self.index:
                self.__exception_no_index()
            p.index(index=self.index, document=args[0])
        '''
        ... if args and kwargs, kwargs are prioritized and args dismissed
        '''
        if kwargs:
            '''
            1. Get the Elastic index
            '''
            index = kwargs.get('index')
            index = index if index else self.index
            if not index:
                self.__exception_no_index()
            '''
            2. Treat the content and id;
            '''
            content = kwargs.get('content')    # Get the json object to persist
            id_ = kwargs.get('id')     # Priority to the 'id' inside the document
            id_ = id_ if id_ else content.get('id')   # Otherwise check if an id inside the doc
            '''
            3. persist
            '''
            p.index(index=index, document=content, id=id_)

        return self

    def ask(self, *args, **kwargs) -> bool:
        """
        Asks if a field key with a field value exists in Elasticsearch.
        Usage:

        1. The url of the ElasticPersistor host has been provided via the constructor
        2. If no argument -> Exception is raised
        3. If only two argument -> the expected parameters are field key and the field value and the default index is
            used, if it has been provided at construction time, otherwise an Exception is raised
        4. The recommended option is to pass the index, the field key and the field value as named arguments in kwarg

        Usage:
            ask(field_key: str, field_value: str)     # The default index provided in the constructor is used
            ask(index="index-name", field_key="field_key_elastic", field_value="field_value_elastic")
        Example:
            ask("rsc_id", "12123")
            ask(index="camss*", field_key="rsc_id", field_value="12123")
        :return: bool
        """

        if not args and not kwargs:
            raise PersistorArgumentError(f"FAILED: a document could not be persisted in ElasticPersistor because no "
                                         "arguments in the method persist() were provided. Check the documentation.")

        p = self.elastic
        ask_exists = False
        ''' 
        If args but no kwargs, args are taken, obviously, otherwise ... 
        '''
        if args and len(args) == 2 and not kwargs:
            if not self.index:
                self.__exception_no_index()

            query = {
                "query": {
                    "term": {f"{args[0]}": f"{args[1]}"}
                }
            }
            num_occurrences = p.count(index=self.index, body=query).get('count')
            if num_occurrences > 0:
                ask_exists = True
            else:
                ask_exists = False
        '''
        ... if args and kwargs, kwargs are prioritized and args dismissed
        '''
        if kwargs:
            '''
            1. Get the Elastic index
            '''
            index = kwargs.get('index')
            index = index if index else self.index
            if not index:
                self.__exception_no_index()
            '''
            2. Prepare the ask query
            '''
            field_key = kwargs.get('field_key')
            field_value = kwargs.get('field_value')

            query = {
                "query": {
                    "term": {f"{field_key}": f"{field_value}"}
                }
            }
            '''
            3. Execute ask query
            '''
            num_occurrences = p.count(index=index, body=query).get('count')
            '''
            4. Check if occurrences are higher then 0
            '''
            if num_occurrences > 0:
                ask_exists = True
            else:
                ask_exists = False
        return ask_exists
    '''
    def search(self):
        # TODO: Modify this method when used
        # Query to Elasticsearch
        scan(client=Elasticsearch(self.client),
             query=self.query,
             scroll=self.scroll,
             index=self.index,
             raise_on_error=self.raise_on_error,
             preserve_order=self.preserve_order,
             clear_scroll=self.clear_scroll)
        return self
    '''
