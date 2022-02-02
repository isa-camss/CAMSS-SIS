import com.nttdata.dgi.util.io as io


class GraphNameError(ValueError):
    pass


class StarDog:

    db: str
    con: s.Connection
    connection_details: dict = {}

    def __init__(self, **connection_details):
        self.connection_details = connection_details
        self.con = None

    def connect(self):
        db = self.connection_details['database']
        conn = self.connection_details['connection']
        with s.Admin(**conn) as admin:
            if db not in [d.name for d in admin.databases()]:
                io.log(f'DataBase {db} not found!')
            self.con = s.Connection(db, **conn)
        return self.con
    
    def load(self, file: str, graph_name: str = None, drop: bool = False):
        """"
        :param file: the file path and name with the triples to load
        :param graph_name: the name of the graph where to place the triples in the remote store. Although
        optional, if the name of the graph is not provided, and drop == True, the loading will fail, since
        the name of the graph is not extracted from the file.
        :param drop: If True, the graph will be rewritten and the old triples cleared, otherwise the
        triples in the file being loaded will be added to the graph.
        """
        if drop and not graph_name:
            name, ext = io.get_file(file)
            io.log(f'Failed: The file {name + ext} WAS NOT loaded onto the graph store. '
                   f'Reason: no graph name was provided.', level='e')
            raise GraphNameError(f"The file '{name + ext}' WAS NOT loaded onto the graph store. "
                                 "Reason: no graph name was provided.")
        elif drop and graph_name:
            self.drop_graph(graph_name)
        else:
            # The triples will be added to the named graph in the remote store
            pass

        conn = self.connect() if not self.con else self.con
        with conn:
            conn.begin()
            conn.add(s.content.File(file), graph_uri=graph_name)
            conn.commit()
        conn.close()
        return self

    def drop_graph(self, graph_name: str):
        """
        Removes a named graph from the remote graph store
        :param graph_name: the name of the graph to remove
        """
        conn = self.connect() if not self.con else self.con
        query = f'''DROP GRAPH <{graph_name}>'''
        try:
            conn.update(query)
        except s.exceptions.StardogException as e:
            if '[500] QEQOE2' in e.__str__():
                # The graph mentioned does not exist, which is good news, nothing to drop -> nothing to remove
                pass
            else:
                raise Exception(e)
        return self

    def insert(self, query: str):
        """
        Inserts the content of the query.
        """
        conn = self.connect() if not self.con else self.con
        with conn:
            conn.begin()
            conn.update(query)
            conn.commit()
        return self

