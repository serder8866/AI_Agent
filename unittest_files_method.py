import unittest
from functions.get_files_info import get_files_info

class TestFilesMethods(unittest.TestCase):
    
    def test_get_files_info(self):
        self.assertEqual(get_files_info("calculator", "."), "- main.py: file_size=719 bytes, is_dir=False\n- tests.py: file_size=1331 bytes, is_dir=False\n- pkg: file_size=44 bytes, is_dir=True")
        self.assertEqual(get_files_info("calculator", "pkg"), "- calculator.py: file_size=1721 bytes, is_dir=False\n- render.py: file_size=376 bytes, is_dir=False")
        self.assertEqual(get_files_info("calculator", "/bin"), "Error: Cannot list '/bin' as it is outside the permitted working directory")
        self.assertEqual(get_files_info("calculator", "../"), "Error: Cannot list '../' as it is outside the permitted working directory")

if __name__ == "__main__":
    unittest.main()