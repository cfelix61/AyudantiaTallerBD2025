
from neo4j import GraphDatabase
from neo4j import Result
from neo4j import RoutingControl 

driver = GraphDatabase.driver(
  "neo4j://localhost:7687",   # String de conexion para mi database
  auth=("neo4j", "12345678")  # el usuario y la contraseña de la base de datos, suele ser neo4j en la version desktop
)

cypher = """
MATCH path = (person:Person)-[actedIn:ACTED_IN]->(movie:Movie {title: $title})
RETURN path, person, actedIn, movie
"""
title = "Apollo 13"

records, summary, keys = driver.execute_query(
    cypher,
    title=title,
    routing_=RoutingControl.READ 
)
driver.verify_connectivity()
if records:
    print("Se encontraron resultados.")
    for record in records:
        node = record["movie"]
        node2 = record["person"] 
        relacion = record["actedIn"] #relacion entre el actor y la pelicula
    #caminos 
    print("relaciones")
    path = record["path"]
    print(path.start_node)  # Nodo de inicio del camino
    print(path.end_node)    # Nodo de fin del camino
    print(path.relationships)  # Relaciones en el camino
    print(relacion.type)  # Tipo de relación en el camino
    print(len(path))      # Longitud del camino
    print(path.nodes)        # Nodos en el camino

    print("Nodo de la pelicula")
    print(node.element_id)      
    print(node.labels)          
    print(node.items())         
    print(node.get("title", "N/A"))

    print("Nodo del actor")
    print(node2.element_id)
    print(node2.labels)
    print(node2.items()) #con esta manera obtenemos una tupla de tuplas
    print(node2.get("name", "N/A")) # con .get podemos obtener el valor de un atributo en especifico, en este caso el nombre del actor
    driver.close()
else:
    print("No se encontraron resultados.")
    driver.close()