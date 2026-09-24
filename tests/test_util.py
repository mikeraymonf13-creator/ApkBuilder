import unittest
from utils.util import cmd_is_available

class TestUtil(unittest.TestCase):
    def test_cmd_is_available_existing(self):
        # python3 should exist in the test environment
        self.assertTrue(cmd_is_available("python3"))

    def test_cmd_is_available_nonexistent(self):
        self.assertFalse(cmd_is_available("nonexistent_command_xyz_12345"))

    def test_cmd_is_available_caching(self):
        cmd_is_available.cache_clear()
        initial_hits = cmd_is_available.cache_info().hits

        # First call: cache miss
        res1 = cmd_is_available("python3")
        # Second call: cache hit
        res2 = cmd_is_available("python3")

        self.assertEqual(res1, res2)
        self.assertGreater(cmd_is_available.cache_info().hits, initial_hits)

if __name__ == "__main__":
    unittest.main()
