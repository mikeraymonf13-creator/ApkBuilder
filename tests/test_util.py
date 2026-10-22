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

    def test_caching_behavior(self):
        get_bin.cache_clear()
        cmd_is_available.cache_clear()

        info1_bin = get_bin.cache_info()
        self.assertEqual(info1_bin.hits, 0)

        # First call hits original function
        get_bin("python3")
        info2_bin = get_bin.cache_info()
        self.assertEqual(info2_bin.hits, 0)
        self.assertEqual(info2_bin.misses, 1)

        # Second call hits cache
        get_bin("python3")
        info3_bin = get_bin.cache_info()
        self.assertEqual(info3_bin.hits, 1)

        # First call to cmd_is_available uses get_bin ("python3") which hits get_bin cache
        cmd_is_available("python3")
        # Second call hits cmd_is_available cache
        cmd_is_available("python3")
        info_cmd = cmd_is_available.cache_info()
        self.assertEqual(info_cmd.hits, 1)

if __name__ == "__main__":
    unittest.main()
