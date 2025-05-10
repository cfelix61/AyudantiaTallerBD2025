### paths
path = record["path"]

print(path.start_node)  
print(path.end_node)    
print(len(path))  
print(path.relationships)  

el camino que toman los nodos para llegar a destino


###  Spatial Types en Neo4j

Neo4j soporta **datos espaciales** en 2D y 3D mediante el tipo `Point`, que puede representar:
- Coordenadas **geográficas** (WGS84)
- Coordenadas **cartesianas** (x, y [, z])

#### Tipos de Puntos

| Tipo de Punto     | Clase Python                        | SRID (2D) | SRID (3D) |
|-------------------|-------------------------------------|-----------|-----------|
| WGS-84 (geográfico)| `neo4j.spatial.WGS84Point`          | 4326      | 4979      |
| Cartesian (plano) | `neo4j.spatial.CartesianPoint`      | 7203      | 9157      |

---

#### CartesianPoint
Define puntos con coordenadas `(x, y)` o `(x, y, z)`.

```python
from neo4j.spatial import CartesianPoint

two_d = CartesianPoint((1.2, 3.4))
three_d = CartesianPoint((1.2, 3.4, 5.6))

print(two_d.x, two_d.y, two_d.srid)
x, y = two_d  # destructuring

```
#### WGS84Point
Representa coordenadas geográficas: (longitude, latitude [, height]).

```python
Copiar código
from neo4j.spatial import WGS84Point

ldn = WGS84Point((-0.118, 51.509))
shard = WGS84Point((-0.0865, 51.5045, 310))

#Acceso:

print(ldn.longitude, ldn.latitude)
longitude, latitude, height = shard
📏 Distancia entre puntos
```
Puedes usar point.distance(p1, p2) en Cypher para obtener la distancia en línea recta entre dos puntos con el mismo SRID.

```python
Copiar código
from neo4j.spatial import CartesianPoint

p1 = CartesianPoint((1, 1))
p2 = CartesianPoint((10, 10))

records, _, _ = driver.execute_query("""
RETURN point.distance($p1, $p2) AS distance
""", p1=p1, p2=p2)

print(records[0]["distance"])  # Resultado: 12.7279...
```
Si los SRID de los puntos son distintos, point.distance devuelve None.