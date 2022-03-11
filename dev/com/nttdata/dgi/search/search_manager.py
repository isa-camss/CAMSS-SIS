import os
import com.nttdata.dgi.util.io as io


class SearchManager:
    search_details: dict

    def __init__(self, search_elastic_details: dict = None):
        self.search_details = search_elastic_details
        return

    def prepare_search_files(self, search_elastic_details: dict):
        self.search_details = search_elastic_details

        io.drop_file(self.search_details.get('match_terms_file'))
        with open(self.search_details.get('match_terms_file'), 'w+') as outfile:
            outfile.close()
        return self

    def lemmatize_terms(self, search_elastic_details: dict):
        io.log(f"---- Starting with lemmatization of terms ----")
        self.search_details = search_elastic_details

        for term in self.search_details.get('eira_concepts'):

            terms_match = {'term': term,
                           'resources_matches': []
                           }
        return self



