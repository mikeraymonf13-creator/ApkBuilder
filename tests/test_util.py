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
        self.assertTrue(cmd_is_available("python3"))
        info1 = cmd_is_available.cache_info()
        self.assertEqual(info1.hits, 0)
        self.assertEqual(info1.misses, 1)

        self.assertTrue(cmd_is_available("python3"))
        info2 = cmd_is_available.cache_info()
        self.assertEqual(info2.hits, 1)

    def test_snake_to_camel_caching(self):
        from core.binding.resolver import snake_to_camel
        snake_to_camel.cache_clear()

        res1 = snake_to_camel("main_layout_container")
        self.assertEqual(res1, "mainLayoutContainer")
        info1 = snake_to_camel.cache_info()
        self.assertEqual(info1.hits, 0)
        self.assertEqual(info1.misses, 1)

        res2 = snake_to_camel("main_layout_container")
        self.assertEqual(res2, "mainLayoutContainer")
        info2 = snake_to_camel.cache_info()
        self.assertEqual(info2.hits, 1)

if __name__ == "__main__":
    unittest.main()
