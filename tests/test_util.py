import unittest
from utils.util import cmd_is_available

class TestUtil(unittest.TestCase):
    def test_cmd_is_available_true(self):
        # python3 should always be available in the test environment
        self.assertTrue(cmd_is_available("python3"))

    def test_cmd_is_available_false(self):
        # A non-existent command should return False
        self.assertFalse(cmd_is_available("non_existent_command_12345"))

if __name__ == "__main__":
    unittest.main()
