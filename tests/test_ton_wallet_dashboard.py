import os
import unittest

class TestTonWalletDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "ton-wallet-dashboard",
            "index.html"
        )
        with open(self.dashboard_path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_copy_button_and_aria_attributes(self):
        self.assertIn('id="copy-btn"', self.html)
        self.assertIn('aria-label="Copy wallet address"', self.html)
        self.assertIn('onclick="copyAddress()"', self.html)

    def test_focus_visible_keyboard_accessibility(self):
        self.assertIn(':focus-visible', self.html)

    def test_aria_live_polite_status_regions(self):
        self.assertIn('id="balance" class="balance" aria-live="polite"', self.html)
        self.assertIn('id="activity" class="muted" aria-live="polite"', self.html)

    def test_copy_address_logic_and_feedback(self):
        self.assertIn('navigator.clipboard.writeText', self.html)
        self.assertIn('✓ Copied', self.html)
        self.assertIn('Wallet address copied', self.html)

if __name__ == '__main__':
    unittest.main()
