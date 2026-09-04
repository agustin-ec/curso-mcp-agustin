import unittest
from vibe_coding.validator import PasswordValidator, validate_password

class TestPasswordValidator(unittest.TestCase):

    def setUp(self):
        self.validator = PasswordValidator()

    def test_valid_strong_password(self):
        res = self.validator.validate("C0mpl3x#P@ssw0rd!2026")
        self.assertTrue(res.is_valid)
        self.assertEqual(len(res.errors), 0)
        self.assertIn(res.strength, ["Fuerte", "Muy fuerte"])
        self.assertGreater(res.score, 70)

    def test_too_short(self):
        res = self.validator.validate("Ab1!")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("al menos 8" in err for err in res.errors))

    def test_missing_uppercase(self):
        res = self.validator.validate("password123!")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("mayúscula" in err for err in res.errors))

    def test_missing_lowercase(self):
        res = self.validator.validate("PASSWORD123!")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("minúscula" in err for err in res.errors))

    def test_missing_digit(self):
        res = self.validator.validate("Password!ABC")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("número" in err for err in res.errors))

    def test_missing_special(self):
        res = self.validator.validate("Password123")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("carácter especial" in err for err in res.errors))

    def test_disallow_spaces(self):
        res = self.validator.validate("Pass word123!")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("espacios en blanco" in err for err in res.errors))

    def test_common_password(self):
        res = self.validator.validate("123456")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("común" in err for err in res.errors))

    def test_convenience_function(self):
        res = validate_password("Valid_P@ssw0rd2026")
        self.assertTrue(res.is_valid)

if __name__ == "__main__":
    unittest.main()
