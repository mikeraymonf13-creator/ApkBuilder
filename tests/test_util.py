import unittest
import shutil
from utils.util import cmd_is_available, get_bin, get_logger

class TestUtil(unittest.TestCase):
    def test_cmd_is_available(self):
        # Python binary or ls should be available in test environment
        self.assertTrue(cmd_is_available("python3") or cmd_is_available("python") or cmd_is_available("ls"))
        self.assertFalse(cmd_is_available("non_existent_binary_12345_xyz"))

    def test_get_bin(self):
        python_bin = get_bin("python3") or get_bin("python")
        self.assertIsNotNone(python_bin)
        self.assertIsNone(get_bin("non_existent_binary_12345_xyz"))

    def test_get_logger(self):
        logger = get_logger()
        self.assertIsNotNone(logger)

if __name__ == "__main__":
    unittest.main()
