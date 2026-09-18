import unittest
import tempfile
import shutil
import os
from unittest.mock import patch, MagicMock

from core.project import Project

class TestProjectFileTraversal(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        # Create dummy project structure
        self.src_dir = os.path.join(self.test_dir, "src", "java")
        os.makedirs(self.src_dir, exist_ok=True)

        self.libs_dir = os.path.join(self.test_dir, ".libs")
        os.makedirs(self.libs_dir, exist_ok=True)

        # Create java files
        self.java_file1 = os.path.join(self.src_dir, "Main.java")
        open(self.java_file1, "w").close()

        self.sub_dir = os.path.join(self.src_dir, "sub")
        os.makedirs(self.sub_dir, exist_ok=True)
        self.java_file2 = os.path.join(self.sub_dir, "Utils.java")
        open(self.java_file2, "w").close()

        self.kt_file = os.path.join(self.sub_dir, "App.kt")
        open(self.kt_file, "w").close()

        # Create lib structure
        self.lib1 = os.path.join(self.libs_dir, "lib1")
        os.makedirs(self.lib1, exist_ok=True)
        self.jar1 = os.path.join(self.lib1, "lib1.jar")
        open(self.jar1, "w").close()

        self.manifest1 = os.path.join(self.lib1, "AndroidManifest.xml")
        with open(self.manifest1, "w") as f:
            f.write('<manifest package="com.example.lib1"/>')

        self.lib2 = os.path.join(self.libs_dir, "lib2")
        os.makedirs(self.lib2, exist_ok=True)
        self.lint_jar = os.path.join(self.lib2, "lint.jar")
        open(self.lint_jar, "w").close()

        self.manifest2 = os.path.join(self.lib2, "AndroidManifest.xml")
        with open(self.manifest2, "w") as f:
            f.write('<manifest package="com.example.lib2"/>')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("core.project.Project.__init__", return_value=None)
    def test_find_files(self, mock_init):
        proj = Project.__new__(Project)
        proj.sources_dir = self.src_dir

        java_files = proj.find_java_files()
        self.assertEqual(sorted(java_files), sorted([self.java_file1, self.java_file2]))

        kt_files = proj.find_kotlin_files()
        self.assertEqual(kt_files, [self.kt_file])

    @patch("core.project.Project.__init__", return_value=None)
    def test_find_lib_jars(self, mock_init):
        proj = Project.__new__(Project)
        proj.libs_dir = self.libs_dir

        jars = proj.find_lib_jars()
        self.assertEqual(jars, [self.jar1])

    @patch("core.project.Project.__init__", return_value=None)
    def test_get_lib_package_names(self, mock_init):
        proj = Project.__new__(Project)
        proj.libs_dir = self.libs_dir

        packages = proj.get_lib_package_names()
        self.assertEqual(packages, "com.example.lib1:com.example.lib2")


if __name__ == "__main__":
    unittest.main()
