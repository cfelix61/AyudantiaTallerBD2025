from neo4j import GraphDatabase
import pandas as pd

# Conexión con la base de datos
URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678" # Cambia esto por la contraseña que ingresaste al crear la base de datos

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
driver.verify_connectivity()

# Función para ejecutar consultas
def run_query(cypher_query: str, parameters: dict = {}) -> pd.DataFrame:
    with driver.session() as session:
        result = session.run(cypher_query, parameters)
        # Se convierte a DataFrame
        data = [record.data() for record in result]
        return pd.DataFrame(data)

# ---------- EJEMPLO DE CONSULTA: Goleadores de Colo-Colo ---------- #
query_goleadores_colocolo = """
MATCH (p:FPlayer)
WHERE p.team = $club and p.goals > 0
RETURN p.name AS jugador, p.goals AS goles
ORDER BY goles DESC
LIMIT 10
"""
club = "Colo Colo"
df_goleadores = run_query(query_goleadores_colocolo, parameters={"club": club})
print(df_goleadores)

# ---------- EJEMPLO DE VISUALIZACIÓN ---------- #
import matplotlib.pyplot as plt

def plot_goleadores(df):
    if df.empty:
        print("No se encontraron datos.")
        return
    plt.figure(figsize=(10, 6))
    plt.barh(df['jugador'], df['goles'], color='skyblue')
    plt.xlabel("Goles")
    plt.title("Goleadores de Colo-Colo - Liga Chilena 2025")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

plot_goleadores(df_goleadores)

# Cierre de la conexión
driver.close()
