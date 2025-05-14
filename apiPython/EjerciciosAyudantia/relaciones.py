from neo4j import GraphDatabase
import pandas as pd

# Conexión a Neo4j
URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
driver.verify_connectivity()

def run_query(cypher_query: str, parameters: dict = {}) -> pd.DataFrame:
    with driver.session() as session:
        result = session.run(cypher_query, parameters)
        data = [record.data() for record in result]
        return pd.DataFrame(data)

# Solo crear relaciones si aún no existen
query_crear_relaciones_si_no_existe = """
MATCH (p:FPlayer), (c:Club)
WHERE p.team = c.name AND NOT (p)-[:PLAYS_FOR]->(c)
CREATE (p)-[r:PLAYS_FOR {year: p.year}]->(c)
RETURN p.name AS jugador, type(r) AS relacion, r.year AS año, c.name AS club
"""

df_relaciones_nuevas = run_query(query_crear_relaciones_si_no_existe)
print(df_relaciones_nuevas)

driver.close()
