EURLEX_EXPERT_QUERY = '![CDATA[DTS_SUBDOM = "TREATIES" OR "INTER_AGREE" OR "LEGISLATION" OR "EFTA" OR "EU_LAW_ALL" ' \
                      'AND PD >= 01/01/2012 <= 07/02/2022]]'

EIRA_ABBS_QUERY = '''
    select distinct ?Lemma
    from <http://data.europa.eu/dr8/eira_lemmas/>
    where {
        ?s ?p skos:Collection.
        ?s skos:member ?o.
        ?o skos:prefLabel ?Lemma
        FILTER (contains(STR(?s), "http://data.europa.eu/dr8/view/%s"))
    }'''

KIBANA_EIRA_TERMS = {
    "query": {
        "bool": {
            "should": [
                {
                    "match_phrase": {
                        "lemma.keyword": "bind instrument"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperable digital public service implementation orientation"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "legal act"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "international treaty"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "legal agreement"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "legal authority"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "legal interoperability agreement"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "legislation catalogue"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "legislation datum information knowledge exchange"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "non-binding instrument"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public policy"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public policy cycle"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "share legal framework"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "business"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "business capability"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "business information"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "citizen"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "digital business capability"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "exchange business information"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperability framework"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperability governance"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperability organisational authority"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperability skill"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperability strategy"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "interoperable digital public service"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "organisation"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "organisational agreement"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "organisational interoperability agreement"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "privacy framework"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public administration"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public service agent"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public service catalogue"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public service consumer"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public service consumer agent"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public service delivery agent"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "public service provider"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "security framework"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "service delivery model"
                    }
                },
                {
                    "match_phrase": {
                        "lemma.keyword": "share governance framework"
                    }
                }
            ],
            "minimum_should_match": 1
        }
    }
}
