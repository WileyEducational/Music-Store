import unittest
import os
from main.utilities.Checksum import ChecksumUtility

def create_test_file(file_path):
    with open(file_path, 'w') as f:
        f.write('This is a test file.')

def remove_test_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

class TestChecksumUtility(unittest.TestCase):
    def setUp(self):
        self.test_file_path = 'test_file.txt'
        create_test_file(self.test_file_path)

    def tearDown(self):
        remove_test_file(self.test_file_path)

    def test_calculate_checksum(self):
        expected_checksum = 'f29bc64a9d3732b4b9035125fdb3285f5b6455778edca72414671e0ca3b2e0de'
        actual_checksum = ChecksumUtility.calculate_checksum(self.test_file_path)
        self.assertEqual(actual_checksum, expected_checksum)

if __name__ == '__main__':
    unittest.main()
