"""Tests for drive_client module"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import tempfile
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.drive_client import DriveClient
from test.mocks.mock_drive import MockGoogleDriveService

class TestDriveClient(unittest.TestCase):
    
    def setUp(self):
        """Setup test environment"""
        self.test_content = "Test file content for Drive upload"
        self.test_filename = "test_file.txt"
        self.test_folder_id = "test_folder_123"
        
    def test_init_local_mode(self):
        """Test DriveClient initialization in local mode (no credentials)"""
        client = DriveClient()
        self.assertTrue(client.mock_mode)
        self.assertIsNone(client.service)
        
    @patch('src.drive_client.build')
    @patch('src.drive_client.Credentials')
    @patch('os.path.exists')
    def test_init_google_mode(self, mock_exists, mock_credentials, mock_build):
        """Test DriveClient initialization with Google credentials"""
        # Setup mocks
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_credentials.from_authorized_user_file.return_value = mock_creds
        mock_service = MockGoogleDriveService()
        mock_build.return_value = mock_service
        
        client = DriveClient()
        
        # Should be in Google mode
        self.assertFalse(client.mock_mode)
        self.assertIsNotNone(client.service)
        
    def test_upload_string_local_mode(self):
        """Test uploading string in local mode"""
        client = DriveClient()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test upload - correct API: upload_string(data, name, parent_id)
            result = client.upload_string(
                data=self.test_content,
                name=self.test_filename, 
                parent_id=temp_dir
            )
            
            # Check file was created
            expected_path = os.path.join(temp_dir, self.test_filename)
            self.assertTrue(os.path.exists(expected_path))
            
            # Check content
            with open(expected_path, 'r', encoding='utf-8') as f:
                self.assertEqual(f.read(), self.test_content)
                
            # upload_string returns None in mock mode
            self.assertIsNone(result)
            
    @patch('src.drive_client.build')
    @patch('src.drive_client.Credentials')
    @patch('os.path.exists')
    def test_upload_string_google_mode(self, mock_exists, mock_credentials, mock_build):
        """Test uploading string in Google Drive mode"""
        # Setup mocks for Google mode
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_credentials.from_authorized_user_file.return_value = mock_creds
        mock_service = MockGoogleDriveService()
        mock_build.return_value = mock_service
        
        client = DriveClient()
        
        # Test upload - correct API
        result = client.upload_string(
            data=self.test_content,
            name=self.test_filename,
            parent_id=self.test_folder_id
        )
        
        # Check that file was "uploaded" (mocked)
        self.assertEqual(len(mock_service.files_mock.created_files), 1)
        self.assertEqual(mock_service.files_mock.created_files[0].name, self.test_filename)
        
    def test_create_local_folder(self):
        """Test creating local folder via upload_string"""
        client = DriveClient()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = os.path.join(temp_dir, "subfolder")
            
            # DriveClient doesn't have public create_folder, but upload_string creates dirs
            client.upload_string(
                data="test content",
                name="test.txt", 
                parent_id=nested_path
            )
            
            # Check folder and file were created
            self.assertTrue(os.path.exists(nested_path))
            self.assertTrue(os.path.isdir(nested_path))
            test_file = os.path.join(nested_path, "test.txt")
            self.assertTrue(os.path.exists(test_file))
            
    def test_upload_string_creates_directory(self):
        """Test that upload_string creates directory if it doesn't exist"""
        client = DriveClient()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = os.path.join(temp_dir, "nested", "folder", "structure")
            
            # Upload to non-existent directory
            result = client.upload_string(
                data=self.test_content,
                name=self.test_filename,
                parent_id=nested_path
            )
            
            # Check directory was created
            self.assertTrue(os.path.exists(nested_path))
            self.assertTrue(os.path.isdir(nested_path))
            
            # Check file was created
            expected_file = os.path.join(nested_path, self.test_filename)
            self.assertTrue(os.path.exists(expected_file))
            
    def test_upload_string_overwrites_existing(self):
        """Test that upload_string overwrites existing files"""
        client = DriveClient()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, self.test_filename)
            
            # Create initial file
            with open(file_path, 'w') as f:
                f.write("Original content")
                
            # Upload new content
            client.upload_string(
                data=self.test_content,
                name=self.test_filename,
                parent_id=temp_dir
            )
            
            # Check content was overwritten
            with open(file_path, 'r', encoding='utf-8') as f:
                self.assertEqual(f.read(), self.test_content)
                
    def test_upload_string_empty_content(self):
        """Test uploading empty string"""
        client = DriveClient()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            result = client.upload_string(
                data="",
                name=self.test_filename,
                parent_id=temp_dir
            )
            
            # Check empty file was created
            file_path = os.path.join(temp_dir, self.test_filename)
            self.assertTrue(os.path.exists(file_path))
            
            with open(file_path, 'r') as f:
                self.assertEqual(f.read(), "")
                
    def test_upload_string_unicode_content(self):
        """Test uploading Unicode content"""
        client = DriveClient()
        unicode_content = "Test with émojis 🚀 and čeština ř"
        
        with tempfile.TemporaryDirectory() as temp_dir:
            client.upload_string(
                data=unicode_content,
                name=self.test_filename,
                parent_id=temp_dir  
            )
            
            # Check Unicode content is preserved
            file_path = os.path.join(temp_dir, self.test_filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                self.assertEqual(f.read(), unicode_content)
                
    @patch('src.drive_client.build')
    @patch('src.drive_client.Credentials')  
    @patch('os.path.exists')
    def test_google_drive_authentication_error(self, mock_exists, mock_credentials, mock_build):
        """Test handling of Google Drive authentication errors"""
        # Setup mocks to simulate auth error
        mock_exists.return_value = True
        mock_credentials.from_authorized_user_file.side_effect = Exception("Auth error")
        
        # Should fall back to local mode
        client = DriveClient()
        self.assertTrue(client.mock_mode)
        
    def test_print_local_mode_warning(self):
        """Test that local mode warning is printed"""
        with patch('builtins.print') as mock_print:
            DriveClient()
            mock_print.assert_called_with("⚠️ client_secret.json nenalezen - používám lokální mock místo Google Drive")

if __name__ == '__main__':
    unittest.main()
