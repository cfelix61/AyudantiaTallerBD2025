# Uso del Símbolo `$` en Consultas Cypher (Neo4j)

En Cypher, el lenguaje de consultas de Neo4j, el símbolo `$` se utiliza para referenciar **parámetros externos** dentro de una consulta. Esto permite separar la lógica de la consulta del valor de los datos.

---

## 🔹 ¿Qué es `$param`?

Es una **variable de parámetro**. Sirve como marcador de posición en la consulta que luego será reemplazado por un valor real proporcionado desde el código de aplicación.

### Ejemplo:
```cypher
MATCH (a:Person) WHERE a.name = $name RETURN a
ej code: 
def get_person_by_name(tx, name):
    result = tx.run("MATCH (a:Person) WHERE a.name = $name RETURN a", name=name)
    return result.single()
```
- $name en Cypher será reemplazado por el valor de name en Python.

✅ Ventajas del uso de parámetros
-------------------------------------------------------------------------
|Ventaja	|Descripción|
|Seguridad	|Evita inyecciones de código.|
|Rendimiento	|Permite a Neo4j reutilizar planes de ejecución.|
|Legibilidad	|Separa la lógica de la consulta del contenido variable.|
--------------------------------------------------------------------------