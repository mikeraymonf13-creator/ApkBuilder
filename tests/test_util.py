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

    def test_lru_cache_util_functions(self):
        # Clear cache before test
        get_bin.cache_clear()
        cmd_is_available.cache_clear()

        # Call get_bin twice
        res1 = get_bin("python3")
        res2 = get_bin("python3")
        self.assertEqual(res1, res2)
        info = get_bin.cache_info()
        self.assertGreaterEqual(info.hits, 1)

        # Call cmd_is_available twice
        cmd_is_available("python3")
        cmd_is_available("python3")
        info_cmd = cmd_is_available.cache_info()
        self.assertGreaterEqual(info_cmd.hits, 1)

if __name__ == "__main__":
    unittest.main()
