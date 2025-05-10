from neo4j import GraphDatabase
from neo4j.spatial import CartesianPoint, WGS84Point

# Conexión
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "12345678"))

# Crear nodos con puntos espaciales
driver.execute_query("""
CREATE (:LocationCartesian {
    name: 'PuntoA',
    position: point({x: 1.0, y: 2.0, z: 3.0})
}),
(:LocationWGS {
    name: 'Londres',
    position: point({longitude: -0.118092, latitude: 51.509865, height: 50})
})
""")

# Consultar puntos creados
records, _, _ = driver.execute_query("""
MATCH (c:LocationCartesian), (w:LocationWGS)
RETURN c.position AS cartesian, w.position AS wgs
""")

cartesian = records[0]["cartesian"]
wgs = records[0]["wgs"]

print("📌 Coordenadas Cartesianas:")
print(f"x: {cartesian.x}, y: {cartesian.y}, z: {cartesian.z}, SRID: {cartesian.srid}")

print("\n🌍 Coordenadas Geográficas:")
print(f"Longitude: {wgs.longitude}, Latitude: {wgs.latitude}, Height: {wgs.height}, SRID: {wgs.srid}")

# Calcular distancia entre dos puntos cartesianas en Python
p1 = CartesianPoint((1.0, 2.0))
p2 = CartesianPoint((10.0, 10.0))

records, _, _ = driver.execute_query("""
RETURN point.distance($p1, $p2) AS distancia
""", p1=p1, p2=p2)

print(f"\n📏 Distancia entre puntos cartesianos: {records[0]['distancia']:.2f} unidades")

driver.close()
