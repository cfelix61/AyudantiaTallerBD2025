from neo4j import GraphDatabase

# Conexión
uri = "neo4j://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))

# Transacción de escritura: Crear persona
def create_person(tx, name, age):
    query = """
    CREATE (p:Person {name: $name, age: $age})
    RETURN p.name AS name, p.age AS age
    """
    result = tx.run(query, name=name, age=age)
    return result.single()

# Transacción de lectura: Buscar persona
def find_person(tx, name):
    query = "MATCH (p:Person {name: $name}) RETURN p.name AS name, p.age AS age"
    result = tx.run(query, name=name)
    return result.single()

# Transacción múltiple (crear dos personas)
def create_two_people(tx, person1, person2):
    tx.run("CREATE (:Person {name: $name, age: $age})", **person1)
    tx.run("CREATE (:Person {name: $name, age: $age})", **person2)

# Uso de sesiones y transacciones
with driver.session(database="neo4j") as session:

    # Crear una persona
    created = session.execute_write(create_person, name="Ana", age=29)
    print("✅ Persona creada:", created)

    # Crear dos personas en una única transacción
    session.execute_write(
        create_two_people,
        {"name": "Luis", "age": 35},
        {"name": "Clara", "age": 31}
    )
    print("✅ Dos personas creadas.")

    # Leer una persona
    found = session.execute_read(find_person, name="Ana")
    print("🔍 Persona encontrada:", found)

    # Ejemplo de consumir resumen
    def get_summary(tx):
        result = tx.run("RETURN 'Hola mundo' AS saludo")
        summary = result.consume()
        return summary

    summary = session.execute_read(get_summary)
    print(f"⚡ Resultados disponibles después de {summary.result_available_after}ms, consumidos después de {summary.result_consumed_after}ms")

driver.close()
