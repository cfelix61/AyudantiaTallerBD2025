from neo4j import GraphDatabase
import pandas as pd

# Conexión
URI = "neo4j://localhost:7687"
USER = "neo4j"
PASSWORD = "12345678"
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
driver.verify_connectivity()

# Función para crear cada jugador
def insert_player(tx, row):
    query = """
    MERGE (p:FPlayer {
        name: $name,
        team: $team,
        year: $year
    })
    SET p.position = $position,
        p.age = $age,
        p.height = $height,
        p.weight = $weight,
        p.nationality = $nationality,
        p.matches = $matches,
        p.substitutions = $substitutions,
        p.goals = $goals,
        p.assists = $assists,
        p.yellowCards = $yellowCards,
        p.redCards = $redCards,
        p.foulsCommitted = $foulsCommitted,
        p.foulsSuffered = $foulsSuffered,
        p.TT = $TT,
        p.TM = $TM
    """
    tx.run(query, **row)

# Cargar el CSV
df = pd.read_csv("csvPrueba.csv")

# Limpieza y conversión de tipos a int 
def convert_val(val, to_type):
    try:
        return to_type(val)
    except:
        return None

numeric_fields = {
    "Año": int, "Edad": int, "Partidos": int, "Sustituciones": int, "Goles": int,
    "Asistencias": int, "TA": int, "TR": int, "FC": int, "FS": int, "TT": int, "TM": int
}
for col, to_type in numeric_fields.items(): #convierto cada atributo a su valor en el diccionario
    df[col] = df[col].apply(lambda x: convert_val(x, to_type))

# Insertar cada fila de jugador en la base de datos
with driver.session() as session:
    for _, row in df.iterrows():
        data = {
            "name": row["Nombre"],
            "team": row["Equipo"],
            "year": row["Año"],
            "position": row["Posición"],
            "age": row["Edad"],
            "height": row["Estatura"],
            "weight": row["Peso"],
            "nationality": row["Nacionalidad"],
            "matches": row["Partidos"],
            "substitutions": row["Sustituciones"],
            "goals": row["Goles"],
            "assists": row["Asistencias"],
            "yellowCards": row["TA"],
            "redCards": row["TR"],
            "foulsCommitted": row["FC"],
            "foulsSuffered": row["FS"],
            "TT": row["TT"],
            "TM": row["TM"]
        }
        session.write_transaction(insert_player, data)

print("Jugadores insertados correctamente.")
driver.close()
