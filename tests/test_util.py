import unittest
from utils.util import cmd_is_available, get_bin

class TestUtils(unittest.TestCase):
    def test_cmd_is_available_existing(self):
        # python3 should always exist in the test environment
        self.assertTrue(cmd_is_available("python3"))

    def test_cmd_is_available_nonexistent(self):
        # non-existent command should return False
        self.assertFalse(cmd_is_available("non_existent_binary_xyz_12345"))

    def test_get_bin(self):
        self.assertIsNotNone(get_bin("python3"))
        self.assertIsNone(get_bin("non_existent_binary_xyz_12345"))

if __name__ == "__main__":
    unittest.main()
