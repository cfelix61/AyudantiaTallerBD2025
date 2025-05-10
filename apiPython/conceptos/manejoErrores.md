
# 🛠️ Manejo de Errores en Cypher (Neo4j)

Al trabajar con Neo4j, es común encontrarse con errores que deben ser **gestionados adecuadamente** para asegurar que la aplicación sea robusta y resiliente.

---

## ⚠️ Tipos de Errores

El controlador oficial de Neo4j en Python define excepciones que permiten distinguir el origen del error.

### 🔹 Jerarquía de errores

- **Neo4jError**: Clase base para errores del motor de base de datos.
- **DriverError**: Subclase para errores relacionados con el controlador/conexión.

### 🔹 Excepciones comunes

| Excepción              | Situación                                                          |
|------------------------|--------------------------------------------------------------------|
| `CypherSyntaxError`    | La sintaxis de la consulta Cypher es inválida.                    |
| `ConstraintError`      | Se ha violado una restricción única u otra en el esquema.         |
| `AuthError`            | Falla de autenticación.                                            |
| `TransientError`       | La base de datos no está disponible o el recurso está ocupado.    |

---

## 📋 Propiedades del error

Cualquier error generado por el DBMS (Neo4jError) posee:

- `code`: Código de error como `"Neo.ClientError.Schema.ConstraintValidationFailed"`.
- `message`: Descripción legible del error.
- `gql_status`: Código GQL según el estándar ISO GQL (ej. `22N41`).

---

## 🐍 Ejemplo básico en Python

```python
from neo4j.exceptions import Neo4jError

try:
    # Ejecutar una consulta Cypher
    tx.run("MATCH (n) RETURN n")
except Neo4jError as e:
    print(e.code)
    print(e.message)
    print(e.gql_status)
```

---

## 🔐 Ejemplo: Violación de Restricción Única

Crear una restricción única:

```cypher
CREATE CONSTRAINT unique_email IF NOT EXISTS
FOR (u:User) REQUIRE u.email IS UNIQUE
```

Si se intenta insertar un usuario con un `email` ya existente, se generará un `ConstraintError`.

### ✅ Manejo en Python

```python
from neo4j.exceptions import ConstraintError

def create_user(tx, name, email):
    try:
        result = tx.run("""
            CREATE (u:User {name: $name, email: $email})
            RETURN u
        """, name=name, email=email)
    except ConstraintError as e:
        print(e.code)        # Ej: Neo.ClientError.Schema.ConstraintValidationFailed
        print(e.message)     # Ej: The value [email] for property [email] violates the constraint [unique_email]
        print(e.gql_status)  # Ej: 22N41
```

---

## 📚 Recursos adicionales

- Documentación oficial de Neo4j para [Códigos de Estado](https://neo4j.com/docs/status-codes/current/)
- [Neo4j Driver API Docs](https://neo4j.com/docs/api/python-driver/)

---

## ✅ Recomendaciones

- Maneja explícitamente los errores específicos que esperas (como `ConstraintError`).
- Usa `Neo4jError` como fallback para capturar otros errores inesperados.
- Nunca asumas que una consulta siempre se ejecutará correctamente.

