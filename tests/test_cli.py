"""Tests for cc_news_analyzer.cli module."""

import os
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch

from cc_news_analyzer.cli import DEFAULT_DOWNLOAD_DIR, cli
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


class TestGetWarcCmd(unittest.TestCase):
    """Tests for the get-warc CLI command."""

    def setUp(self):
        """Set up the CLI test runner."""
        self.runner = CliRunner()

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    def test_downloads_warc_file(self, mock_download):
        """Should call download_warc_by_path with the given path and .tmp dir."""
        mock_download.return_value = ".tmp/CC-NEWS-20260204051206-06668.warc.gz"

        result = self.runner.invoke(
            cli,
            [
                "get-warc",
                "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        mock_download.assert_called_once_with(
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ".tmp",
        )
        self.assertIn("CC-NEWS-20260204051206-06668.warc.gz", result.output)

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    def test_custom_dest_dir(self, mock_download):
        """Should use the --dest option when provided."""
        mock_download.return_value = "/data/CC-NEWS-20260204051206-06668.warc.gz"

        result = self.runner.invoke(
            cli,
            [
                "get-warc",
                "--dest",
                "/data",
                "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        mock_download.assert_called_once_with(
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            "/data",
        )

    def test_missing_argument(self):
        """Should fail when no WARC path argument is provided."""
        result = self.runner.invoke(cli, ["get-warc"])
        self.assertNotEqual(result.exit_code, 0)

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    def test_empty_path_shows_error(self, mock_download):
        """Should show an error when an empty path is given."""
        mock_download.side_effect = ValueError("WARC path must not be empty.")

        result = self.runner.invoke(cli, ["get-warc", ""])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("WARC path must not be empty", result.output)

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    def test_network_error_shows_friendly_error(self, mock_download):
        """Should display a friendly error when the download fails."""
        mock_download.side_effect = OSError("Connection refused")

        result = self.runner.invoke(
            cli,
            [
                "get-warc",
                "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Download failed", result.output)
        self.assertNotIn("Traceback", result.output)

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    @patch("cc_news_analyzer.cli.resolve_warc_path")
    def test_http_error_shows_friendly_error(self, mock_resolve, mock_download):
        """Should display a friendly error for HTTP errors like 404."""
        from urllib.error import HTTPError

        mock_resolve.return_value = "crawl-data/CC-NEWS/2026/02/bad-path.warc.gz"
        mock_download.side_effect = HTTPError(
            "https://data.commoncrawl.org/crawl-data/CC-NEWS/2026/02/bad-path.warc.gz",
            404,
            "Not Found",
            {},
            None,
        )

        result = self.runner.invoke(
            cli,
            [
                "get-warc",
                "bad-path.warc.gz",
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Download failed", result.output)
        self.assertIn("404", result.output)
        self.assertNotIn("Traceback", result.output)

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    def test_output_shows_downloaded_path(self, mock_download):
        """Should show the downloaded file path in output."""
        mock_download.return_value = ".tmp/CC-NEWS-20260204051206-06668.warc.gz"

        result = self.runner.invoke(
            cli,
            [
                "get-warc",
                "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Downloaded", result.output)
        self.assertIn(".tmp/CC-NEWS-20260204051206-06668.warc.gz", result.output)

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    @patch("cc_news_analyzer.cli.resolve_warc_path")
    def test_resolves_full_url(self, mock_resolve, mock_download):
        """Should resolve a full URL before downloading."""
        mock_resolve.return_value = (
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        )
        mock_download.return_value = ".tmp/CC-NEWS-20260204051206-06668.warc.gz"

        url = (
            "https://data.commoncrawl.org/"
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        )
        result = self.runner.invoke(cli, ["get-warc", url])

        self.assertEqual(result.exit_code, 0)
        mock_resolve.assert_called_once()
        mock_download.assert_called_once_with(
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ".tmp",
        )

    @patch("cc_news_analyzer.cli.download_warc_by_path")
    @patch("cc_news_analyzer.cli.resolve_warc_path")
    def test_resolves_bare_filename(self, mock_resolve, mock_download):
        """Should resolve a bare filename via the local index."""
        mock_resolve.return_value = (
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        )
        mock_download.return_value = ".tmp/CC-NEWS-20260204051206-06668.warc.gz"

        result = self.runner.invoke(
            cli, ["get-warc", "CC-NEWS-20260204051206-06668.warc.gz"]
        )

        self.assertEqual(result.exit_code, 0)
        mock_resolve.assert_called_once()
        mock_download.assert_called_once_with(
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            ".tmp",
        )

    @patch("cc_news_analyzer.cli.resolve_warc_path")
    def test_resolve_error_shows_friendly_message(self, mock_resolve):
        """Should show a friendly error when resolve_warc_path fails."""
        mock_resolve.side_effect = ValueError(
            "Could not resolve filename 'bad.warc.gz'"
        )

        result = self.runner.invoke(cli, ["get-warc", "bad.warc.gz"])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Could not resolve", result.output)


class TestCountRecordsCmd(unittest.TestCase):
    """Smoke tests for the existing count-records command."""

    def setUp(self):
        """Set up the CLI test runner."""
        self.runner = CliRunner()
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _create_file(self, name: str) -> str:
        """Create a temporary file with the given name."""
        path = os.path.join(self.tmp_dir, name)
        with open(path, "w") as f:
            f.write("fake")
        return path

    def test_missing_file_argument(self):
        """Should fail when no file argument is provided."""
        result = self.runner.invoke(cli, ["count-records"])
        self.assertNotEqual(result.exit_code, 0)

    def test_nonexistent_file(self):
        """Should fail when the file does not exist."""
        result = self.runner.invoke(cli, ["count-records", "/no/such/file.warc"])
        self.assertNotEqual(result.exit_code, 0)

    def test_rejects_non_warc_extension(self):
        """Should show a friendly error for non-.warc files."""
        txt_file = self._create_file("warc.paths")
        result = self.runner.invoke(cli, ["count-records", txt_file])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("does not appear to be a WARC file", result.output)

    @patch("cc_news_analyzer.cli._count_records")
    def test_archive_load_failed_shows_friendly_error(self, mock_count):
        """Should show a friendly error when warcio cannot parse the file."""
        from warcio.exceptions import ArchiveLoadFailed

        mock_count.side_effect = ArchiveLoadFailed("bad format")
        warc_file = self._create_file("test.warc.gz")

        result = self.runner.invoke(cli, ["count-records", warc_file])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Failed to read WARC file", result.output)
        self.assertNotIn("Traceback", result.output)


class TestCountArticlesCmd(unittest.TestCase):
    """Tests for the count-articles CLI command."""

    def setUp(self):
        """Set up the CLI test runner."""
        self.runner = CliRunner()
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def _create_file(self, name: str) -> str:
        """Create a temporary file with the given name."""
        path = os.path.join(self.tmp_dir, name)
        with open(path, "w") as f:
            f.write("fake")
        return path

    def test_missing_file_argument(self):
        """Should fail when no file argument is provided."""
        result = self.runner.invoke(cli, ["count-articles"])
        self.assertNotEqual(result.exit_code, 0)

    def test_nonexistent_file(self):
        """Should fail when the file does not exist."""
        result = self.runner.invoke(cli, ["count-articles", "/no/such/file.warc"])
        self.assertNotEqual(result.exit_code, 0)

    def test_rejects_non_warc_extension(self):
        """Should show a friendly error for non-.warc files."""
        txt_file = self._create_file("warc.paths")
        result = self.runner.invoke(cli, ["count-articles", txt_file])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("does not appear to be a WARC file", result.output)

    def test_suggests_tmp_path_when_file_not_found(self):
        """Should suggest .tmp/ path when file exists there."""
        warc_name = "CC-NEWS-20260207200705-06723.warc.gz"
        tmp_path = os.path.join(DEFAULT_DOWNLOAD_DIR, warc_name)

        # Mock os.path.exists to simulate .tmp/ containing the file
        original_exists = os.path.exists

        def fake_exists(path):
            if path == warc_name:
                return False
            if path == tmp_path:
                return True
            return original_exists(path)

        with patch("cc_news_analyzer.cli.os.path.exists", side_effect=fake_exists):
            result = self.runner.invoke(cli, ["count-articles", warc_name])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(".tmp/", result.output)
        self.assertIn("Did you mean", result.output)

    @patch("cc_news_analyzer.cli._count_articles")
    def test_outputs_article_count(self, mock_count):
        """Should display the article count from count_articles."""
        mock_count.return_value = 42
        warc_file = self._create_file("test.warc.gz")

        result = self.runner.invoke(cli, ["count-articles", warc_file])

        self.assertEqual(result.exit_code, 0)
        mock_count.assert_called_once_with(warc_file)
        self.assertIn("42", result.output)
        self.assertIn("Total articles", result.output)

    @patch("cc_news_analyzer.cli._count_articles")
    def test_outputs_zero_count(self, mock_count):
        """Should display zero when no articles are found."""
        mock_count.return_value = 0
        warc_file = self._create_file("test.warc")

        result = self.runner.invoke(cli, ["count-articles", warc_file])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("0", result.output)

    @patch("cc_news_analyzer.cli._count_articles")
    def test_archive_load_failed_shows_friendly_error(self, mock_count):
        """Should show a friendly error when warcio cannot parse the file."""
        from warcio.exceptions import ArchiveLoadFailed

        mock_count.side_effect = ArchiveLoadFailed("bad format")
        warc_file = self._create_file("test.warc.gz")

        result = self.runner.invoke(cli, ["count-articles", warc_file])

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Failed to read WARC file", result.output)
        self.assertNotIn("Traceback", result.output)


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

    def test_short_help_flag(self):
        """Should show help text with -h shorthand."""
        result = self.runner.invoke(cli, ["-h"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("CC News Analyzer", result.output)

    def test_subcommand_short_help_flag(self):
        """Should show subcommand help text with -h shorthand."""
        result = self.runner.invoke(cli, ["count-articles", "-h"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Count article records", result.output)

    def test_get_index_help(self):
        """Should show help text for the get-index command."""
        result = self.runner.invoke(cli, ["get-index", "--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("MM-YYYY", result.output)


if __name__ == "__main__":
    unittest.main()
