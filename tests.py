# python
import unittest
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

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
    
    def test_write_lorem(self):
        out = write_file("calculator", "lorem.txt", 
                         "wait, this isn't lorem ipsum")
        
        self.assertIn('Successfully wrote to "lorem.txt" '
                      +'(28 characters written)', out) 
        
    def test_more_lorem(self):
        out = write_file("calculator", "pkg/morelorem.txt", 
                            "lorem ipsum dolor sit amet")
        
        self.assertIn('Successfully wrote to "pkg/morelorem.txt" '
                      +'(26 characters written)', out)
        
    def test_write_error(self):
        out = write_file("calculator", "/tmp/temp.txt", 
                            "this should not be allowed")
        
        self.assertIn('Error: Cannot write to "/tmp/temp.txt" '
                      +'as it is outside the permitted working directory', out)
        
    def test_run_calculator_maih(self):
        out = run_python_file("calculator", "main.py")
        self.assertIn('STDOUT:\nCalculator App\nUsage: python main.py "<expression>"\nExample: python main.py "3 + 5"\nSTDERR:\n', out)
        
    def test_run_nonexistent(self):
        out = run_python_file("calculator", "nonexistent.py")
        self.assertIn('Error: File "nonexistent.py" not found.', out)
        
    def test_run_outside(self):
        out = run_python_file("calculator", "../main.py")
        self.assertIn('Error: Cannot execute "../main.py" as it is outside the permitted working directory', out)

if __name__ == "__main__":
    unittest.main()