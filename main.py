# https://sparqlwrapper.readthedocs.io/en/latest/main.html

from SPARQLWrapper import SPARQLWrapper, JSON


query_descriptions = {
    'Query 01': 'Title',
    'Query 02': 'Title & maker',
    'Query 03': 'Manmade objects',
    'Query 04': 'Manmade objects with title & maker',
    'Query 05': 'Doesn''t work',
    'Query 06': 'Title, description & collection'
}


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


def parse_results(results):
    for r in results:
        print('┌────────────────────────────────────────────────────────────────────────────────────────────────────')
        print_results(r, 'object')
        print_results(r, 'title')
        print_results(r, 'description')
        print_results(r, 'maker')
        print_results(r, 'collection')
        print_results(r, 'id')
        print_results(r, 'identificator')
        print('│')
        print('│')


def print_results(result, field):
    if field in result:
        print('│ ➤', field.title(), ':', result[field]['value'])


def query01():

    sparql = """
        PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
        SELECT ?title FROM <http://stad.gent/ldes/hva> 
        WHERE { 
          ?object cidoc:P102_has_title ?title
        } LIMIT 1000
        """

    run_query(sparql)


def query02():

    sparql = """
        PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
        SELECT ?title  ?maker FROM <http://stad.gent/ldes/dmg> 
        WHERE { 
          ?object cidoc:P102_has_title ?title.
          ?object cidoc:P108i_was_produced_by ?maker.
        } LIMIT 1000
        """

    run_query(sparql)


def query03():
    sparql = """
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

    run_query(sparql)


def query04():
    sparql = """
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

    run_query(sparql)


def query05():
    sparql = """
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

    run_query(sparql)


def query06():

    sparql = """
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

    run_query(sparql)

#
# PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#
# SELECT ?asso FROM <http://stad.gent/ldes/hva>
# WHERE {
#   ?start cidoc:P128_carries ?object.
#   ?object cidoc:P129_is_about ?is.
#   ?is cidoc:P2_has_type ?id.
#   ?id skos:prefLabel ?asso
# } LIMIT 50000



if __name__ == '__main__':

    print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
    print('┃')
    for query in query_descriptions:
        print('┃', query, ': ', query_descriptions[query])
    print('┃')
    print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')

    query_to_run = input('│ Query to run: ')

    match query_to_run:
        case '1':
            query01()
        case '2':
            query02()
        case '3':
            query03()
        case '4':
            query04()
        case '5':
            query05()
        case '6':
            query06()
        case _:
            print('Nothing to do')





