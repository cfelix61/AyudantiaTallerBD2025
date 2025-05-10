from neo4j import GraphDatabase

# SCRIPT UTILIZANDO LA BD DE ACTORES 

driver = GraphDatabase.driver(
  "neo4j://localhost:7687",   # String de conexion para mi database
  auth=("neo4j", "12345678")  # el usuario y la contraseña de la base de datos, suele ser neo4j en la version desktop
)

driver.verify_connectivity() #Arroja una excepcion si no se puede conectar a la base de datos

records, summary, keys = driver.execute_query( # driver.execute_query es un metodo que ejecuta una consulta en la base de datos y devuelve los resultados
    "RETURN COUNT {()} AS count"
)
# keys es una lista de los nombres de las columnas de la consulta

first = records[0] # contiene una lista de filas de la consulta
# first es un diccionario que contiene el resultado de la consulta, en este caso el conteo de nodos


print(first["count"])   # Imprime el conteo de nodos en la base de datos
print("xd")

# SCRIPT UTILIZANDO LA BD DE ACTORES
cypher = """
MATCH (p:Person {name: $name})-[r:ACTED_IN]->(m:Movie)
RETURN m.title AS title, r.role AS role
"""
name = "Tom Hanks"

records, summary, keys = driver.execute_query( 
    cypher,    
    name=name  
)

driver.close() # Cierra la conexion a la base de datos