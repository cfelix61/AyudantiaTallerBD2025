from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "12345678"))
driver.verify_connectivity()

cypher = """
MATCH (p:FPlayer)-[r:PLAYS_FOR {year: 2025}]->(c:Club {name: $club})
RETURN p.name AS player
ORDER BY p.name
"""

club = "Colo-Colo"

records, summary, keys = driver.execute_query(cypher, club=club)

print(f"Jugadores que jugaron en {club} en 2025:")
for record in records:
    print(f"- {record['player']}")

driver.close()
