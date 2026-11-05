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

    def test_lru_caching(self):
        get_bin.cache_clear()
        cmd_is_available.cache_clear()

        # Initial call - cache miss
        info_before = get_bin.cache_info()
        get_bin("python3")
        info_after_first = get_bin.cache_info()
        self.assertEqual(info_after_first.misses, info_before.misses + 1)

        # Subsequent call - cache hit
        get_bin("python3")
        info_after_second = get_bin.cache_info()
        self.assertEqual(info_after_second.hits, info_after_first.hits + 1)

        # cmd_is_available caching
        cmd_before = cmd_is_available.cache_info()
        cmd_is_available("python3")
        cmd_after_first = cmd_is_available.cache_info()
        self.assertEqual(cmd_after_first.misses, cmd_before.misses + 1)

        cmd_is_available("python3")
        cmd_after_second = cmd_is_available.cache_info()
        self.assertEqual(cmd_after_second.hits, cmd_after_first.hits + 1)

if __name__ == "__main__":
    unittest.main()
