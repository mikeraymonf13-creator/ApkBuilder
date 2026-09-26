import unittest
from unittest.mock import patch
from utils.util import cmd_is_available

class TestUtil(unittest.TestCase):
    @patch("shutil.which")
    def test_cmd_is_available_true(self, mock_which):
        mock_which.return_value = "/usr/bin/javac"
        self.assertTrue(cmd_is_available("javac"))
        mock_which.assert_called_once_with("javac")

    @patch("shutil.which")
    def test_cmd_is_available_false(self, mock_which):
        mock_which.return_value = None
        self.assertFalse(cmd_is_available("nonexistent_binary"))
        mock_which.assert_called_once_with("nonexistent_binary")

if __name__ == "__main__":
    unittest.main()
