# 🛡️ Vibe Coding - Validador y Gestor de Credenciales y Usuarios

Paquete en Python para validación robusta y evaluación de seguridad de correos electrónicos, contraseñas y gestión de listas de usuarios.

## 🚀 Características

1. **Validador de Contraseñas (`PasswordValidator`)**:
   - Cumplimiento de longitud mínima y máxima.
   - Requisitos de mayúsculas, minúsculas, dígitos y caracteres especiales.
   - Prohibición opcional de espacios en blanco.
   - Detección de contraseñas comunes y vulnerables.
   - Cálculo de entropía en bits y puntuación de seguridad (0 a 100) con niveles (*Muy débil*, *Débil*, *Aceptable*, *Fuerte*, *Muy fuerte*).

2. **Validador de Correos Electrónicos (`EmailValidator`)**:
   - Cumplimiento de estándares RFC 5322 / RFC 5321.
   - Validación y normalización de la parte local y el dominio.
   - Verificación de etiquetas y TLD válido.

3. **Gestor y Validador Multiusuario (`UserManager`)**:
   - Manejo de listas de usuarios (`User`) con email, contraseña, nombre opcional y rol de administrador (`is_admin` o `role="admin"`).
   - **Validación de contraseña opcional para administradores**: Por defecto, los usuarios administradores pueden omitir o tener contraseñas simples sin invalidar el registro (generando advertencias informativas en lugar de errores bloqueantes). Configurable mediante `validate_admin_password=True`.
   - Detección automática de correos duplicados (case-insensitive) dentro del lote o en el gestor.
   - Métodos de filtrado (`valid_users`, `invalid_users`, `admin_users`), estadísticas y métricas acumuladas (`average_password_score`, `is_all_valid`, `admin_users_count`).
   - Soporte para diferentes formatos de entrada (`User`, `dict`, `tuple`, `list`).

---

## 💻 Ejemplos de Uso

### 1. Validación con Usuarios Administradores y Estándar

```python
from vibe_coding import validate_users, User

usuarios = [
    # Usuario normal: contraseña segura requerida
    User(email="agustin@ejemplo.com", password="S3cure#Password2026", name="Agustín"),
    # Administrador: validación de contraseña opcional (pasa con contraseña simple o vacía)
    User(email="admin@ejemplo.com", password="123", is_admin=True, name="Super Admin"),
    # Formato diccionario con rol de administrador
    {"email": "root@ejemplo.com", "role": "admin"},
    # Usuario normal con contraseña débil (quedará marcado como inválido)
    {"email": "invalido@test.com", "password": "123", "name": "Usuario Inválido"},
]

resultado = validate_users(usuarios)

print(f"Total: {resultado.total_users}")
print(f"Válidos: {resultado.valid_users_count}")
print(f"Administradores: {resultado.admin_users_count}")
print(f"Puntuación promedio de contraseña: {resultado.average_password_score}/100")

for r in resultado.results:
    admin_tag = " [Admin]" if r.user.is_admin else ""
    print(f"- {r.email}{admin_tag}: {'✅ Válido' if r.is_valid else '❌ Inválido'}")
    if r.warnings:
        print(f"  Advertencias: {r.warnings}")
    if r.errors:
        print(f"  Errores: {r.errors}")
```

### 2. Uso del Gestor de Usuarios (`UserManager`)

```python
from vibe_coding import UserManager, User

manager = UserManager()

# Agregar administrador con contraseña opcional/simple
res_admin = manager.add_user({"email": "admin@empresa.com", "password": "123", "is_admin": True})
print("Admin agregado:", res_admin.is_valid)  # True

# Agregar usuario normal con contraseña robusta
res_user = manager.add_user({"email": "dev@empresa.com", "password": "Adm1n#S3curePass!"})
print("Usuario agregado:", res_user.is_valid)  # True

# Obtener administradores
admins = manager.get_admins()
print(f"Total administradores: {len(admins)}")
```

### 3. Ejecución de la CLI Interactiva

```bash
python -m vibe_coding
```

O si está instalado con `uv` o `pip`:

```bash
vibe-coding
```

---

## 🧪 Ejecución de Pruebas

Para ejecutar la suite de pruebas unitarias:

```bash
PYTHONPATH=src python3 -m unittest discover tests
```
