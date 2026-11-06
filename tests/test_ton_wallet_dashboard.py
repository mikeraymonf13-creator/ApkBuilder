import os
import unittest

class TestTonWalletDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "ton-wallet-dashboard", "index.html")
        )
        self.assertTrue(os.path.exists(self.dashboard_path), "ton-wallet-dashboard/index.html must exist")
        with open(self.dashboard_path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_accessible_copy_button(self):
        self.assertIn('id="copy-btn"', self.html)
        self.assertIn('aria-label="Copy wallet address"', self.html)
        self.assertIn('copyAddress()', self.html)
        self.assertIn('Wallet address copied', self.html)

    def test_accessibility_live_region(self):
        self.assertIn('id="activity"', self.html)
        self.assertIn('aria-live="polite"', self.html)

    def test_keyboard_focus_styling(self):
        self.assertIn('button:focus-visible', self.html)

if __name__ == '__main__':
    unittest.main()
