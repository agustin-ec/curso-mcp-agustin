import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Iterable, Union, Any

from .validator import PasswordValidator, ValidationResult
from .email_validator import EmailValidator, EmailValidationResult


@dataclass
class User:
    """Modelo de datos para un usuario con email, contraseña y rol."""
    email: str
    password: str = ""
    name: Optional[str] = None
    role: str = "user"
    is_admin: bool = False
    id: Optional[str] = field(default_factory=lambda: str(uuid.uuid4()))

    def __post_init__(self):
        if self.password is None:
            self.password = ""
        if self.is_admin or self.role == "admin":
            self.is_admin = True
            self.role = "admin"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "is_admin": self.is_admin
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        is_admin_val = data.get("is_admin", False)
        role_val = data.get("role", "admin" if is_admin_val else "user")
        is_admin = bool(is_admin_val or str(role_val).lower() == "admin")
        return cls(
            email=data.get("email", ""),
            password=data.get("password", ""),
            name=data.get("name"),
            role="admin" if is_admin else str(role_val),
            is_admin=is_admin,
            id=data.get("id", str(uuid.uuid4()))
        )


@dataclass
class UserValidationResult:
    """Resultado de la validación individual de un usuario."""
    user: User
    is_valid: bool
    email_result: EmailValidationResult
    password_result: ValidationResult
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    is_duplicate_email: bool = False
    is_password_optional: bool = False

    @property
    def email(self) -> str:
        return self.user.email

    @property
    def score(self) -> int:
        return self.password_result.score

    @property
    def strength(self) -> str:
        return self.password_result.strength

    @property
    def is_admin(self) -> bool:
        return self.user.is_admin


@dataclass
class UserListValidationResult:
    """Resultado acumulado de la validación de una lista de usuarios."""
    results: List[UserValidationResult] = field(default_factory=list)

    @property
    def total_users(self) -> int:
        return len(self.results)

    @property
    def valid_users(self) -> List[User]:
        return [r.user for r in self.results if r.is_valid]

    @property
    def invalid_users(self) -> List[User]:
        return [r.user for r in self.results if not r.is_valid]

    @property
    def admin_users(self) -> List[User]:
        return [r.user for r in self.results if r.user.is_admin]

    @property
    def valid_users_count(self) -> int:
        return len(self.valid_users)

    @property
    def invalid_users_count(self) -> int:
        return len(self.invalid_users)

    @property
    def admin_users_count(self) -> int:
        return len(self.admin_users)

    @property
    def is_all_valid(self) -> bool:
        return self.total_users > 0 and self.invalid_users_count == 0

    @property
    def average_password_score(self) -> float:
        scored = [r for r in self.results if r.user.password or not r.is_password_optional]
        if not scored:
            return 0.0
        total_score = sum(r.password_result.score for r in scored)
        return round(total_score / len(scored), 2)

    def summary(self) -> Dict[str, Any]:
        return {
            "total_users": self.total_users,
            "valid_users_count": self.valid_users_count,
            "invalid_users_count": self.invalid_users_count,
            "admin_users_count": self.admin_users_count,
            "is_all_valid": self.is_all_valid,
            "average_password_score": self.average_password_score
        }


class UserManager:
    """Gestor y validador de listas de usuarios con credenciales (email y contraseña)."""

    def __init__(
        self,
        password_validator: Optional[PasswordValidator] = None,
        email_validator: Optional[EmailValidator] = None,
        allow_duplicate_emails: bool = False,
        validate_admin_password: bool = False,
        **kwargs
    ):
        self.password_validator = password_validator or PasswordValidator()
        self.email_validator = email_validator or EmailValidator()
        self.allow_duplicate_emails = allow_duplicate_emails
        if "require_admin_password" in kwargs:
            self.validate_admin_password = kwargs["require_admin_password"]
        elif "optional_admin_password" in kwargs:
            self.validate_admin_password = not kwargs["optional_admin_password"]
        else:
            self.validate_admin_password = validate_admin_password
        self._users: List[User] = []

    def _normalize_user(self, user_data: Union[User, Dict[str, Any], tuple, list]) -> User:
        """Convierte diferentes representaciones en un objeto User."""
        if isinstance(user_data, User):
            return user_data
        elif isinstance(user_data, dict):
            return User.from_dict(user_data)
        elif isinstance(user_data, (tuple, list)):
            if len(user_data) == 1:
                return User(email=str(user_data[0]))
            elif len(user_data) == 2:
                return User(email=str(user_data[0]), password=str(user_data[1]))
            elif len(user_data) == 3:
                if isinstance(user_data[2], bool):
                    return User(email=str(user_data[0]), password=str(user_data[1]), is_admin=user_data[2])
                return User(email=str(user_data[0]), password=str(user_data[1]), name=str(user_data[2]))
            elif len(user_data) >= 4:
                val_admin = user_data[3]
                is_admin = False
                role = "user"
                if isinstance(val_admin, bool):
                    is_admin = val_admin
                    role = "admin" if is_admin else "user"
                elif str(val_admin).lower() == "admin":
                    is_admin = True
                    role = "admin"
                return User(
                    email=str(user_data[0]),
                    password=str(user_data[1]),
                    name=str(user_data[2]),
                    role=role,
                    is_admin=is_admin
                )
        raise ValueError(f"Formato de usuario no soportado: {user_data}")

    def validate_user(
        self,
        user_input: Union[User, Dict[str, Any], tuple, list],
        existing_emails: Optional[set] = None,
        validate_admin_password: Optional[bool] = None
    ) -> UserValidationResult:
        """Valida un usuario individual contra reglas de email y contraseña, y verifica duplicidad."""
        user = self._normalize_user(user_input)
        email_res = self.email_validator.validate(user.email)
        
        check_admin = self.validate_admin_password if validate_admin_password is None else validate_admin_password
        is_pwd_optional = user.is_admin and not check_admin

        if not user.password and is_pwd_optional:
            pwd_res = ValidationResult(
                is_valid=True,
                score=0,
                strength="Opcional",
                errors=[],
                criteria={}
            )
        else:
            pwd_res = self.password_validator.validate(user.password or "")

        errors: List[str] = []
        warnings: List[str] = []
        is_duplicate = False

        if not email_res.is_valid:
            errors.extend([f"Email: {err}" for err in email_res.errors])

        if not pwd_res.is_valid:
            if is_pwd_optional:
                warnings.extend([f"Contraseña (opcional para admin): {err}" for err in pwd_res.errors])
            else:
                errors.extend([f"Contraseña: {err}" for err in pwd_res.errors])

        if not self.allow_duplicate_emails and existing_emails is not None:
            norm_email = (email_res.normalized_email or user.email).strip().lower()
            if norm_email in existing_emails:
                is_duplicate = True
                errors.append(f"Email duplicado: '{user.email}' ya existe en la lista de usuarios.")

        pwd_valid = pwd_res.is_valid or is_pwd_optional
        is_valid = email_res.is_valid and pwd_valid and not is_duplicate

        return UserValidationResult(
            user=user,
            is_valid=is_valid,
            email_result=email_res,
            password_result=pwd_res,
            errors=errors,
            warnings=warnings,
            is_duplicate_email=is_duplicate,
            is_password_optional=is_pwd_optional
        )

    def validate_users(
        self,
        users_list: Iterable[Union[User, Dict[str, Any], tuple, list]],
        validate_admin_password: Optional[bool] = None
    ) -> UserListValidationResult:
        """Valida una lista completa de usuarios detectando duplicados entre ellos."""
        seen_emails: set = set()
        results: List[UserValidationResult] = []

        for item in users_list:
            user = self._normalize_user(item)
            res = self.validate_user(
                user,
                existing_emails=seen_emails,
                validate_admin_password=validate_admin_password
            )
            results.append(res)

            norm_email = (res.email_result.normalized_email or user.email).strip().lower()
            seen_emails.add(norm_email)

        return UserListValidationResult(results=results)

    def add_user(
        self,
        user_input: Union[User, Dict[str, Any], tuple, list],
        validate: bool = True,
        validate_admin_password: Optional[bool] = None
    ) -> UserValidationResult:
        """Añade un usuario al gestor."""
        user = self._normalize_user(user_input)
        existing_emails = {
            (u.email.strip().lower()) for u in self._users
        }
        val_res = self.validate_user(
            user,
            existing_emails=existing_emails,
            validate_admin_password=validate_admin_password
        )

        if not validate or val_res.is_valid:
            self._users.append(user)

        return val_res

    def add_users(
        self,
        users_list: Iterable[Union[User, Dict[str, Any], tuple, list]],
        only_valid: bool = True,
        validate_admin_password: Optional[bool] = None
    ) -> UserListValidationResult:
        """Añade una lista de usuarios al gestor."""
        existing_emails = {
            (u.email.strip().lower()) for u in self._users
        }
        results: List[UserValidationResult] = []

        for item in users_list:
            user = self._normalize_user(item)
            val_res = self.validate_user(
                user,
                existing_emails=existing_emails,
                validate_admin_password=validate_admin_password
            )
            results.append(val_res)

            norm_email = (val_res.email_result.normalized_email or user.email).strip().lower()
            existing_emails.add(norm_email)

            if not only_valid or val_res.is_valid:
                self._users.append(user)

        return UserListValidationResult(results=results)

    def get_users(self) -> List[User]:
        """Obtiene la lista actual de usuarios gestionados."""
        return list(self._users)

    def get_admins(self) -> List[User]:
        """Obtiene la lista actual de administradores gestionados."""
        return [u for u in self._users if u.is_admin]

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su email."""
        clean = email.strip().lower()
        for u in self._users:
            if u.email.strip().lower() == clean:
                return u
        return None

    def remove_by_email(self, email: str) -> bool:
        """Elimina un usuario por su email."""
        initial_len = len(self._users)
        clean = email.strip().lower()
        self._users = [u for u in self._users if u.email.strip().lower() != clean]
        return len(self._users) < initial_len

    def clear(self) -> None:
        """Limpia todos los usuarios almacenados."""
        self._users.clear()

    def __len__(self) -> int:
        return len(self._users)


def validate_users(
    users: Iterable[Union[User, Dict[str, Any], tuple, list]],
    **kwargs
) -> UserListValidationResult:
    """Función de conveniencia para validar una lista de usuarios."""
    manager = UserManager(**kwargs)
    return manager.validate_users(users)


def validate_user(
    user: Union[User, Dict[str, Any], tuple, list],
    **kwargs
) -> UserValidationResult:
    """Función de conveniencia para validar un único usuario."""
    manager = UserManager(**kwargs)
    return manager.validate_user(user)
