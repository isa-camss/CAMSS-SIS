import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
from flask_restx import Resource, fields, Namespace
from flask import request
from com.nttdata.dgi.rdf.skos_lemmatizer import SKOSLemmatizer

api = Namespace(ctt.RDF_SKOS_NAME,
                description='Maps labels from one '
                            'or more SKOS or SKOS-XL thesauri to the result returned by an endpoint '
                            'given as an argument.')

t1l = api.model("GSF lemmas", {"source": fields.String(default=ctt.EIRA_THESAURUS_LEMMA_DETAILS.get('source')),
                               "target": fields.String(default=ctt.EIRA_THESAURUS_LEMMA_DETAILS.get('target')),
                               "function": fields.String(default=ctt.EIRA_THESAURUS_LEMMA_DETAILS.get('function'))})

t1md5 = api.model("GSF md5 lemmas", {"source": fields.String(default=ctt.EIRA_THESAURUS_MD5_DETAILS.get('source')),
                                     "target": fields.String(default=ctt.EIRA_THESAURUS_MD5_DETAILS.get('target')),
                                     "function": fields.String(default=ctt.EIRA_THESAURUS_MD5_DETAILS.get('function'))})

model = api.model("SKOS Lemmatizer",
                  {'endpoint': fields.String(default=ctt.LEMMATIZER_ENDPOINT),
                   'labels': fields.List(fields.String(), default=ctt.LABELS),
                   'thesauri': fields.List(fields.Nested(t1l))})


@api.route(f'/{ctt.SKOS_LEMMATIZER_ENDPOINT}')
@api.expect(model)
class SKOSMirror(Resource):
    @api.doc(
        """"
        Given an endpoint and a list of thesauri, returns a mirror of each thesaurus where the SKOS label has been 
        replaced with the value returned by the endpoint (e.g., the lemma of the label, the md5 of the lemma, other)."
        """)
    def post(self):
        """
        Given an endpoint and a list of thesauri, returns a mirror of each thesaurus where the SKOS label has been
        replaced with the value returned by the endpoint (e.g., the lemma of the label, the md5 of the lemma, other).
        \nI. PRE-CONDITIONS: Make sure that...\n
        1. The file cfg/ctt.py exists and contains proper configuration settings (e.g., the graph store details are
        supplied)
        2. The endpoint you enter as an argument exists and it is up and running
        3. If you want to store the graphs, make sure that the store specified in the cfg/ctt file is up and running
        \nII. ARGUMENTS:\n
        1. 'endpoint': the endpoint of the method returning the value that replaces the original SKOS or SKOS-XL label
        2. 'thesauri': a list of dictionaries containing the details of the thesauri to map:
            2.1. 'source' (REQUIRED): the file path and name containing the SKOS/SKOS-XL original labels
            2.2. 'target' (REQUIRED): the file path and name to create where the original labels have been replaced with
             the values returned by the endpoint
            2.3. 'graph' (OPTIONAL): the name for the Named Graph that will be stored in the graph store
            2.4. 'function' (OPTIONAL): the name of a default function inside the endpoint, e.g. lemma or md5lemma if
            the endpoint is /nlp/lemmatize
        \nIII. EXAMPLE: The following call ...
            - would parse two taxonomies and produce four mappings with the lemmatized labels and the md5 of the
            lemmatized labels, and
            - would create four named graphs in the graph store\n
        {
            "endpoint": "http://localhost:5000/nlp/lemmatize",
            "labels": ['<title', '<preflabel', '<altlabel', '<hiddenlabel', '<literal', '<literalform',
                        '<skos:preflabel', '<skos:altlabel', '<skos:hiddenlabel']
            "thesauri": [
                {
                "source": "./arti/kg/pp_project_gsfthesaurus.concepts.rdf",
                "target": "./arti/kg/pp_project_gsfthesaurus.md5lemmas.rdf",
                "graph": "http://thesaurus.iadb.org/rsc/gsf-thesaurus/md5lemmas/",
                "function": "md5lemma"
                },
                {
                "source": "./arti/kg/pp_project_gsfthesaurus.concepts.rdf",
                "target": "./arti/kg/pp_project_gsfthesaurus.md5lemmas.rdf",
                "graph": "http://thesaurus.iadb.org/rsc/gsf-thesaurus/lemmas/",
                "function": "lemma"
                },
                {
                "source": "./arti/kg/EuroSciVoc-skos-ap-eu.rdf",
                "target": "./arti/kg/EuroSciVoc-skos-ap-eu.rdf.md5lemmas.rdf",
                "graph": "http://thesaurus.iadb.org/rsc/EuroSciVoc-skos-ap-eu.rdf/md5lemmas/",
                "function": "md5lemma"
                },
                {
                "source": "./arti/kg/EuroSciVoc-skos-ap-eu.rdf",
                "target": "./arti/kg/EuroSciVoc-skos-ap-eu.rdf.lemmas.rdf",
                "graph": "http://thesaurus.iadb.org/rsc/EuroSciVoc-skos-ap-eu.rdf/lemmas/",
                "function": "lemma"
                }
            ]
        }
        """
        t0 = io.log(f'Mapping started...(now: {io.now()})')
        code = 200
        args = request.json
        print(args)
        endpoint = args.get('endpoint')
        labels = args.get('labels')
        if not endpoint:
            m = f"FAILED -> Endpoint not supplied. Please check the documentation."
            io.log(m, 'e')
            return {'message': m}, 404

        td = args.get('thesauri')
        if not td:
            m = f"FAILED -> Thesauri details not supplied. Please check the documentation."
            io.log(m, 'e')
            return {'message': m}, 404
        try:
            sm = SKOSLemmatizer(lemmatization_details=ctt.LEMMATIZATION_DETAILS, labels=labels)
            sm.mirror(thesauri=td)

            '''
            # Thesauri_processor is responsible to invoke a persistor specialized in loading files into a concrete tripestore
            sm.store(thesauri=td, store_details=ctt.STORE_DETAILS) 
            '''

            io.log(f'Process finished. It took {io.now() - t0} (now: {io.now()}')
            ret = sm.report
        except Exception as ex:
            ret = {'message': 'FAILED -> ' + ex.__str__()}
            code = 404
        ret['lapse'] = str(io.now()-t0)
        ret['now'] = str(io.now())
        return ret, code
