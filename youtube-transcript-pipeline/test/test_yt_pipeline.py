"""Tests for yt_pipeline module"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
import json
import tempfile
import subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.yt_pipeline import (
    extract_video_id, get_basic_meta, fetch_transcript, 
    clean_text_from_segments, run_for_url, slugify_title, slugify_path_segment
)
from src.drive_client import DriveClient
from test.mocks.mock_youtube import MockTranscriptSegment

class TestYTPipeline(unittest.TestCase):
    
    def setUp(self):
        """Setup test environment"""
        # Load test fixtures
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
        with open(os.path.join(fixtures_dir, 'sample_transcript.json'), 'r') as f:
            self.sample_transcript = json.load(f)
            
        with open(os.path.join(fixtures_dir, 'sample_metadata.json'), 'r') as f:
            self.sample_metadata = json.load(f)
            
        with open(os.path.join(fixtures_dir, 'sample_llm_response.md'), 'r') as f:
            self.sample_llm_response = f.read()
            
    def test_extract_video_id_youtube_com(self):
        """Test extracting video ID from youtube.com URLs"""
        test_cases = [
            ("https://www.youtube.com/watch?v=JU8BwMe_BWg", "JU8BwMe_BWg"),
            ("https://youtube.com/watch?v=JU8BwMe_BWg&t=123", "JU8BwMe_BWg"),
            ("http://www.youtube.com/watch?v=JU8BwMe_BWg", "JU8BwMe_BWg"),
        ]
        
        for url, expected_id in test_cases:
            with self.subTest(url=url):
                result = extract_video_id(url)
                self.assertEqual(result, expected_id)
                
    def test_extract_video_id_youtu_be(self):
        """Test extracting video ID from youtu.be URLs"""
        test_cases = [
            ("https://youtu.be/JU8BwMe_BWg", "JU8BwMe_BWg"),
            ("http://youtu.be/JU8BwMe_BWg?t=123", "JU8BwMe_BWg"),
            ("youtu.be/JU8BwMe_BWg", "JU8BwMe_BWg"),
        ]
        
        for url, expected_id in test_cases:
            with self.subTest(url=url):
                result = extract_video_id(url)
                self.assertEqual(result, expected_id)
                
    def test_extract_video_id_invalid_url(self):
        """Test extracting video ID from invalid URLs - fallback behavior"""
        # Function returns last path segment as fallback, not None
        test_cases = [
            ("https://example.com/video", "video"),
            ("not_a_url", "not_a_url"),  # fallback to path name
            ("", ""),  # empty path name
            ("https://youtube.com/watch?v=", "watch"),  # fallback to path segment
        ]
        
        for url, expected in test_cases:
            with self.subTest(url=url):
                result = extract_video_id(url)
                self.assertEqual(result, expected)
                
    @patch('src.yt_pipeline.subprocess.run')
    def test_get_basic_meta_success(self, mock_subprocess):
        """Test successful metadata extraction"""
        # Setup mock
        mock_process = MagicMock()
        mock_process.stdout = json.dumps(self.sample_metadata)
        mock_subprocess.return_value = mock_process
        
        # Test
        result = get_basic_meta("https://youtu.be/JU8BwMe_BWg")
        
        # Assertions
        self.assertEqual(result["title"], "Advanced Claude Code Tips and Tricks")
        self.assertEqual(result["channel"], "Tech Tutorial Channel")
        self.assertEqual(result["published"], "20250823")
        self.assertEqual(result["duration"], 1234)
        
        # Check subprocess was called correctly
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]
        self.assertIn("yt-dlp", call_args)
        self.assertIn("--ignore-config", call_args)
        self.assertIn("--dump-single-json", call_args)
        self.assertIn("https://youtu.be/JU8BwMe_BWg", call_args)
        
    @patch('src.yt_pipeline.subprocess.run')
    def test_get_basic_meta_subprocess_error(self, mock_subprocess):
        """Test handling of subprocess errors"""
        # Setup mock to raise CalledProcessError
        from subprocess import CalledProcessError
        mock_subprocess.side_effect = CalledProcessError(1, 'yt-dlp', stderr="Error message")
        
        # Test should raise exception
        with self.assertRaises(CalledProcessError):
            get_basic_meta("https://youtu.be/JU8BwMe_BWg")
            
    @patch('src.yt_pipeline.YouTubeTranscriptApi')
    def test_fetch_transcript_success(self, mock_transcript_api):
        """Test successful transcript fetching"""
        # Setup mock
        mock_segments = [MockTranscriptSegment(**seg) for seg in self.sample_transcript]
        mock_transcript = MagicMock()
        mock_transcript.fetch.return_value = mock_segments
        
        # Mock transcript object
        mock_transcript.language_code = "cs"
        
        # Mock API instance
        mock_api_instance = MagicMock()
        mock_api_instance.list.return_value = [mock_transcript]
        mock_transcript_api.return_value = mock_api_instance
        
        # Test
        result = fetch_transcript("JU8BwMe_BWg", lang_priorities=("cs", "en"))
        
        # Assertions
        self.assertEqual(len(result), len(self.sample_transcript))
        self.assertEqual(result[0].text, "Welcome to this tutorial about Claude Code.")
        
    @patch('src.yt_pipeline.YouTubeTranscriptApi')
    def test_fetch_transcript_no_transcript_found(self, mock_transcript_api):
        """Test handling when no transcript is found"""
        from youtube_transcript_api import NoTranscriptFound
        # Mock API instance
        mock_api_instance = MagicMock()
        mock_api_instance.list.side_effect = NoTranscriptFound(
            "JU8BwMe_BWg", [], ""
        )
        mock_transcript_api.return_value = mock_api_instance
        
        # Test - should raise exception
        with self.assertRaises(Exception):
            fetch_transcript("JU8BwMe_BWg", lang_priorities=("cs", "en"))
        
    def test_clean_text_from_segments_with_objects(self):
        """Test cleaning text from segment objects"""
        segments = [MockTranscriptSegment(**seg) for seg in self.sample_transcript]
        
        result = clean_text_from_segments(segments)
        
        # Check result is string
        self.assertIsInstance(result, str)
        
        # Check some content is present
        self.assertIn("Welcome to this tutorial", result)
        self.assertIn("advanced features", result)
        
        # Check sentences are on separate lines (formatting feature)
        lines = result.split('\n')
        self.assertGreater(len(lines), 1)
        
    def test_clean_text_from_segments_with_dicts(self):
        """Test cleaning text from segment dictionaries"""
        result = clean_text_from_segments(self.sample_transcript)
        
        # Check result is string
        self.assertIsInstance(result, str)
        
        # Check content
        self.assertIn("Welcome to this tutorial", result)
        
    def test_clean_text_from_segments_empty(self):
        """Test cleaning text from empty segments"""
        result = clean_text_from_segments([])
        
        self.assertEqual(result, "")
        
    def test_clean_text_from_segments_mixed_types(self):
        """Test cleaning text from mixed segment types"""
        segments = [
            MockTranscriptSegment("First segment", 0.0, 2.0),
            {"text": "Second segment", "start": 2.0, "duration": 2.0},
            MockTranscriptSegment("Third segment", 4.0, 2.0),
        ]
        
        result = clean_text_from_segments(segments)
        
        self.assertIn("First segment", result)
        self.assertIn("Second segment", result)
        self.assertIn("Third segment", result)

    def test_slugify_title(self):
        """Ensure title slugging handles accents/punctuation"""
        self.assertEqual(slugify_title("Příliš žluťoučký kůň"), "prilis-zlutoucky-kun")
        self.assertEqual(slugify_title("  Hello, World!  "), "hello-world")
        self.assertEqual(slugify_title("123"), "123")
        self.assertEqual(slugify_title("!!!"), "")

    def test_slugify_path_segment(self):
        """Normalize channel/path names to ASCII kebab-case"""
        self.assertEqual(slugify_path_segment("Tech Tutorial Channel"), "tech-tutorial-channel")
        self.assertEqual(slugify_path_segment("Příliš/žluťoučký_kůň"), "prilis-zlutoucky-kun")
        self.assertEqual(slugify_path_segment("Curt Jaimungal"), "curt-jaimungal")
        self.assertEqual(slugify_path_segment("TÂCHES TEACHES"), "taches-teaches")
        self.assertEqual(slugify_path_segment("  ???  ", fallback="fallback"), "fallback")
        
    @patch('src.yt_pipeline.analyze_text')
    @patch('src.yt_pipeline.fetch_transcript')
    @patch('src.yt_pipeline.get_basic_meta')
    @patch('src.yt_pipeline.extract_video_id')
    def test_run_for_url_success(self, mock_extract_id, mock_get_meta, 
                                 mock_fetch_transcript, mock_analyze_text):
        """Test successful complete pipeline run"""
        # Setup mocks
        mock_extract_id.return_value = "JU8BwMe_BWg"
        mock_get_meta.return_value = self.sample_metadata
        
        mock_segments = [MockTranscriptSegment(**seg) for seg in self.sample_transcript]
        mock_fetch_transcript.return_value = mock_segments
        
        mock_analyze_text.return_value = self.sample_llm_response
        
        # Create mock drive client
        mock_drive = MagicMock()
        mock_drive.ensure_path.return_value = "mock_folder"
        mock_drive.upload_string.return_value = "mock_file_id"
        
        # Test
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('src.yt_pipeline.time.strftime', return_value="2024-01-01"):
                run_for_url("https://youtu.be/JU8BwMe_BWg", mock_drive)
            
            # Verify all components were called
            mock_extract_id.assert_called_once_with("https://youtu.be/JU8BwMe_BWg")
            mock_get_meta.assert_called_once_with("https://youtu.be/JU8BwMe_BWg")
            mock_fetch_transcript.assert_called_once_with("JU8BwMe_BWg", lang_priorities=("cs", "en"))
            mock_analyze_text.assert_called_once()
            
            # Verify files were uploaded
            self.assertEqual(mock_drive.upload_string.call_count, 3)  # raw, clean, analysis

            # Ensure folder name uses slugified title
            expected_folder = "2024-01-01_advanced-claude-code-tips-and-tricks"
            mock_drive.ensure_path.assert_called_once()
            path_parts = mock_drive.ensure_path.call_args[0][0]
            self.assertEqual(path_parts, ["youtube", "tech-tutorial-channel", expected_folder])
            
    @patch('src.yt_pipeline.analyze_text')
    @patch('src.yt_pipeline.fetch_transcript')
    @patch('src.yt_pipeline.get_basic_meta')
    @patch('src.yt_pipeline.extract_video_id')
    def test_run_for_url_llm_failure(self, mock_extract_id, mock_get_meta,
                                    mock_fetch_transcript, mock_analyze_text):
        """Test pipeline graceful degradation when LLM fails"""
        # Setup mocks
        mock_extract_id.return_value = "JU8BwMe_BWg"
        mock_get_meta.return_value = self.sample_metadata
        
        mock_segments = [MockTranscriptSegment(**seg) for seg in self.sample_transcript]
        mock_fetch_transcript.return_value = mock_segments
        
        # LLM should fail
        mock_analyze_text.side_effect = Exception("LLM API Error")
        
        # Create mock drive client
        mock_drive = MagicMock()
        mock_drive.upload_string.return_value = "mock_file_id"
        
        # Test - should not raise exception
        run_for_url("https://youtu.be/JU8BwMe_BWg", mock_drive)
        
        # Verify transcript files were still uploaded (2 calls for raw+clean)
        # Plus 1 call for placeholder analysis = 3 total
        self.assertEqual(mock_drive.upload_string.call_count, 3)
        
    @patch('src.yt_pipeline.fetch_transcript')
    @patch('src.yt_pipeline.get_basic_meta')
    @patch('src.yt_pipeline.extract_video_id')
    def test_run_for_url_no_transcript(self, mock_extract_id, mock_get_meta, 
                                      mock_fetch_transcript):
        """Test pipeline when no transcript is available"""
        # Setup mocks
        mock_extract_id.return_value = "JU8BwMe_BWg"
        mock_get_meta.return_value = self.sample_metadata
        mock_fetch_transcript.return_value = []  # No transcript
        
        # Create mock drive client
        mock_drive = MagicMock()
        
        # Test - should handle gracefully
        with patch('builtins.print') as mock_print:
            run_for_url("https://youtu.be/JU8BwMe_BWg", mock_drive)
            
            # Should print error message
            mock_print.assert_called()
            
    def test_run_for_url_invalid_url(self):
        """Test pipeline with invalid URL - should raise subprocess error"""
        mock_drive = MagicMock()
        
        # get_basic_meta will fail with subprocess error for invalid URLs
        with self.assertRaises(subprocess.CalledProcessError):
            run_for_url("invalid_url", mock_drive)

if __name__ == '__main__':
    unittest.main()
