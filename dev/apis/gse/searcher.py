import cfg.ctt as ctt
import com.nttdata.dgi.util.io as io
from flask_restx import Resource, Namespace
from com.nttdata.dgi.search.search_manager import SearchManager

api = Namespace(ctt.SEARCH_NAME,
                description='Search concepts in the Corpora to find candidate Specifications.')


def search_terms():
    report = {"message": [],
              "warning": [],
              "error": []}

    t0 = io.log("Search process started")

    # 0. Initialize the needed variables for this process
    # Search variables
    search_details = ctt.SEARCH_DETAILS

    # 1. Create Searcher
    search_manager = SearchManager()

    # 2. Prepare all folders/files
    search_manager.prepare_search_files(search_details)
    report['message'].append(f"Search files preparation finished in {str(io.now() - t0)}")
    t1 = io.log(f"search configuration done in {str(io.now() - t0)}")

    return report


# ping_args = api.parser()
@api.route('/search')
class SearchSpecifications(Resource):
    @api.doc("Search concepts in the Corpus to find candidate Specifications")
    # @api.expect(ping_args, validate=True)
    def post(self):
        try:
            t0 = io.now()
            report = search_terms()
            return {'message': f'Done in: {str(io.now() - t0)}'}, 200
        except Exception as ex:
            io.log(f"Exception: {ex}")
            return {'message': f'Exception: {ex}'}, 555
