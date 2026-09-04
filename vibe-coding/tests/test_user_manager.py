import unittest
from vibe_coding import (
    User,
    UserManager,
    UserValidationResult,
    UserListValidationResult,
    validate_user,
    validate_users
)

class TestUserManager(unittest.TestCase):

    def setUp(self):
        self.manager = UserManager()

    def test_user_creation_and_to_dict(self):
        user = User(email="test@example.com", password="Secure#Password123", name="Agustin")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "Secure#Password123")
        self.assertEqual(user.name, "Agustin")
        self.assertIsNotNone(user.id)
        
        user_dict = user.to_dict()
        self.assertEqual(user_dict["email"], "test@example.com")
        self.assertEqual(user_dict["name"], "Agustin")
        
        restored = User.from_dict(user_dict)
        self.assertEqual(restored.email, user.email)
        self.assertEqual(restored.password, user.password)
        self.assertEqual(restored.id, user.id)

    def test_validate_single_valid_user(self):
        user = User(email="agustin@domain.com", password="Str0ng!Password#2026")
        res = self.manager.validate_user(user)
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)
        self.assertTrue(res.email_result.is_valid)
        self.assertTrue(res.password_result.is_valid)
        self.assertEqual(res.email, "agustin@domain.com")
        self.assertGreater(res.score, 70)

    def test_validate_single_invalid_user_email_and_password(self):
        user = User(email="correo_invalido", password="123")
        res = self.manager.validate_user(user)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Email:" in e for e in res.errors))
        self.assertTrue(any("Contraseña:" in e for e in res.errors))

    def test_validate_users_list_mixed(self):
        users_input = [
            User(email="valido1@test.com", password="P@ssword123!", name="User 1"),
            {"email": "invalido-email", "password": "Valid!Password123", "name": "User 2"},
            ("valido2@test.com", "123", "User 3"),  # tuple format with weak pwd
            ["valido3@test.com", "V@lidPassword456!"]  # list format
        ]

        batch_res = self.manager.validate_users(users_input)
        self.assertEqual(batch_res.total_users, 4)
        self.assertEqual(batch_res.valid_users_count, 2)
        self.assertEqual(batch_res.invalid_users_count, 2)
        self.assertFalse(batch_res.is_all_valid)
        self.assertEqual(len(batch_res.valid_users), 2)
        self.assertEqual(len(batch_res.invalid_users), 2)

    def test_duplicate_email_detection_in_batch(self):
        users_input = [
            {"email": "duplicado@test.com", "password": "Password#123!"},
            {"email": "DUPLICADO@test.com", "password": "Password#456!"},
            {"email": "otro@test.com", "password": "Password#789!"}
        ]

        batch_res = self.manager.validate_users(users_input)
        self.assertEqual(batch_res.total_users, 3)
        self.assertTrue(batch_res.results[0].is_valid)
        self.assertFalse(batch_res.results[1].is_valid)
        self.assertTrue(batch_res.results[1].is_duplicate_email)
        self.assertTrue(any("duplicado" in e for e in batch_res.results[1].errors))
        self.assertTrue(batch_res.results[2].is_valid)

    def test_add_users_batch_storage(self):
        users_input = [
            {"email": "user1@test.com", "password": "S3cure#Pass1"},
            {"email": "user2@test.com", "password": "weak"},
            {"email": "user3@test.com", "password": "S3cure#Pass3"}
        ]
        
        # Con only_valid=True (por defecto) solo guarda los válidos
        res = self.manager.add_users(users_input, only_valid=True)
        self.assertEqual(res.total_users, 3)
        self.assertEqual(res.valid_users_count, 2)
        self.assertEqual(len(self.manager), 2)

        # Verificar lista de usuarios
        stored = self.manager.get_users()
        self.assertEqual(len(stored), 2)
        self.assertEqual(stored[0].email, "user1@test.com")
        self.assertEqual(stored[1].email, "user3@test.com")

    def test_add_user_and_store(self):
        res1 = self.manager.add_user({"email": "agustin@test.com", "password": "S3cure#Password123"})
        self.assertTrue(res1.is_valid)
        self.assertEqual(len(self.manager), 1)

        # Intento de agregar email duplicado
        res2 = self.manager.add_user({"email": "agustin@test.com", "password": "Other#Password456"})
        self.assertFalse(res2.is_valid)
        self.assertTrue(res2.is_duplicate_email)
        # No se debió añadir porque validate=True por defecto y fue inválido
        self.assertEqual(len(self.manager), 1)

        # Buscar usuario
        found = self.manager.find_by_email("AGUSTIN@test.com")
        self.assertIsNotNone(found)
        self.assertEqual(found.email, "agustin@test.com")

        # Eliminar usuario
        removed = self.manager.remove_by_email("agustin@test.com")
        self.assertTrue(removed)
        self.assertEqual(len(self.manager), 0)

        # Clear
        self.manager.add_user({"email": "tmp@test.com", "password": "S3cure#Password123"})
        self.assertEqual(len(self.manager), 1)
        self.manager.clear()
        self.assertEqual(len(self.manager), 0)

    def test_empty_user_list(self):
        res = self.manager.validate_users([])
        self.assertEqual(res.total_users, 0)
        self.assertEqual(res.valid_users_count, 0)
        self.assertEqual(res.average_password_score, 0.0)
        self.assertFalse(res.is_all_valid)

    def test_invalid_input_format(self):
        with self.assertRaises(ValueError):
            self.manager.validate_user(12345)  # type: ignore

    def test_convenience_functions(self):
        res_single = validate_user({"email": "test@domain.com", "password": "C0mpl3x#P@ssword2026"})
        self.assertTrue(res_single.is_valid)

        res_batch = validate_users([
            ("user1@test.com", "S3cure#Pass1"),
            ("user2@test.com", "S3cure#Pass2")
        ])
        self.assertTrue(res_batch.is_all_valid)
        self.assertEqual(res_batch.total_users, 2)
        summary = res_batch.summary()
        self.assertEqual(summary["total_users"], 2)
        self.assertEqual(summary["valid_users_count"], 2)

    def test_admin_user_role_and_flag_sync(self):
        # is_admin=True sincroniza role a 'admin'
        u1 = User(email="admin1@test.com", is_admin=True)
        self.assertTrue(u1.is_admin)
        self.assertEqual(u1.role, "admin")
        self.assertEqual(u1.password, "")

        # role='admin' sincroniza is_admin a True
        u2 = User(email="admin2@test.com", role="admin")
        self.assertTrue(u2.is_admin)
        self.assertEqual(u2.role, "admin")

        # Serialización a dict y deserialización
        u_dict = u1.to_dict()
        self.assertTrue(u_dict["is_admin"])
        self.assertEqual(u_dict["role"], "admin")
        restored = User.from_dict(u_dict)
        self.assertTrue(restored.is_admin)
        self.assertEqual(restored.role, "admin")

    def test_admin_password_validation_optional_by_default(self):
        # Admin con contraseña débil (ej. '123') es válido por defecto
        admin_weak = User(email="admin@domain.com", password="123", is_admin=True)
        res_weak = self.manager.validate_user(admin_weak)
        self.assertTrue(res_weak.is_valid)
        self.assertTrue(res_weak.is_password_optional)
        self.assertEqual(len(res_weak.errors), 0)
        self.assertGreater(len(res_weak.warnings), 0)  # Contiene advertencias no bloqueantes

        # Admin sin contraseña es válido por defecto
        admin_empty = User(email="admin_empty@domain.com", is_admin=True)
        res_empty = self.manager.validate_user(admin_empty)
        self.assertTrue(res_empty.is_valid)
        self.assertTrue(res_empty.is_password_optional)
        self.assertEqual(len(res_empty.errors), 0)
        self.assertEqual(res_empty.password_result.strength, "Opcional")

    def test_regular_user_password_validation_still_mandatory(self):
        # Usuario normal con contraseña débil debe fallar
        regular_user = User(email="user@domain.com", password="123")
        res = self.manager.validate_user(regular_user)
        self.assertFalse(res.is_valid)
        self.assertFalse(res.is_password_optional)
        self.assertTrue(any("Contraseña:" in e for e in res.errors))

    def test_admin_password_validation_when_explicitly_required(self):
        # Cuando se exige validación para admins, contraseña débil debe fallar
        strict_manager = UserManager(validate_admin_password=True)
        admin_weak = User(email="admin@domain.com", password="123", is_admin=True)
        res = strict_manager.validate_user(admin_weak)
        self.assertFalse(res.is_valid)
        self.assertFalse(res.is_password_optional)
        self.assertTrue(any("Contraseña:" in e for e in res.errors))

        # Cuando la contraseña es robusta, debe pasar
        admin_strong = User(email="admin@domain.com", password="Str0ng!AdminPass#2026", is_admin=True)
        res_strong = strict_manager.validate_user(admin_strong)
        self.assertTrue(res_strong.is_valid)

    def test_admin_email_validation_and_uniqueness_still_enforced(self):
        # Correo inválido debe fallar para admin
        admin_bad_email = User(email="correo_invalido", password="123", is_admin=True)
        res = self.manager.validate_user(admin_bad_email)
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Email:" in e for e in res.errors))

        # Email duplicado debe fallar para admin
        self.manager.add_user(User(email="admin@test.com", is_admin=True))
        dup_admin = User(email="admin@test.com", is_admin=True)
        res_dup = self.manager.add_user(dup_admin)
        self.assertFalse(res_dup.is_valid)
        self.assertTrue(res_dup.is_duplicate_email)

    def test_batch_validation_with_admins(self):
        users_input = [
            {"email": "admin1@test.com", "password": "weak", "is_admin": True},
            {"email": "admin2@test.com", "role": "admin"},  # sin contraseña
            {"email": "user1@test.com", "password": "Str0ng!Password#1"},
            {"email": "user2@test.com", "password": "weak"}  # usuario normal con pass débil -> inválido
        ]

        batch_res = self.manager.validate_users(users_input)
        self.assertEqual(batch_res.total_users, 4)
        self.assertEqual(batch_res.valid_users_count, 3)
        self.assertEqual(batch_res.invalid_users_count, 1)
        self.assertEqual(batch_res.admin_users_count, 2)
        self.assertEqual(len(batch_res.admin_users), 2)
        self.assertFalse(batch_res.is_all_valid)

    def test_normalize_user_variations_with_admin(self):
        # 3-tupla con bool: (email, pass, is_admin)
        u1 = self.manager._normalize_user(("admin@test.com", "123", True))
        self.assertTrue(u1.is_admin)
        self.assertEqual(u1.password, "123")

        # 4-tupla: (email, pass, name, 'admin')
        u2 = self.manager._normalize_user(("admin2@test.com", "123", "Admin Name", "admin"))
        self.assertTrue(u2.is_admin)
        self.assertEqual(u2.name, "Admin Name")

        # Gestor get_admins
        self.manager.clear()
        self.manager.add_user(u1)
        self.manager.add_user(("user@test.com", "Str0ng#Pass123!"))
        self.assertEqual(len(self.manager.get_admins()), 1)
        self.assertEqual(self.manager.get_admins()[0].email, "admin@test.com")


if __name__ == "__main__":
    unittest.main()
