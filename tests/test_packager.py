import os
import tempfile
import zipfile
import unittest
from unittest.mock import patch
from core.project import Project
from core.packager import Task as PackagerTask

class TestPackager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = self.temp_dir.name

        with open(os.path.join(self.project_dir, "project.yml"), "w") as f:
            f.write("""
bins:
    aapt2: /usr/bin/stub
    javac: /usr/bin/stub
    kotlinc: /usr/bin/stub
    d8: /usr/bin/stub
    apksigner: /usr/bin/stub

android:
    sdk-api-version: 34
    sdk-min-api-version: 21
    version-code: 1
    version-name: "1"
    build-type: debug
    keystore-path: test.keystore
    keystore-alias: test
    keystore-store-pass: pass
    keystore-key-pass: pass
""")

        os.makedirs(os.path.join(self.project_dir, "src", "java"), exist_ok=True)
        with open(os.path.join(self.project_dir, "AndroidManifest.xml"), "w") as f:
            f.write('<manifest package="com.example.test"></manifest>')
        with open(os.path.join(self.project_dir, "test.keystore"), "w") as f:
            f.write("dummy keystore")

        # Mock bin directory and gen.apk.res
        self.proj = Project(self.project_dir)
        os.makedirs(self.proj.bin_dir, exist_ok=True)
        with zipfile.ZipFile(os.path.join(self.proj.bin_dir, "gen.apk.res"), "w") as z:
            z.writestr("AndroidManifest.xml", "dummy manifest")

        # Create main dex file
        os.makedirs(self.proj.dex_dir, exist_ok=True)
        with open(os.path.join(self.proj.dex_dir, "classes.dex"), "wb") as f:
            f.write(b"dex_main_content")

        # Create library with dex file
        self.lib_dir = os.path.join(self.proj.libs_dir, "test_lib")
        os.makedirs(self.lib_dir, exist_ok=True)
        with open(os.path.join(self.lib_dir, "classes.jar"), "w") as f:
            f.write("jar")
        with open(os.path.join(self.lib_dir, "classes.dex"), "wb") as f:
            f.write(b"dex_lib_content")

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("core.packager.cmd_is_available", return_value=True)
    @patch("core.packager.run")
    @patch("os.remove")
    def test_dex_files_stored_uncompressed(self, mock_remove, mock_run, mock_cmd_avail):
        task = PackagerTask(self.proj)
        task.start()

        unsigned_apk = os.path.join(self.proj.bin_dir, "unsigned.apk")
        self.assertTrue(os.path.isfile(unsigned_apk))

        with zipfile.ZipFile(unsigned_apk, "r") as apk:
            entries = {info.filename: info.compress_type for info in apk.infolist()}
            self.assertIn("classes.dex", entries)
            self.assertIn("classes2.dex", entries)
            # Verify both primary and library DEX files are uncompressed (ZIP_STORED = 0)
            self.assertEqual(entries["classes.dex"], zipfile.ZIP_STORED)
            self.assertEqual(entries["classes2.dex"], zipfile.ZIP_STORED)

if __name__ == "__main__":
    unittest.main()
