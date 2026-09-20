import unittest
import sys
from utils.util import cmd_is_available, get_bin, get_logger

class TestUtils(unittest.TestCase):
    def test_cmd_is_available_existing(self):
        # 'python' or 'python3' or 'ls' should be available
        python_bin = sys.executable
        self.assertTrue(cmd_is_available(python_bin))

    def test_cmd_is_available_non_existing(self):
        self.assertFalse(cmd_is_available("non_existent_command_xyz_123"))

    def test_get_bin(self):
        self.assertIsNotNone(get_bin(sys.executable))
        self.assertIsNone(get_bin("non_existent_command_xyz_123"))

    def test_get_logger(self):
        logger = get_logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "builder")

if __name__ == "__main__":
    unittest.main()
