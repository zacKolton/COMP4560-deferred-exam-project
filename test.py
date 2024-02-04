import unittest
from unittest.mock import patch
import os
import tempfile
import shutil
from main import copy_file_to_downloads  # Adjust the import if your filename differs

class TestCopyFileToDownloads(unittest.TestCase):
    def setUp(self):
        # Setup a temporary directory to simulate the user's home directory
        self.home_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.home_dir)

    @patch('os.path.expanduser')
    @patch('shutil.copy')
    def test_copy_file_to_downloads(self, mock_copy, mock_expanduser):
        # Mock the expanduser function to return the path to the temporary directory
        mock_expanduser.return_value = self.home_dir

        # Simulate the Downloads folder within the temporary home directory
        downloads_path = os.path.join(self.home_dir, 'Downloads')
        os.makedirs(downloads_path)  # Ensure the Downloads directory exists

        # Test the function with a dummy file path
        file_path = "/path/to/source/file.xlsx"
        new_file_name = "data.xlsx"
        expected_new_file_path = os.path.join(downloads_path, new_file_name)

        result = copy_file_to_downloads(file_path, new_file_name)
        
        # Verify the file was copied to the correct location
        self.assertEqual(result, expected_new_file_path)
        mock_copy.assert_called_once_with(file_path, expected_new_file_path)

if __name__ == '__main__':
    unittest.main()