import sys
import json
import getpass
from typing import List, Dict, Any, Union

from .validator import PasswordValidator, ValidationResult, validate_password
from .email_validator import EmailValidator, EmailValidationResult, validate_email
from .user_manager import (
    User,
    UserManager,
    UserValidationResult,
    UserListValidationResult,
    validate_user,
    validate_users
)

__all__ = [
    "PasswordValidator",
    "ValidationResult",
    "validate_password",
    "EmailValidator",
    "EmailValidationResult",
    "validate_email",
    "User",
    "UserManager",
    "UserValidationResult",
    "UserListValidationResult",
    "validate_user",
    "validate_users",
    "main",
]

def show_password_validation(password: str) -> None:
    result = validate_password(password)
    print("\n--- Evaluación de Contraseña ---")
    print(f"• ¿Es válida?: {'✅ Sí' if result.is_valid else '❌ No'}")
    print(f"• Nivel de seguridad: {result.strength} ({result.score}/100)")

    criterios_labels = {
        "min_length": "Longitud mínima (>= 8 caracteres)",
        "max_length": "Longitud máxima (<= 128 caracteres)",
        "no_spaces": "Sin espacios en blanco",
        "uppercase": "Contiene mayúsculas (A-Z)",
        "lowercase": "Contiene minúsculas (a-z)",
        "digit": "Contiene números (0-9)",
        "special": "Contiene caracteres especiales (!@#...)",
        "not_common": "No es una contraseña común"
    }

    print("\nCriterios:")
    for key, ok in result.criteria.items():
        label = criterios_labels.get(key, key)
        icon = "✅" if ok else "❌"
        print(f"  {icon} {label}")

    if result.errors:
        print("\nSugerencias de mejora:")
        for err in result.errors:
            print(f"  ⚠️  {err}")

def show_email_validation(email: str) -> None:
    result = validate_email(email)
    print("\n--- Evaluación de Email ---")
    print(f"• ¿Es válido?: {'✅ Sí' if result.is_valid else '❌ No'}")
    if result.is_valid:
        print(f"• Email normalizado: {result.normalized_email}")
        print(f"• Usuario / Local: {result.local_part}")
        print(f"• Dominio: {result.domain}")
    else:
        print("\nErrores encontrados:")
        for err in result.errors:
            print(f"  ❌ {err}")

def show_user_validation(result: UserValidationResult) -> None:
    role_str = " [👑 Administrador]" if result.user.is_admin else ""
    print(f"\n--- Validación de Usuario: {result.user.name or result.user.email}{role_str} ---")
    print(f"• Estado general: {'✅ Válido' if result.is_valid else '❌ Inválido'}")
    print(f"• Rol: {'Administrador' if result.user.is_admin else 'Usuario estándar'}")
    print(f"• Email: {result.user.email} -> {'✅ Correcto' if result.email_result.is_valid else '❌ Inválido'}")
    
    if result.is_password_optional:
        if result.user.password:
            pwd_status = '✅ Válida' if result.password_result.is_valid else '⚠️ Opcional (no cumple criterios estrictos)'
            print(f"• Contraseña: {pwd_status} ({result.strength} - {result.score}/100) [Admin: Validación Opcional]")
        else:
            print("• Contraseña: ⚪ No requerida [Admin: Validación Opcional]")
    else:
        print(f"• Contraseña: {'✅ Válida' if result.password_result.is_valid else '❌ Inválida'} ({result.strength} - {result.score}/100)")
    
    if result.errors:
        print("\nDetalle de problemas:")
        for err in result.errors:
            print(f"  ❌  {err}")

    if result.warnings:
        print("\nAdvertencias (no bloqueantes):")
        for warn in result.warnings:
            print(f"  ⚠️  {warn}")

def show_batch_user_validation(batch: UserListValidationResult) -> None:
    print("\n" + "=" * 65)
    print(" 📊 RESUMEN DE EVALUACIÓN DE LISTA DE USUARIOS ")
    print("=" * 65)
    print(f"• Total de usuarios evaluados: {batch.total_users}")
    print(f"• Usuarios válidos: {batch.valid_users_count} ✅")
    print(f"• Usuarios inválidos: {batch.invalid_users_count} ❌")
    print(f"• Administradores: {batch.admin_users_count} 👑")
    print(f"• Puntuación media de contraseñas: {batch.average_password_score}/100")
    print(f"• ¿Lista 100% aprobada?: {'✅ Sí' if batch.is_all_valid else '❌ No'}")
    print("-" * 65)
    print(f"{'#':<3} | {'Email':<25} | {'Rol':<8} | {'Estado':<10} | {'Contraseña':<15}")
    print("-" * 65)

    for idx, r in enumerate(batch.results, 1):
        status_label = "✅ Válido" if r.is_valid else "❌ Error"
        role_label = "Admin" if r.user.is_admin else "User"
        if r.is_password_optional and not r.user.password:
            pwd_label = "Opcional (N/A)"
        else:
            pwd_label = f"{r.strength} ({r.score})"
        email_display = r.email if len(r.email) <= 25 else r.email[:22] + "..."
        print(f"{idx:<3} | {email_display:<25} | {role_label:<8} | {status_label:<10} | {pwd_label:<15}")
        if r.errors:
            for err in r.errors:
                print(f"     ↳ ❌  {err}")
        if r.warnings:
            for warn in r.warnings:
                print(f"     ↳ ⚠️  {warn}")

    print("=" * 65)

def main() -> None:
    """CLI interactivo para validar contraseñas, correos y listas de usuarios."""
    print("=" * 50)
    print(" 🛡️  VALIDADOR Y GESTOR DE USUARIOS ")
    print("=" * 50)

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        # Si se pasa un archivo JSON como argumento
        if arg.endswith(".json"):
            try:
                with open(arg, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    batch_res = validate_users(data)
                    show_batch_user_validation(batch_res)
                    return
            except Exception as ex:
                print(f"Error al leer archivo JSON: {ex}")
                return
        elif "@" in arg:
            show_email_validation(arg)
        else:
            show_password_validation(arg)
        print("=" * 50)
        return

    print("Selecciona qué deseas realizar:")
    print("1. Validar una contraseña individual")
    print("2. Validar un correo electrónico individual")
    print("3. Validar un usuario individual (Email + Contraseña)")
    print("4. Validar y gestionar lista de múltiples usuarios")

    try:
        opcion = input("\nElige una opción (1/2/3/4) [4]: ").strip() or "4"
        print("-" * 50)

        if opcion == "1":
            pwd = getpass.getpass("Ingresa la contraseña a evaluar: ")
            show_password_validation(pwd)
        elif opcion == "2":
            email = input("Ingresa el correo electrónico a evaluar: ").strip()
            show_email_validation(email)
        elif opcion == "3":
            nombre = input("Nombre (opcional): ").strip() or None
            email = input("Correo electrónico: ").strip()
            es_admin_input = input("¿Es administrador? (s/n) [n]: ").strip().lower()
            is_admin = es_admin_input in ("s", "si", "sí", "y", "yes", "true", "1")
            pwd_prompt = "Contraseña (opcional para admin): " if is_admin else "Contraseña: "
            pwd = getpass.getpass(pwd_prompt)
            user = User(email=email, password=pwd, name=nombre, is_admin=is_admin)
            res = validate_user(user)
            show_user_validation(res)
        elif opcion == "4":
            print("--- Ingreso de Lista de Usuarios ---")
            print("Ingresa los usuarios uno a uno. Deja el email vacío cuando termines.")
            users_list = []
            idx = 1
            while True:
                print(f"\n[Usuario #{idx}]")
                email = input("  Email (enter para finalizar): ").strip()
                if not email:
                    break
                es_admin_input = input("  ¿Es administrador? (s/n) [n]: ").strip().lower()
                is_admin = es_admin_input in ("s", "si", "sí", "y", "yes", "true", "1")
                pwd_prompt = "  Contraseña (opcional para admin): " if is_admin else "  Contraseña: "
                pwd = getpass.getpass(pwd_prompt)
                nombre = input("  Nombre (opcional): ").strip() or None
                users_list.append(User(email=email, password=pwd, name=nombre, is_admin=is_admin))
                idx += 1

            if not users_list:
                print("\nNo se ingresaron usuarios.")
            else:
                batch_res = validate_users(users_list)
                show_batch_user_validation(batch_res)
        else:
            print("Opción no válida.")
    except (KeyboardInterrupt, EOFError):
        print("\nOperación cancelada.")

    print("=" * 50)
