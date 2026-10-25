import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from core.project import Project

class TestProjectCaching(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = self.temp_dir.name

        # Create minimal project structure
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

        manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.test">
</manifest>
"""
        with open(os.path.join(self.project_dir, "AndroidManifest.xml"), "w") as f:
            f.write(manifest_content)

        # Create keystore stub
        with open(os.path.join(self.project_dir, "test.keystore"), "w") as f:
            f.write("dummy keystore")

        # Create libs directory with dummy jar and manifest
        self.libs_dir = os.path.join(self.project_dir, ".libs")
        lib1_dir = os.path.join(self.libs_dir, "lib1")
        os.makedirs(lib1_dir, exist_ok=True)
        with open(os.path.join(lib1_dir, "classes.jar"), "w") as f:
            f.write("dummy jar")
        with open(os.path.join(lib1_dir, "AndroidManifest.xml"), "w") as f:
            f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.example.lib1">
</manifest>""")

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_find_lib_jars_caching(self, mock_getenv, mock_get_bin):
        proj = Project(self.project_dir)

        # First call populates cache
        jars1 = proj.find_lib_jars()
        self.assertEqual(len(jars1), 1)
        self.assertTrue(jars1[0].endswith("classes.jar"))
        self.assertIsNotNone(proj._cached_lib_jars)

        # Add another jar to filesystem after first call
        lib2_dir = os.path.join(self.libs_dir, "lib2")
        os.makedirs(lib2_dir, exist_ok=True)
        with open(os.path.join(lib2_dir, "classes2.jar"), "w") as f:
            f.write("dummy jar 2")

        # Second call returns cached result without re-scanning disk
        jars2 = proj.find_lib_jars()
        self.assertEqual(len(jars2), 1)
        self.assertEqual(jars1, jars2)

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_get_lib_package_names_caching(self, mock_getenv, mock_get_bin):
        proj = Project(self.project_dir)

        pkg_names1 = proj.get_lib_package_names()
        self.assertEqual(pkg_names1, "com.example.lib1")
        self.assertEqual(proj._cached_lib_package_names, "com.example.lib1")

        # Call again to verify cached return
        pkg_names2 = proj.get_lib_package_names()
        self.assertEqual(pkg_names2, "com.example.lib1")

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_find_files_nonexistent_dir(self, mock_getenv, mock_get_bin):
        proj = Project(self.project_dir)

        nonexistent = os.path.join(self.project_dir, "does_not_exist")
        result = proj.find_files(nonexistent, ".java")
        self.assertEqual(result, [])

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_find_files_nested_directories(self, mock_getenv, mock_get_bin):
        proj = Project(self.project_dir)

        nested_dir = os.path.join(self.project_dir, "src", "java", "com", "example", "app")
        os.makedirs(nested_dir, exist_ok=True)

        file_java1 = os.path.join(self.project_dir, "src", "java", "Main.java")
        file_java2 = os.path.join(nested_dir, "Activity.java")
        file_kt = os.path.join(nested_dir, "Utils.kt")

        for filepath in (file_java1, file_java2, file_kt):
            with open(filepath, "w") as f:
                f.write("// stub")

        java_files = proj.find_files(os.path.join(self.project_dir, "src", "java"), ".java")
        self.assertEqual(len(java_files), 2)
        self.assertIn(file_java1, java_files)
        self.assertIn(file_java2, java_files)
        self.assertNotIn(file_kt, java_files)

        kt_files = proj.find_files(os.path.join(self.project_dir, "src", "java"), ".kt")
        self.assertEqual(len(kt_files), 1)
        self.assertEqual(kt_files[0], file_kt)

    @patch("utils.util.get_bin", return_value=None)
    @patch("os.getenv", return_value=None)
    def test_sdk_and_bin_fallback(self, mock_getenv, mock_get_bin):
        # Create minimal yml without bins overrides
        yml_path = os.path.join(self.project_dir, "project.yml")
        with open(yml_path, "w") as f:
            f.write("""
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

        # Mock os.path.exists to simulate /opt/android-sdk and build-tools
        fake_sdk = "/opt/android-sdk"
        fake_aapt2 = os.path.join(fake_sdk, "build-tools", "35.0.0", "aapt2")

        orig_exists = os.path.exists
        orig_isfile = os.path.isfile
        orig_access = os.access
        orig_listdir = os.listdir

        def custom_exists(path):
            if path == fake_sdk or path == os.path.join(fake_sdk, "build-tools"):
                return True
            return orig_exists(path)

        def custom_listdir(path):
            if path == os.path.join(fake_sdk, "build-tools"):
                return ["35.0.0"]
            return orig_listdir(path)

        def custom_isfile(path):
            if path == fake_aapt2:
                return True
            return orig_isfile(path)

        def custom_access(path, mode):
            if path == fake_aapt2:
                return True
            return orig_access(path, mode)

        with patch("os.path.exists", side_effect=custom_exists), \
             patch("os.listdir", side_effect=custom_listdir), \
             patch("os.path.isfile", side_effect=custom_isfile), \
             patch("os.access", side_effect=custom_access):
            proj = Project(self.project_dir)
            self.assertEqual(proj.sdk_dir, fake_sdk)
            self.assertEqual(proj.bin_aapt2, fake_aapt2)
            self.assertEqual(proj._build_tools_versions, ["35.0.0"])

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_dexer_classpath_caching(self, mock_getenv, mock_get_bin):
        from core.dexer import Task as DexerTask
        proj = Project(self.project_dir)

        task = DexerTask(proj)
        self.assertIsNone(task.classpath)

        # Calling __get_classpath populates self.classpath list
        classpath1 = task._Task__get_classpath()
        self.assertIsNotNone(task.classpath)

        # Subsequent call returns cached self.classpath
        classpath2 = task._Task__get_classpath()
        self.assertIs(classpath1, classpath2)

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_find_dex_files(self, mock_getenv, mock_get_bin):
        proj = Project(self.project_dir)

        # Before dex_dir is created, find_dex_files should return empty list
        self.assertEqual(proj.find_dex_files(), [])

        # Create dex_dir and add .dex files as well as non-.dex files
        os.makedirs(proj.dex_dir, exist_ok=True)
        classes_dex = os.path.join(proj.dex_dir, "classes.dex")
        classes2_dex = os.path.join(proj.dex_dir, "classes2.dex")
        other_file = os.path.join(proj.dex_dir, "other.txt")

        with open(classes_dex, "w") as f:
            f.write("dex data 1")
        with open(classes2_dex, "w") as f:
            f.write("dex data 2")
        with open(other_file, "w") as f:
            f.write("text data")

        dex_files = proj.find_dex_files()
        self.assertEqual(len(dex_files), 2)
        self.assertIn(classes_dex, dex_files)
        self.assertIn(classes2_dex, dex_files)
        self.assertNotIn(other_file, dex_files)

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_find_native_libs(self, mock_getenv, mock_get_bin):
        proj = Project(self.project_dir)

        # Before creating native libs directory, find_native_libs returns empty list
        self.assertEqual(proj.find_native_libs(), [])

        # Create arm64-v8a and armeabi-v7a native libraries
        arm64_dir = os.path.join(proj.native_libs_dir, "arm64-v8a")
        os.makedirs(arm64_dir, exist_ok=True)
        so_file = os.path.join(arm64_dir, "libexample.so")
        with open(so_file, "w") as f:
            f.write("dummy so file")

        libs = proj.find_native_libs()
        self.assertEqual(len(libs), 1)
        abi, path = libs[0]
        self.assertEqual(abi, "arm64-v8a")
        self.assertEqual(path, so_file)

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_view_binding_generator(self, mock_getenv, mock_get_bin):
        from core.binding.generator import GenerateViewBinding
        proj = Project(self.project_dir)

        # When layout directory does not exist, GenerateViewBinding.start should return gracefully
        gen_task = GenerateViewBinding(proj)
        gen_task.start()

        # Create layout directory and a sample layout XML file
        layout_dir = os.path.join(proj.res_dir, "layout")
        os.makedirs(layout_dir, exist_ok=True)
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:id="@+id/main_layout"
    android:layout_width="match_parent"
    android:layout_height="match_parent">
    <TextView
        android:id="@+id/title_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
</LinearLayout>"""
        with open(os.path.join(layout_dir, "activity_main.xml"), "w") as f:
            f.write(xml_content)

        gen_task.start()

        expected_binding_file = os.path.join(
            proj.view_binding_dir,
            "com", "example", "test", "databinding",
            "ActivityMainBinding.java"
        )
        self.assertTrue(os.path.isfile(expected_binding_file))

    @patch("utils.util.get_bin", return_value="/usr/bin/stub")
    @patch("os.getenv", return_value="/tmp/android-sdk")
    def test_multi_jar_library_deduplication(self, mock_getenv, mock_get_bin):
        from core.resources import Aapt2Task
        from core.packager import Task as PackagerTask
        import zipfile

        # Add a second jar in lib1 directory
        lib1_dir = os.path.join(self.libs_dir, "lib1")
        with open(os.path.join(lib1_dir, "extra.jar"), "w") as f:
            f.write("extra jar content")

        proj = Project(self.project_dir)
        jars = proj.find_lib_jars()
        self.assertEqual(len(jars), 2)  # classes.jar and extra.jar in lib1_dir

        # Test Aapt2Task prepare deduplication
        aapt_task = Aapt2Task(proj)
        with patch("core.resources.cmd_is_available", return_value=True):
            aapt_task.prepare()
            # self.libs_to_compile should contain only 1 entry for lib1 directory
            self.assertEqual(len(aapt_task.libs_to_compile), 1)

        # Test Packager Task library dex deduplication
        # Create a dex file in lib1
        dex_in_lib1 = os.path.join(lib1_dir, "classes.dex")
        with open(dex_in_lib1, "w") as f:
            f.write("dex payload")

        # Create main dex file in project dex_dir
        os.makedirs(proj.dex_dir, exist_ok=True)
        with open(os.path.join(proj.dex_dir, "classes.dex"), "w") as f:
            f.write("main dex payload")

        # Create dummy gen.apk.res in bin_dir
        os.makedirs(proj.bin_dir, exist_ok=True)
        res_apk = os.path.join(proj.bin_dir, "gen.apk.res")
        with zipfile.ZipFile(res_apk, "w") as z:
            z.writestr("AndroidManifest.xml", "dummy manifest")

        packager_task = PackagerTask(proj)
        with patch.object(packager_task, "_Task__sign_apk") as mock_sign:
            packager_task.start()

            unsigned_apk = os.path.join(proj.bin_dir, "unsigned.apk")
            with zipfile.ZipFile(unsigned_apk, "r") as z:
                namelist = z.namelist()
                # Should contain classes.dex and classes2.dex (lib1 dex added ONCE, not twice)
                self.assertIn("classes.dex", namelist)
                self.assertIn("classes2.dex", namelist)
                self.assertNotIn("classes3.dex", namelist)

if __name__ == "__main__":
    unittest.main()
