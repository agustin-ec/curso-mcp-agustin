import re
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class EmailValidationResult:
    is_valid: bool
    email: str
    normalized_email: Optional[str] = None
    local_part: Optional[str] = None
    domain: Optional[str] = None
    errors: List[str] = field(default_factory=list)

class EmailValidator:
    """Validador de formato y estructura de correos electrónicos (RFC 5322 / RFC 5321)."""

    # Caracteres permitidos en la parte local (sin comillas)
    LOCAL_PART_REGEX = re.compile(r"^[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*$")
    # Subdominio (etiqueta DNS)
    DOMAIN_LABEL_REGEX = re.compile(r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$")

    def __init__(self, check_tld_length: bool = True, max_length: int = 254):
        self.check_tld_length = check_tld_length
        self.max_length = max_length

    def validate(self, email: str) -> EmailValidationResult:
        errors: List[str] = []

        if not isinstance(email, str) or not email.strip():
            return EmailValidationResult(
                is_valid=False,
                email=email if isinstance(email, str) else "",
                errors=["El correo electrónico no puede estar vacío."]
            )

        email_clean = email.strip()

        # 1. Longitud total (RFC 5321: máx 254 caracteres)
        if len(email_clean) > self.max_length:
            errors.append(f"El correo excede la longitud máxima permitida ({self.max_length} caracteres).")

        # 2. Espacios intermedios
        if " " in email_clean:
            errors.append("El correo no debe contener espacios en blanco.")

        # 3. Presencia del separador '@'
        if "@" not in email_clean:
            errors.append("Falta el símbolo '@'.")
            return EmailValidationResult(is_valid=False, email=email_clean, errors=errors)

        parts = email_clean.split("@")
        if len(parts) > 2:
            errors.append("El correo contiene múltiples símbolos '@'.")
            return EmailValidationResult(is_valid=False, email=email_clean, errors=errors)

        local_part, domain = parts[0], parts[1]

        # 4. Validación de la parte local
        if not local_part:
            errors.append("La parte local (antes del '@') no puede estar vacía.")
        elif len(local_part) > 64:
            errors.append("La parte local no puede exceder 64 caracteres.")
        elif local_part.startswith(".") or local_part.endswith("."):
            errors.append("La parte local no puede comenzar ni terminar con un punto ('.').")
        elif ".." in local_part:
            errors.append("La parte local no puede contener puntos consecutivos ('..').")
        elif not self.LOCAL_PART_REGEX.match(local_part):
            errors.append("La parte local contiene caracteres no permitidos.")

        # 5. Validación del dominio
        if not domain:
            errors.append("El dominio (después del '@') no puede estar vacío.")
        elif len(domain) > 253:
            errors.append("El dominio no puede exceder 253 caracteres.")
        elif domain.startswith(".") or domain.endswith("."):
            errors.append("El dominio no puede comenzar ni terminar con un punto ('.').")
        elif ".." in domain:
            errors.append("El dominio no puede contener puntos consecutivos ('..').")
        else:
            domain_labels = domain.split(".")
            if len(domain_labels) < 2:
                errors.append("El dominio debe incluir una extensión válida (ej. .com, .org, .edu.pe).")
            else:
                for label in domain_labels:
                    if not self.DOMAIN_LABEL_REGEX.match(label):
                        errors.append(f"La etiqueta del dominio '{label}' contiene caracteres no válidos o formato incorrecto.")
                        break

                # Validar TLD (Top-Level Domain)
                tld = domain_labels[-1]
                if self.check_tld_length:
                    if len(tld) < 2:
                        errors.append("La extensión del dominio (TLD) debe tener al menos 2 caracteres.")
                    elif not tld.isalpha():
                        errors.append("La extensión del dominio (TLD) solo debe contener letras.")

        is_valid = len(errors) == 0
        normalized = f"{local_part}@{domain.lower()}" if is_valid else None

        return EmailValidationResult(
            is_valid=is_valid,
            email=email_clean,
            normalized_email=normalized,
            local_part=local_part if is_valid else None,
            domain=domain.lower() if is_valid else None,
            errors=errors
        )


def validate_email(email: str, **kwargs) -> EmailValidationResult:
    """Función de conveniencia para validar un correo electrónico rápidamente."""
    validator = EmailValidator(**kwargs)
    return validator.validate(email)
