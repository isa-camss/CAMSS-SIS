EURLEX_EXPERT_QUERY = '![CDATA[DTS_SUBDOM = "TREATIES" OR "INTER_AGREE" OR "LEGISLATION" OR "EFTA" OR "EU_LAW_ALL" ' \
                      'AND PD >= 01/01/2012 <= 07/02/2022]]'

EIRA_LEGAL_ABBS_QUERY = '''
    select distinct ?Lema
    from <http://data.europa.eu/dr8/eira_lemmas/>
    where {
        ?s ?p skos:Collection.
        ?s skos:member ?o.
        ?o skos:prefLabel ?Lema
        FILTER (contains(STR(?s), "http://data.europa.eu/dr8/view/LegalView"))
    }'''

EIRA_ORGANISATIONAL_ABBS_QUERY = '''
    select distinct ?Lema
    from <http://data.europa.eu/dr8/eira_lemmas/>
    where {
        ?s ?p skos:Collection.
        ?s skos:member ?o.
        ?o skos:prefLabel ?Lema
        FILTER (contains(STR(?s), "http://data.europa.eu/dr8/view/OrganisationalView"))
    }'''
