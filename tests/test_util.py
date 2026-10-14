import os
import sys
import unittest
from utils.util import cmd_is_available, get_bin

class TestUtil(unittest.TestCase):
    def test_cmd_is_available_true_for_existing_bin(self):
        self.assertTrue(cmd_is_available("python3"))

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

    def test_get_bin_caching(self):
        from utils.util import _bin_cache
        bin_name = "python3"
        path1 = get_bin(bin_name)
        self.assertIn(bin_name, _bin_cache)
        self.assertEqual(_bin_cache[bin_name], path1)

        path2 = get_bin(bin_name)
        self.assertEqual(path1, path2)

    def test_cmd_is_available_caching(self):
        from utils.util import _cmd_availability_cache
        bin_name = "python3"
        result1 = cmd_is_available(bin_name)
        self.assertIn(bin_name, _cmd_availability_cache)
        self.assertTrue(result1)

        result2 = cmd_is_available(bin_name)
        self.assertEqual(result1, result2)

if __name__ == "__main__":
    unittest.main()
