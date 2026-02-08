"""Tests for cc_news_analyzer.cli module."""

import unittest
from datetime import datetime
from unittest.mock import patch

from cc_news_analyzer.cli import cli
from click.testing import CliRunner


class TestGetIndexCmd(unittest.TestCase):
    """Tests for the get-index CLI command."""

    def setUp(self):
        """Set up the CLI test runner."""
        self.runner = CliRunner()

    @patch("cc_news_analyzer.cli.fetch_warc_paths")
    def test_with_date_option(self, mock_fetch):
        """Should fetch the index for the specified month and list paths."""
        mock_fetch.return_value = [
            "crawl-data/CC-NEWS/2026/02/file1.warc.gz",
            "crawl-data/CC-NEWS/2026/02/file2.warc.gz",
        ]

        result = self.runner.invoke(cli, ["get-index", "--date", "02-2026"])

        self.assertEqual(result.exit_code, 0)
        mock_fetch.assert_called_once_with(2026, 2, ".tmp")
        self.assertIn("Found 2 WARC file(s) for 2026-02:", result.output)
        self.assertIn("crawl-data/CC-NEWS/2026/02/file1.warc.gz", result.output)
        self.assertIn("crawl-data/CC-NEWS/2026/02/file2.warc.gz", result.output)

    @patch("cc_news_analyzer.cli.fetch_warc_paths")
    @patch("cc_news_analyzer.cli.datetime")
    def test_without_date_defaults_to_current_month(self, mock_dt, mock_fetch):
        """Should default to the current month when --date is not provided."""
        mock_dt.now.return_value = datetime(2026, 3, 15)
        mock_fetch.return_value = [
            "crawl-data/CC-NEWS/2026/03/file1.warc.gz",
        ]

        result = self.runner.invoke(cli, ["get-index"])

        self.assertEqual(result.exit_code, 0)
        mock_fetch.assert_called_once_with(2026, 3, ".tmp")
        self.assertIn("Found 1 WARC file(s) for 2026-03:", result.output)

    def test_invalid_date_format(self):
        """Should display an error for an invalid date format."""
        result = self.runner.invoke(cli, ["get-index", "--date", "2026-02"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid date format", result.output)

    def test_invalid_date_non_numeric(self):
        """Should display an error for non-numeric date input."""
        result = self.runner.invoke(cli, ["get-index", "--date", "ab-cdef"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Invalid date format", result.output)

    @patch("cc_news_analyzer.cli.fetch_warc_paths")
    def test_empty_index(self, mock_fetch):
        """Should display zero count when the index is empty."""
        mock_fetch.return_value = []

        result = self.runner.invoke(cli, ["get-index", "--date", "01-2026"])

        self.assertEqual(result.exit_code, 0)
        mock_fetch.assert_called_once_with(2026, 1, ".tmp")
        self.assertIn("Found 0 WARC file(s) for 2026-01:", result.output)

    @patch("cc_news_analyzer.cli.fetch_warc_paths")
    def test_fetch_error_propagates(self, mock_fetch):
        """Should propagate OSError from fetch_warc_paths."""
        mock_fetch.side_effect = OSError("Network error")

        result = self.runner.invoke(cli, ["get-index", "--date", "02-2026"])

        self.assertNotEqual(result.exit_code, 0)


class TestCountRecordsCmd(unittest.TestCase):
    """Smoke tests for the existing count-records command."""

    def setUp(self):
        """Set up the CLI test runner."""
        self.runner = CliRunner()

    def test_missing_file_argument(self):
        """Should fail when no file argument is provided."""
        result = self.runner.invoke(cli, ["count-records"])
        self.assertNotEqual(result.exit_code, 0)

    def test_nonexistent_file(self):
        """Should fail when the file does not exist."""
        result = self.runner.invoke(cli, ["count-records", "/no/such/file.warc"])
        self.assertNotEqual(result.exit_code, 0)


class TestCliGroup(unittest.TestCase):
    """Tests for the CLI group itself."""

    def setUp(self):
        """Set up the CLI test runner."""
        self.runner = CliRunner()

    def test_help(self):
        """Should show help text."""
        result = self.runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("CC News Analyzer", result.output)

    def test_get_index_help(self):
        """Should show help text for the get-index command."""
        result = self.runner.invoke(cli, ["get-index", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("MM-YYYY", result.output)


if __name__ == "__main__":
    unittest.main()
