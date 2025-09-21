# python
import unittest
from functions.get_file_content import get_file_content

class TestGetFileContent(unittest.TestCase):
    def test_main_py_contains_main_def(self):
        out = get_file_content("calculator", "main.py")
        self.assertIn("def main():", out)

    def test_pkg_calculator_contains_apply_operator(self):
        out = get_file_content("calculator", "pkg/calculator.py")
        self.assertIn("def _apply_operator(self, operators, values)", out)

    def test_forbidden_absolute_path_errors(self):
        out = get_file_content("calculator", "/bin/cat")
        self.assertTrue(out.startswith("Error:"))

    def test_missing_file_errors(self):
        out = get_file_content("calculator", "pkg/does_not_exist.py")
        self.assertTrue(out.startswith("Error:"))

if __name__ == "__main__":
    unittest.main()