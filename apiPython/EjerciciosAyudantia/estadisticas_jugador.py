from neo4j import GraphDatabase
from neo4j import RoutingControl
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "12345678"))
driver.verify_connectivity()

cypher = """
MATCH (p:FPlayer {name: $name})
RETURN 
  p.goals AS goals, 
  p.assists AS assists, 
  p.yellowCards AS yellowCards, 
  p.redCards AS redCards
"""

name = "Jugador1"

records, summary, keys = driver.execute_query(cypher, name=name, routing_=RoutingControl.READ )

if records:
    stats = records[0]
    print(f"Estadísticas de {name}:")
    print(f"Goles: {stats['goals']}")
    print(f"Asistencias: {stats['assists']}")
    print(f"Tarjetas amarillas: {stats['yellowCards']}")
    print(f"Tarjetas rojas: {stats['redCards']}")
else:
    print(f"No se encontraron datos para {name}")

driver.close()
