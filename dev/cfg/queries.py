EURLEX_EXPERT_QUERY = '![CDATA[DTS_SUBDOM = "TREATIES" OR "INTER_AGREE" OR "LEGISLATION" OR "EFTA" OR "EU_LAW_ALL" ' \
                      'AND PD >= 01/01/2012 <= 07/02/2022]]'

ELASTIC_QUERY = {
    "query": {
        "bool": {
            "must": [
                {"match": {"terms.lemma": "s%"}}
            ]
        }
    }
}

