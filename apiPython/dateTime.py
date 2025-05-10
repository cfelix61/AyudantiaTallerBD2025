from neo4j.time import DateTime
from datetime import timezone, timedelta
from neo4j import GraphDatabase


driver = GraphDatabase.driver(
  "neo4j://localhost:7687",   # String de conexion para mi database
  auth=("neo4j", "12345678")  # el usuario y la contraseña de la base de datos, suele ser neo4j en la version desktop
)

#Creamos un nodo evento para poder cuando se crean o actualizan los nodos
driver.execute_query("""
CREATE (e:Event {
  startsAt: $datetime,              // (1)
  createdAt: datetime($dtstring),   // (2)
  updatedAt: datetime()             // (3)
})
""",
    datetime=DateTime(
        2024, 5, 15, 14, 30, 0,
        tzinfo=timezone(timedelta(hours=2)) #UTC +2
    ),  
    dtstring="2024-05-15T14:30:00+02:00" #Ambos representan la misma fecha y hora: 15 de mayo de 2024, a las 14:30, hora UTC+2.
)