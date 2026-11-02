import os
import unittest

class TestTonWalletDashboard(unittest.TestCase):
    def setUp(self):
        self.html_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "ton-wallet-dashboard", "index.html")
        )

    def test_ton_wallet_dashboard_concurrent_fetching(self):
        self.assertTrue(os.path.isfile(self.html_path))
        with open(self.html_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Verify Promise.all concurrency optimization
        self.assertIn("Promise.all", content)
        self.assertIn("fetch('/api/ton/account/' + encodedAddr)", content)
        self.assertIn("fetch('/api/ton/transactions/' + encodedAddr)", content)

        # Verify elements and handlers
        self.assertIn("id=\"balance\"", content)
        self.assertIn("id=\"activity\"", content)
        self.assertIn("loadTonData(address)", content)

if __name__ == "__main__":
    unittest.main()
