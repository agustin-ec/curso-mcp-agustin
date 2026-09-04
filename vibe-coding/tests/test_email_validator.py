import unittest
from vibe_coding.email_validator import EmailValidator, validate_email

class TestEmailValidator(unittest.TestCase):

    def setUp(self):
        self.validator = EmailValidator()

    def test_valid_standard_emails(self):
        valid_cases = [
            "usuario@dominio.com",
            "nombre.apellido@empresa.org",
            "dev+test@dominio.co.uk",
            "agustin_123@sub.dominio.pe",
            "user-name@domain.tech"
        ]
        for email in valid_cases:
            with self.subTest(email=email):
                res = self.validator.validate(email)
                self.assertTrue(res.is_valid, f"Falló para: {email}, errores: {res.errors}")
                self.assertEqual(res.normalized_email, email.lower())

    def test_empty_or_whitespace_email(self):
        for email in ["", "   ", None]:
            res = self.validator.validate(email)
            self.assertFalse(res.is_valid)

    def test_missing_at_symbol(self):
        res = self.validator.validate("usuariodominio.com")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Falta el símbolo '@'" in err for err in res.errors))

    def test_multiple_at_symbols(self):
        res = self.validator.validate("user@@domain.com")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("múltiples" in err for err in res.errors))

    def test_invalid_local_part_dots(self):
        invalid_cases = [
            ".usuario@dominio.com",
            "usuario.@dominio.com",
            "usu..ario@dominio.com"
        ]
        for email in invalid_cases:
            with self.subTest(email=email):
                res = self.validator.validate(email)
                self.assertFalse(res.is_valid)

    def test_spaces_in_email(self):
        res = self.validator.validate("user name@domain.com")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("espacios" in err for err in res.errors))

    def test_invalid_domain_structure(self):
        invalid_domains = [
            "user@dominio",
            "user@.dominio.com",
            "user@dominio..com",
            "user@dominio.c",
            "user@-dominio.com"
        ]
        for email in invalid_domains:
            with self.subTest(email=email):
                res = self.validator.validate(email)
                self.assertFalse(res.is_valid)

    def test_convenience_function(self):
        res = validate_email("ernesto@hotmail.com")
        self.assertTrue(res.is_valid)
        self.assertEqual(res.local_part, "ernesto")
        self.assertEqual(res.domain, "hotmail.com")

if __name__ == "__main__":
    unittest.main()
