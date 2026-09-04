import re
import string
import math
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ValidationResult:
    is_valid: bool
    score: int  # 0 to 100
    strength: str  # 'Muy débil', 'Débil', 'Aceptable', 'Fuerte', 'Muy fuerte'
    errors: List[str] = field(default_factory=list)
    criteria: Dict[str, bool] = field(default_factory=dict)

class PasswordValidator:
    """Validador y evaluador de seguridad de contraseñas."""

    COMMON_PASSWORDS = {
        "123456", "password", "12345678", "qwerty", "123456789", "12345",
        "1234", "111111", "1234567", "dragon", "admin", "welcome", "abc123"
    }

    SPECIAL_CHARS = set(string.punctuation)

    def __init__(
        self,
        min_length: int = 8,
        max_length: int = 128,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True,
        disallow_spaces: bool = True,
        check_common: bool = True
    ):
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digit = require_digit
        self.require_special = require_special
        self.disallow_spaces = disallow_spaces
        self.check_common = check_common

    def validate(self, password: str) -> ValidationResult:
        errors: List[str] = []
        criteria: Dict[str, bool] = {}

        # 1. Verificación de longitud
        has_min_len = len(password) >= self.min_length
        has_max_len = len(password) <= self.max_length
        criteria["min_length"] = has_min_len
        criteria["max_length"] = has_max_len

        if not has_min_len:
            errors.append(f"Debe tener al menos {self.min_length} caracteres.")
        if not has_max_len:
            errors.append(f"No debe exceder {self.max_length} caracteres.")

        # 2. Espacios en blanco
        if self.disallow_spaces:
            no_spaces = " " not in password
            criteria["no_spaces"] = no_spaces
            if not no_spaces:
                errors.append("No debe contener espacios en blanco.")

        # 3. Mayúsculas
        if self.require_uppercase:
            has_upper = bool(re.search(r"[A-Z]", password))
            criteria["uppercase"] = has_upper
            if not has_upper:
                errors.append("Debe contener al menos una letra mayúscula (A-Z).")

        # 4. Minúsculas
        if self.require_lowercase:
            has_lower = bool(re.search(r"[a-z]", password))
            criteria["lowercase"] = has_lower
            if not has_lower:
                errors.append("Debe contener al menos una letra minúscula (a-z).")

        # 5. Dígitos
        if self.require_digit:
            has_digit = bool(re.search(r"\d", password))
            criteria["digit"] = has_digit
            if not has_digit:
                errors.append("Debe contener al menos un número (0-9).")

        # 6. Caracteres especiales
        if self.require_special:
            has_special = any(c in self.SPECIAL_CHARS for c in password)
            criteria["special"] = has_special
            if not has_special:
                errors.append("Debe contener al menos un carácter especial (ej. !@#$%^&*).")

        # 7. Contraseñas comunes
        if self.check_common:
            is_not_common = password.lower() not in self.COMMON_PASSWORDS
            criteria["not_common"] = is_not_common
            if not is_not_common:
                errors.append("Es una contraseña demasiado común y fácil de adivinar.")

        # Cálculo de fuerza y puntuación (0 a 100)
        score, strength = self._calculate_strength(password, criteria, errors)
        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            strength=strength,
            errors=errors,
            criteria=criteria
        )

    def _calculate_strength(
        self,
        password: str,
        criteria: Dict[str, bool],
        errors: List[str]
    ) -> tuple[int, str]:
        if not password:
            return 0, "Muy débil"

        # Calcular pool de caracteres disponibles
        pool_size = 0
        if re.search(r"[a-z]", password):
            pool_size += 26
        if re.search(r"[A-Z]", password):
            pool_size += 26
        if re.search(r"\d", password):
            pool_size += 10
        if any(c in self.SPECIAL_CHARS for c in password):
            pool_size += len(self.SPECIAL_CHARS)

        # Entropía en bits: L * log2(pool_size)
        if pool_size > 0:
            entropy = len(password) * math.log2(pool_size)
        else:
            entropy = 0

        # Mapeo de entropía a puntuación de 0 a 100
        # < 28 bits: Muy débil
        # 28-45 bits: Débil
        # 46-59 bits: Aceptable
        # 60-79 bits: Fuerte
        # >= 80 bits: Muy fuerte
        score = min(100, int((entropy / 80) * 100))

        # Penalización si hay errores de validación
        if errors:
            score = min(score, 50)
            if len(errors) >= 3:
                score = min(score, 25)

        if score < 25:
            strength = "Muy débil"
        elif score < 50:
            strength = "Débil"
        elif score < 70:
            strength = "Aceptable"
        elif score < 85:
            strength = "Fuerte"
        else:
            strength = "Muy fuerte"

        return score, strength


def validate_password(password: str, **kwargs) -> ValidationResult:
    """Función de conveniencia para validar una contraseña rápidamente."""
    validator = PasswordValidator(**kwargs)
    return validator.validate(password)
