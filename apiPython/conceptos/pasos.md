# Pasos para operar con API de python en neo4j

### Instalar Driver
comando:
- pip install neo4j
- pip install pandas

### Crear instancia para el driver en python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
  "neo4j://localhost:7687",       # String de conexion para mi database
  auth=("neo4j", "your-password") # el de mi cuenta de neo4j creada en el directorio local
)
#### Puertos (Se pueden obtener desde el archivo setting de la bd)
2025-04-29 03:03:34.806+0000 INFO  Bolt enabled on localhost:7687. PUERTO AL QUE NOS CONECTAREMOS.
2025-04-29 03:03:34.808+0000 INFO  Bolt (Routing) enabled on localhost:7688.
2025-04-29 03:03:35.825+0000 INFO  HTTP enabled on localhost:7474

### Comprobar conexión:
driver.verify_connectivity() --arroja una exception() si no se conecta a la bd

### Consulta usando solo un bloque de code para probar conexión
with GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)) as driver:
    result, summary, keys = driver.execute_query("RETURN COUNT {()} AS count")



  