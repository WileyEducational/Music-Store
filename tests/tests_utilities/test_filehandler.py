import os
import shutil
import tempfile
import unittest
from main.utilities.FileHandler import FileHandler

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test2.txt")
        with open(self.temp_file, "w") as f:
            f.write("Test data")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_uploaded_file_path(self):
        file_path = "/path/to/test2.txt"
        expected_upload_path = os.path.join(FileHandler.uploads_folder, "test2.txt")
        self.assertEqual(FileHandler.uploaded_file_path(file_path), expected_upload_path)

    def test_copy_file_to_uploads(self):
        upload_path = FileHandler.copy_file_to_uploads(self.temp_file)
        self.assertTrue(os.path.exists(upload_path))
        self.assertTrue(os.path.isfile(upload_path))

    def test_copy_file_to_uploads_existing(self):
        with open(os.path.join(FileHandler.uploads_folder, "test2.txt"), "w") as f:
            f.write("Existing data")
        with self.assertRaises(FileExistsError):
            FileHandler.copy_file_to_uploads(self.temp_file)

    def test_replace_file(self):
        existing_file_path = os.path.join(FileHandler.uploads_folder, "existing.txt")
        with open(existing_file_path, "w") as f:
            f.write("Existing data")
        FileHandler.replace_file(existing_file_path, self.temp_file)
        with open(existing_file_path, "r") as f:
            self.assertEqual(f.read(), "Test data")

    def test_replace_file_nonexistent(self):
        with self.assertRaises(FileNotFoundError):
            FileHandler.replace_file("/nonexistent/file.txt", self.temp_file)

if __name__ == "__main__":
    unittest.main()
