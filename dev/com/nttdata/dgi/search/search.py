from elasticsearch.helpers import scan
from elasticsearch import Elasticsearch


class Search:
    client: str
    query: dict
    scroll: str
    index = str
    raise_on_error = True
    preserve_order = False
    clear_scroll = True

    def __init__(self, elastic_host: str = None,
                 elastic_query: dict = None,
                 scroll_resources: str = None,
                 elastic_index: str = None):
        super().__init__()

        self.client = elastic_host
        self.query = elastic_query
        self.scroll: scroll_resources
        self.index = elastic_index
        self.raise_on_error = True
        self.preserve_order = False
        self.clear_scroll = True
        return

    def ask_elastic(self):
        # Query to Elasticsearch
        scan(client=Elasticsearch(self.client),
             query=self.query,
             scroll=self.scroll,
             index=self.index,
             raise_on_error=self.raise_on_error,
             preserve_order=self.preserve_order,
             clear_scroll=self.clear_scroll)
        return self
