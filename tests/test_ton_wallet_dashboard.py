import os
import unittest

class TestTonWalletDashboard(unittest.TestCase):
    def setUp(self):
        self.html_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "ton-wallet-dashboard", "index.html"
        ))
        with open(self.html_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_copy_button_and_accessibility(self):
        self.assertIn('id="copyAddressBtn"', self.content)
        self.assertIn('aria-label="Copy wallet address"', self.content)
        self.assertIn('button:focus-visible', self.content)
        self.assertIn('copyWalletAddress()', self.content)
        self.assertIn('aria-live="polite"', self.content)
        self.assertIn('✓ Copied', self.content)

if __name__ == "__main__":
    unittest.main()
