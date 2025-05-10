from neo4j import GraphDatabase
#Result se puede usar para crear dataFrames
from neo4j import Result
from neo4j import RoutingControl #para establecer que solo leere, por defecto esta en modo write, asi hace todo mas rapido
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

#print(repr(first)) 
print(first["count"])   # Imprime el conteo de nodos en la base de datos
print("xd")

# SCRIPT UTILIZANDO LA BD DE ACTORES
cypher = """
MATCH (p:Person {name: $name})-[r:ACTED_IN]->(m:Movie)
RETURN m.title AS title, r.roles AS role
"""
name = "Tom Hanks"

records, summary, keys = driver.execute_query( 
    cypher,    
    name=name  
)
print(keys)  # ['title', 'role']
print(summary)  
for record in records:
    print(record["title"])
    print(record.get("role", "Sin rol"))  # Devuelve "Sin rol" si no existe el campo "role" en el diccionario
    

#records: una lista con los resultados (cada uno es un diccionario).

#summary: un resumen del resultado (información sobre cómo se ejecutó la consulta).

#keys: una lista con los nombres de las columnas devueltas (en este caso, ['title', 'role']).

print("formateo de la salida")
result = driver.execute_query(
    cypher,
    name=name,
    result_transformer_= lambda result: [
        f"Tom Hanks actuó como {record['role']} en {record['title']}"
        for record in result
    ]
)

print(result)  



driver.execute_query(
    cypher,
    result_transformer_=Result.to_df, #creo un dataframe con los resultados, permitiendome trabajar con pandas
    routing_=RoutingControl.READ  # or simply "r" #optimiso para que solo haga lectura y distribuya la carga en los clusters.
)

driver.close() # Cierra la conexion a la base de datos