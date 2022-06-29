# https://sparqlwrapper.readthedocs.io/en/latest/main.html

from SPARQLWrapper import SPARQLWrapper, JSON


query_description = {}

##################################################################################################
query_description['sparql01'] = "Title"
sparql01 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    SELECT ?title FROM <http://stad.gent/ldes/hva> 
    WHERE { 
      ?object cidoc:P102_has_title ?title
    } LIMIT 1000
"""

##################################################################################################
query_description['sparql02'] = "Title & maker"
sparql02 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    SELECT ?title  ?maker FROM <http://stad.gent/ldes/dmg> 
    WHERE { 
      ?object cidoc:P102_has_title ?title.
      ?object cidoc:P108i_was_produced_by ?maker.
    } LIMIT 1000
    """

##################################################################################################
query_description['sparql02'] = "Manmade objects"
sparql03 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX adms: <http://www.w3.org/ns/adms#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT *
    WHERE {
    ?object a cidoc:E22_Man-Made_Object .
      ## http://www.w3.org/ns/adms#Identifier
      ?object adms:identifier ?id. ## fetch skolem (blank node)
      ## http://www.w3.org/2004/02/skos/core#notation
      ?id skos:notation ?identificator ## fetch value
    }
    LIMIT 1000
"""

##################################################################################################
query_description['sparql04'] = "Manmade objects with title & maker"
sparql04 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX adms: <http://www.w3.org/ns/adms#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    SELECT *
    WHERE {
      ?object a cidoc:E22_Man-Made_Object.
      ?object cidoc:P102_has_title ?title.
      ?object cidoc:P108i_was_produced_by ?maker.
      ## http://www.w3.org/ns/adms#Identifier
      ?object adms:identifier ?id. ## fetch skolem (blank node)
      ## http://www.w3.org/2004/02/skos/core#notation
      ?id skos:notation ?identificator ## fetch value
    }
    LIMIT 1000
"""

##################################################################################################
query_description['sparql05'] = "Association"
sparql05 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?association FROM <http://stad.gent/ldes/hva>
    WHERE {
      ?start cidoc:P128_carries ?object.
      ?object cidoc:P129_is_about ?is.
      ?is cidoc:P2_has_type ?id.
      ?id skos:prefLabel ?association
    } LIMIT 10000
"""

##################################################################################################
query_description['sparql06'] = "Title, description & collection"
sparql06 = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX aat: <http://vocab.getty.edu/aat/>
    PREFIX dcterms: <http://purl.org/dc/terms/>

    SELECT DISTINCT ?title ?description ?collection
    WHERE { 
      ?object cidoc:P102_has_title ?title
      FILTER (lang(?title) = "nl")
      ?object cidoc:P46i_forms_part_of ?coll.
      ?coll cidoc:P2_has_type ?typeCollectie.
      ?typeCollectie skos:prefLabel ?collection
      FILTER (lang(?collection) = "nl")
      ?object cidoc:P3_has_note ?description
      FILTER (lang(?description) = "nl")
    } 
    """

##################################################################################################
query_description['sparql07'] = "Dates"
sparql07 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

    SELECT ?title ?date FROM <http://stad.gent/ldes/hva>
    WHERE { 
      ?start cidoc:P102_has_title ?title.
      ?start cidoc:P108i_was_produced_by ?maker.
      ?maker cidoc:P4_has_time-span ?date.
    } LIMIT 50000
    """

##################################################################################################
query_description['sparql08'] = "Object type and title"
sparql08 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    
    SELECT ?title ?tag FROM <http://stad.gent/ldes/hva>
    WHERE { 
      ?start cidoc:P102_has_title ?title.
      ?start cidoc:P41i_was_classified_by ?object.
      ?object cidoc:P42_assigned ?is.
      ?is skos:prefLabel ?tag.
    } LIMIT 50000
    """

##################################################################################################
query_description['sparql09'] = "Object manufacturer"
sparql09 = """
    PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX la: <https://linked.art/ns/terms/>
    
    SELECT ?title ?manufacturer FROM <http://stad.gent/ldes/hva>
    WHERE { 
      ?start cidoc:P102_has_title ?title.
      ?start cidoc:P108i_was_produced_by ?m.
      ?m cidoc:P14_carried_out_by ?vervaardiger.
      ?vervaardiger la:equivalent ?v.
      ?v rdfs:label ?manufacturer
    } LIMIT 50000
    """


def run_query(sparql_query):
    sparql = SPARQLWrapper(
        "https://stad.gent/sparql"
    )
    sparql.setReturnFormat(JSON)
    sparql.setQuery(sparql_query)

    try:
        ret = sparql.queryAndConvert()
        parse_results(ret["results"]["bindings"])
    except Exception as e:
        print(e)


# Known interesting fields are listed here
def parse_results(results):
    for r in results:
        print('┌────────────────────────────────────────────────────────────────────────────────────────────────────')
        print_results(r, 'object')
        print_results(r, 'title')
        print_results(r, 'description')
        print_results(r, 'maker')
        print_results(r, 'manufacturer')
        print_results(r, 'date')
        print_results(r, 'collection')
        print_results(r, 'id')
        print_results(r, 'identificator')
        print_results(r, 'association')
        print_results(r, 'tag')
        print('│')
        print('│')
    print('\n\nRESULTS: ', len(results))


def print_results(result, field):
    if field in result:
        print('│ ➤', field.title(), ':', result[field]['value'])


if __name__ == '__main__':

    print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃')
    for query in query_description:
        print('┃', query, ': ', query_description[query])
    print('┃')
    print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

    query_to_run = input('│ Query to run: ')
    query_to_run = eval('sparql' + str(int(query_to_run)).zfill(2))
    run_query(query_to_run)
