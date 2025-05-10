# Gestión de Transacciones en Neo4j

Neo4j es una base de datos transaccional compatible con ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad). Las transacciones en Neo4j aseguran que las operaciones de base de datos sean consistentes y confiables, permitiendo realizar múltiples operaciones dentro de una única transacción.

---

## 🔑 Conceptos Clave

### Sesiones

Las **sesiones** se utilizan para ejecutar transacciones en Neo4j. Una sesión maneja las conexiones subyacentes con la base de datos y permite ejecutar consultas transaccionales.

```python
with driver.session() as session:
    # Aquí puedes llamar a funciones de transacción
```

> Al utilizar `with`, la sesión se cierra automáticamente cuando se sale del bloque, liberando las conexiones subyacentes.

---

## 🔄 Transacciones en Neo4j

Las transacciones se pueden ejecutar usando los siguientes métodos del objeto `session`:

- `session.execute_read()`: Para ejecutar una transacción de solo lectura.
- `session.execute_write()`: Para ejecutar una transacción de escritura.

Estas funciones automáticamente gestionan la transacción: si la transacción tiene éxito, se confirma; si ocurre algún error, se revierte.

```python
# Transacción de lectura
with driver.session() as session:
    result = session.execute_read(my_read_function)

# Transacción de escritura
with driver.session() as session:
    session.execute_write(my_write_function)
```

---

## 🧠 Funciones de Transacción

Las funciones de transacción permiten ejecutar varias consultas dentro de la misma transacción, lo que garantiza que todas las operaciones se completen o fallen como una unidad.

### Ejemplo: Crear un nodo `Person`

```python
def create_person(tx, name, age):
    result = tx.run("""
    CREATE (p:Person {name: $name, age: $age})
    RETURN p
    """, name=name, age=age)
```

- `(1)` El primer argumento siempre es un objeto `ManagedTransaction`.
- `(2)` Se usa `tx.run()` para ejecutar la consulta Cypher.

---

## 🔁 Múltiples Consultas en una Transacción

Puedes ejecutar múltiples consultas dentro de una misma transacción. Esto asegura que todas las operaciones se completan juntas.

```python
def transfer_funds(tx, from_account, to_account, amount):
    # Deduce saldo de la primera cuenta
    tx.run(
        "MATCH (a:Account {id: $from_}) SET a.balance = a.balance - $amount",
        from_=from_account, amount=amount
    )
    # Agrega saldo a la segunda cuenta
    tx.run(
        "MATCH (a:Account {id: $to}) SET a.balance = a.balance + $amount",
        to=to_account, amount=amount
    )
```

---

## 💾 Estado de la Transacción

El estado de la transacción se mantiene en memoria del DBMS.  
> ❗ No ejecutes demasiadas operaciones en una sola transacción; esto puede afectar el rendimiento. Es recomendable dividirlas en transacciones más pequeñas.

---

## 📤 Manejo de Salidas

El método `run()` devuelve un objeto `Result`, el cual puede iterarse o consumirse con `consume()` para obtener un resumen (`Summary`) con metadatos.

```python
with driver.session() as session:
    def get_answer(tx, answer):
        result = tx.run("RETURN $answer AS answer", answer=answer)
        return result.consume()

    summary = session.execute_read(get_answer, answer=42)

    print(
        "Resultados disponibles después de", summary.result_available_after,
        "ms y consumidos después de", summary.result_consumed_after, "ms"
    )
```

---

## 🔁 Reintentos ante Errores Transitorios

Si la transacción falla debido a errores **transitorios** (por ejemplo, problemas de red o conflictos de concurrencia), los métodos `execute_read()` y `execute_write()` automáticamente reintentan ejecutar la transacción.

---

## 📝 Resumen de Métodos y Funciones

| Método o Función         | Descripción                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `session.execute_read()` | Ejecuta una transacción de solo lectura.                                   |
| `session.execute_write()`| Ejecuta una transacción de escritura.                                      |
| `tx.run()`               | Ejecuta una consulta Cypher dentro de una transacción.                     |
| `result.consume()`       | Consume los resultados y devuelve un objeto `Summary` con metadatos.       |
| `result_available_after` | Tiempo (ms) hasta que los resultados estuvieron disponibles.               |
| `result_consumed_after`  | Tiempo (ms) que tomó consumir completamente los resultados.                |

---

## 🧠 Consideraciones Finales

- **Control de transacciones**: Agrupar múltiples operaciones en una función de transacción asegura atomicidad y coherencia.
- **Rendimiento**: Evita mantener grandes transacciones por mucho tiempo.
- **Reintentos automáticos**: Las transacciones se reintentan automáticamente si fallan por errores transitorios.

---

Este resumen cubre los aspectos fundamentales de la gestión de transacciones en Neo4j, con ejemplos prácticos que puedes probar directamente en tu entorno.
