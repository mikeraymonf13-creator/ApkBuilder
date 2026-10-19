import os
import sys
import unittest
from utils.util import cmd_is_available, get_bin, _cmd_availability_cache

class TestUtil(unittest.TestCase):
    def test_cmd_is_available_true_for_existing_bin(self):
        self.assertTrue(cmd_is_available("python3"))

    def test_cmd_is_available_caching(self):
        test_bin = "python3_test_cache_entry"
        _cmd_availability_cache.pop(test_bin, None)

        self.assertNotIn(test_bin, _cmd_availability_cache)
        res1 = cmd_is_available(test_bin)
        self.assertIn(test_bin, _cmd_availability_cache)

        # Manually alter cache value to verify cached result is returned
        _cmd_availability_cache[test_bin] = True
        res2 = cmd_is_available(test_bin)
        self.assertTrue(res2)

        # Clean up
        _cmd_availability_cache.pop(test_bin, None)

    def test_cmd_is_available_false_for_nonexistent_bin(self):
        self.assertFalse(cmd_is_available("nonexistent_binary_xyz_12345"))

    def test_cmd_is_available_explicit_path(self):
        python_executable = sys.executable
        self.assertTrue(cmd_is_available(python_executable))
        self.assertFalse(cmd_is_available("/tmp/non_existent_binary_path_xyz"))

    def test_get_bin(self):
        path = get_bin("python3")
        self.assertIsNotNone(path)
        self.assertTrue(path.endswith("python3"))

if __name__ == "__main__":
    unittest.main()
