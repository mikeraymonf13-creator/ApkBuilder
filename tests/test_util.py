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

    def test_cmd_is_available_caching(self):
        cmd_is_available.cache_clear()
        initial_hits = cmd_is_available.cache_info().hits

        # First call: cache miss
        res1 = cmd_is_available("python3")
        self.assertTrue(res1)

        # Second call: cache hit
        res2 = cmd_is_available("python3")
        self.assertTrue(res2)

        self.assertGreater(cmd_is_available.cache_info().hits, initial_hits)

if __name__ == "__main__":
    unittest.main()
