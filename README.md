```
   d888888o.   8 888888888o      .8.          8 888888888o.      ,o888888o.      8 8888         
 .`8888:' `88. 8 8888    `88.   .888.         8 8888    `88.  . 8888     `88.    8 8888         
 8.`8888.   Y8 8 8888     `88  :88888.        8 8888     `88 ,8 8888       `8b   8 8888         
 `8.`8888.     8 8888     ,88 . `88888.       8 8888     ,88 88 8888        `8b  8 8888         
  `8.`8888.    8 8888.   ,88'.8. `88888.      8 8888.   ,88' 88 8888         88  8 8888         
   `8.`8888.   8 888888888P'.8`8. `88888.     8 888888888P'  88 8888     `8. 88  8 8888         
    `8.`8888.  8 8888      .8' `8. `88888.    8 8888`8b      88 8888      `8,8P  8 8888         
8b   `8.`8888. 8 8888     .8'   `8. `88888.   8 8888 `8b.    `8 8888       ;8P   8 8888         
`8b.  ;8.`8888 8 8888    .888888888. `88888.  8 8888   `8b.   ` 8888     ,88'8.  8 8888         
 `Y8888P ,88P' 8 8888   .8'       `8. `88888. 8 8888     `88.    `8888888P'  `8. 8 888888888888 
```


# NOTES


## SPARQL Endpoint interface to Python

https://sparqlwrapper.readthedocs.io/en/latest/main.html

---


## CoGhent API

CoGhent API  
https://datalab.stad.gent/coghent

SPARQL demo  
https://github.com/CoGhent/sparql_party

> Het collectiebeheersysteem (Adlib CMS) van het Design Museum Gent, STAM, Industriemuseum, Huis van Alijn en Archief Gent werd uitgebreid met de Linked Data Event Stream specificatie.
> 
> De adlib2eventstream API stelt Adlib databases bloot als event streams. Een event stream is een verzameling van objecten met versiebeheer (in deze context is versie zoals een eventstream event) en kan op elk moment worden bijgewerkt in hun eigen tempo (trage & snelle data). Op deze manier kunnen consumenten gemakkelijk de laatste wijzigingen ontdekken en gebruiken.
> 
> Bekijk de OpenAPI specificatie voor de adlib2eventstream API. De adlib2eventstream is opgebouwd uit open source componenten:
> 
> * Adlib backend: Eerst wordt een Adlib-database opgehaald en wordt de data gemapt naar Linked Data in JSON-LD formaat waarna het wordt opgeslagen in een database.
> * Eventstream API: Hierna worden de Linked Data Fragmenten ontsloten vanuit deze database volgens de Evenstream specificatie.
> 
> **Voorbeeld query:**
> 
> https://apidg.gent.be/opendata/adlib2eventstream/v1/industriemuseum/objecten?generatedAtTime=2022-06-02T00:00:43.528Z

---


## Comunica

Getting started with querying  
https://comunica.dev/docs/query/getting_started/query_cli/

**Voorbeeld query:**

http://query.linkeddatafragments.org/#datasources=https%3A%2F%2Fstad.gent%2Fsparql&query=PREFIX%20cidoc%3A%20%3Chttp%3A%2F%2Fwww.cidoc-crm.org%2Fcidoc-crm%2F%3E%0APREFIX%20adms%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2Fns%2Fadms%23%3E%0APREFIX%20skos%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0ASELECT%20*%0AWHERE%20%7B%0A%3Fobject%20a%20cidoc%3AE22_Man-Made_Object%20.%0A%20%20%23%23%20http%3A%2F%2Fwww.w3.org%2Fns%2Fadms%23Identifier%0A%20%20%3Fobject%20adms%3Aidentifier%20%3Fid.%20%23%23%20fetch%20skolem%20(blank%20node)%0A%20%20%23%23%20http%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23notation%0A%20%20%3Fid%20skos%3Anotation%20%3Fidentificator%20%23%23%20fetch%20value%0A%7D%0ALIMIT%20100&httpProxy=http%3A%2F%2Fproxy.linkeddatafragments.org%2F

---


## SPARQL Interfaces

**Virtuoso SPARQL Query Editor**  
https://stad.gent/sparql

**Comunica**  
http://query.linkeddatafragments.org/

**SPARQL Query Editor**   
https://dbpedia.org/sparql

---

Classes & Properties Declarations of CIDOC-CRM  
https://cidoc-crm.org/html/cidoc_crm_v7.1.1.html

---

## Problems

```SPARQL
PREFIX cidoc: <http://www.cidoc-crm.org/cidoc-crm/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT *
FROM <http://stad.gent/ldes/dmg>
WHERE {
  ?object cidoc:P102_has_title ?title.
  ?object cidoc:P108i_was_produced_by ?p.
  ?p cidoc:P14_carried_out_by ?m.
  ?m rdfs:label ?maker.
}
```

This line should resolve an ID to a label:  
```?m rdfs:label ?maker.```

However, the query returns no results. Leaving that line out, we get:

```
?object    https://stad.gent/id/mensgemaaktobject/dmg/530003762/2022-04-27T00:00:21.255Z
?title     "Lijster op lijsterbes"@nl
?p         https://stad.gent/id/.well-known/skolem/91590474-4d67-45b3-9e2f-64b38bf44f46
?m         https://stad.gent/id/.well-known/skolem/ad96f96d-46d9-4941-b629-6e5e177b0bf9
```

---