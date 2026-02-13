"""Tests for cc_news_analyzer.index module."""

import gzip
import os
import unittest
from datetime import datetime
from unittest.mock import patch

from cc_news_analyzer.index import (
    CC_NEWS_BASE_URL,
    build_current_month_index_url,
    build_index_url,
    build_warc_urls,
    download_warc_by_path,
    fetch_warc_paths,
    parse_month_date,
    resolve_warc_path,
)


class TestBuildIndexUrl(unittest.TestCase):
    """Tests for build_index_url."""

    def test_valid_year_and_month(self):
        """Should return a correctly formatted URL for valid inputs."""
        url = build_index_url(2026, 2)
        self.assertEqual(
            url,
            "https://data.commoncrawl.org/crawl-data/CC-NEWS/2026/02/warc.paths.gz",
        )

    def test_month_zero_padded(self):
        """Should zero-pad single-digit months."""
        url = build_index_url(2026, 1)
        self.assertIn("/01/", url)

    def test_double_digit_month(self):
        """Should handle double-digit months correctly."""
        url = build_index_url(2026, 12)
        self.assertIn("/12/", url)

    def test_year_too_low_raises(self):
        """Should raise ValueError when year is below 2016."""
        with self.assertRaises(ValueError):
            build_index_url(2015, 1)

    def test_year_too_high_raises(self):
        """Should raise ValueError when year is above 2030."""
        with self.assertRaises(ValueError):
            build_index_url(2031, 1)

    def test_month_too_low_raises(self):
        """Should raise ValueError when month is 0."""
        with self.assertRaises(ValueError):
            build_index_url(2026, 0)

    def test_month_too_high_raises(self):
        """Should raise ValueError when month is 13."""
        with self.assertRaises(ValueError):
            build_index_url(2026, 13)

    def test_boundary_year_2016(self):
        """Should accept year 2016 (lower boundary)."""
        url = build_index_url(2016, 6)
        self.assertIn("/2016/", url)

    def test_boundary_year_2030(self):
        """Should accept year 2030 (upper boundary)."""
        url = build_index_url(2030, 6)
        self.assertIn("/2030/", url)


class TestBuildCurrentMonthIndexUrl(unittest.TestCase):
    """Tests for build_current_month_index_url."""

    @patch("cc_news_analyzer.index.datetime")
    def test_uses_current_year_and_month(self, mock_datetime):
        """Should build URL using the current year and month."""
        mock_datetime.now.return_value = datetime(2026, 3, 15)
        url = build_current_month_index_url()
        self.assertEqual(
            url,
            "https://data.commoncrawl.org/crawl-data/CC-NEWS/2026/03/warc.paths.gz",
        )


class TestParseMonthDate(unittest.TestCase):
    """Tests for parse_month_date."""

    def test_valid_date(self):
        """Should parse MM-YYYY into (year, month)."""
        year, month = parse_month_date("02-2026")
        self.assertEqual(year, 2026)
        self.assertEqual(month, 2)

    def test_valid_date_december(self):
        """Should parse December correctly."""
        year, month = parse_month_date("12-2025")
        self.assertEqual(year, 2025)
        self.assertEqual(month, 12)

    def test_valid_date_january(self):
        """Should parse January correctly."""
        year, month = parse_month_date("01-2020")
        self.assertEqual(year, 2020)
        self.assertEqual(month, 1)

    def test_invalid_format_no_dash(self):
        """Should raise ValueError for input without a dash."""
        with self.assertRaises(ValueError):
            parse_month_date("022026")

    def test_invalid_format_reversed(self):
        """Should raise ValueError for YYYY-MM format."""
        with self.assertRaises(ValueError):
            parse_month_date("2026-02")

    def test_invalid_month_zero(self):
        """Should raise ValueError for month 00."""
        with self.assertRaises(ValueError):
            parse_month_date("00-2026")

    def test_invalid_month_thirteen(self):
        """Should raise ValueError for month 13."""
        with self.assertRaises(ValueError):
            parse_month_date("13-2026")

    def test_invalid_non_numeric(self):
        """Should raise ValueError for non-numeric input."""
        with self.assertRaises(ValueError):
            parse_month_date("ab-cdef")

    def test_empty_string(self):
        """Should raise ValueError for empty string."""
        with self.assertRaises(ValueError):
            parse_month_date("")


class TestFetchWarcPaths(unittest.TestCase):
    """Tests for fetch_warc_paths."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = os.path.join(os.path.dirname(__file__), ".test_tmp")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up the temporary directory."""
        import shutil

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def _create_fake_gz(self, content: str, dest: str):
        """Helper: write gzipped content to dest."""
        with gzip.open(dest, "wt") as f:
            f.write(content)

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_returns_parsed_paths(self, mock_urlretrieve):
        """Should download, decompress, and return parsed WARC paths."""
        lines = (
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201022924-06627.warc.gz\n"
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201054311-06628.warc.gz\n"
        )

        def fake_download(url, dest):
            self._create_fake_gz(lines, dest)

        mock_urlretrieve.side_effect = fake_download

        paths = fetch_warc_paths(2026, 2, self.test_dir)

        self.assertEqual(len(paths), 2)
        self.assertEqual(
            paths[0],
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201022924-06627.warc.gz",
        )
        self.assertEqual(
            paths[1],
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201054311-06628.warc.gz",
        )

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_skips_blank_lines(self, mock_urlretrieve):
        """Should skip blank lines in the index file."""
        lines = (
            "crawl-data/CC-NEWS/2026/02/file1.warc.gz\n"
            "\n"
            "crawl-data/CC-NEWS/2026/02/file2.warc.gz\n"
            "\n"
        )

        def fake_download(url, dest):
            self._create_fake_gz(lines, dest)

        mock_urlretrieve.side_effect = fake_download

        paths = fetch_warc_paths(2026, 2, self.test_dir)
        self.assertEqual(len(paths), 2)

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_returns_empty_for_empty_index(self, mock_urlretrieve):
        """Should return an empty list if the index is empty."""

        def fake_download(url, dest):
            self._create_fake_gz("", dest)

        mock_urlretrieve.side_effect = fake_download

        paths = fetch_warc_paths(2026, 2, self.test_dir)
        self.assertEqual(paths, [])

    def test_invalid_year_raises(self):
        """Should raise ValueError for invalid year without downloading."""
        with self.assertRaises(ValueError):
            fetch_warc_paths(2015, 1, self.test_dir)

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_creates_dest_dir(self, mock_urlretrieve):
        """Should create the destination directory if it does not exist."""
        new_dir = os.path.join(self.test_dir, "subdir")

        def fake_download(url, dest):
            self._create_fake_gz("path/to/file.warc.gz\n", dest)

        mock_urlretrieve.side_effect = fake_download

        fetch_warc_paths(2026, 2, new_dir)
        self.assertTrue(os.path.isdir(new_dir))


class TestDownloadWarcByPath(unittest.TestCase):
    """Tests for download_warc_by_path."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = os.path.join(os.path.dirname(__file__), ".test_tmp_dl")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up the temporary directory."""
        import shutil

        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_downloads_file_and_returns_path(self, mock_urlretrieve):
        """Should build URL from relative path and download the file."""
        warc_path = "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"

        def fake_download(url, dest):
            with open(dest, "w") as f:
                f.write("fake warc content")

        mock_urlretrieve.side_effect = fake_download

        result = download_warc_by_path(warc_path, self.test_dir)

        expected_url = f"{CC_NEWS_BASE_URL}/{warc_path}"
        mock_urlretrieve.assert_called_once_with(
            expected_url,
            os.path.join(self.test_dir, "CC-NEWS-20260204051206-06668.warc.gz"),
        )
        self.assertEqual(
            result,
            os.path.join(self.test_dir, "CC-NEWS-20260204051206-06668.warc.gz"),
        )
        self.assertTrue(os.path.exists(result))

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_creates_dest_dir_if_missing(self, mock_urlretrieve):
        """Should create the destination directory if it does not exist."""
        new_dir = os.path.join(self.test_dir, "nested")
        warc_path = "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"

        def fake_download(url, dest):
            with open(dest, "w") as f:
                f.write("fake")

        mock_urlretrieve.side_effect = fake_download

        download_warc_by_path(warc_path, new_dir)
        self.assertTrue(os.path.isdir(new_dir))

    def test_empty_path_raises(self):
        """Should raise ValueError for an empty path."""
        with self.assertRaises(ValueError):
            download_warc_by_path("", self.test_dir)

    def test_path_with_no_filename_raises(self):
        """Should raise ValueError when path has no filename component."""
        with self.assertRaises(ValueError):
            download_warc_by_path("crawl-data/CC-NEWS/2026/02/", self.test_dir)

    @patch("cc_news_analyzer.index.urllib.request.urlretrieve")
    def test_network_error_propagates(self, mock_urlretrieve):
        """Should propagate OSError from urlretrieve."""
        mock_urlretrieve.side_effect = OSError("Network error")
        warc_path = "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        with self.assertRaises(OSError):
            download_warc_by_path(warc_path, self.test_dir)


class TestBuildWarcUrls(unittest.TestCase):
    """Tests for build_warc_urls."""

    def test_converts_paths_to_urls(self):
        """Should prepend the base URL to each path."""
        paths = [
            "crawl-data/CC-NEWS/2026/02/file1.warc.gz",
            "crawl-data/CC-NEWS/2026/02/file2.warc.gz",
        ]
        urls = build_warc_urls(paths)
        self.assertEqual(
            urls,
            [
                f"{CC_NEWS_BASE_URL}/crawl-data/CC-NEWS/2026/02/file1.warc.gz",
                f"{CC_NEWS_BASE_URL}/crawl-data/CC-NEWS/2026/02/file2.warc.gz",
            ],
        )

    def test_empty_list(self):
        """Should return an empty list when given no paths."""
        self.assertEqual(build_warc_urls([]), [])

    def test_single_path(self):
        """Should handle a single path."""
        urls = build_warc_urls(["some/path.warc.gz"])
        self.assertEqual(len(urls), 1)
        self.assertTrue(urls[0].startswith(CC_NEWS_BASE_URL))


class TestResolveWarcPath(unittest.TestCase):
    """Tests for resolve_warc_path."""

    def test_relative_path_unchanged(self):
        """Should return relative crawl-data paths unchanged."""
        path = "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        self.assertEqual(resolve_warc_path(path), path)

    def test_strips_full_url_to_relative_path(self):
        """Should strip the base URL prefix from a full URL."""
        url = (
            "https://data.commoncrawl.org/"
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        )
        expected = "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        self.assertEqual(resolve_warc_path(url), expected)

    def test_strips_url_with_trailing_slash_base(self):
        """Should handle base URL with trailing slash."""
        url = (
            "https://data.commoncrawl.org/"
            "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        )
        expected = "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"
        self.assertEqual(resolve_warc_path(url), expected)

    def test_bare_filename_resolved_from_index(self):
        """Should resolve a bare filename using the local index file."""
        index_dir = os.path.join(os.path.dirname(__file__), ".test_resolve_tmp")
        os.makedirs(index_dir, exist_ok=True)
        try:
            index_path = os.path.join(index_dir, "warc.paths")
            with open(index_path, "w") as f:
                f.write(
                    "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201022924-06627.warc.gz\n"
                    "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz\n"
                )

            result = resolve_warc_path(
                "CC-NEWS-20260204051206-06668.warc.gz",
                index_dir=index_dir,
            )
            self.assertEqual(
                result,
                "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz",
            )
        finally:
            import shutil

            shutil.rmtree(index_dir, ignore_errors=True)

    def test_bare_filename_not_in_index_raises(self):
        """Should raise ValueError when filename not found in index."""
        index_dir = os.path.join(os.path.dirname(__file__), ".test_resolve_tmp2")
        os.makedirs(index_dir, exist_ok=True)
        try:
            index_path = os.path.join(index_dir, "warc.paths")
            with open(index_path, "w") as f:
                f.write(
                    "crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201022924-06627.warc.gz\n"
                )

            with self.assertRaises(ValueError) as ctx:
                resolve_warc_path(
                    "CC-NEWS-NONEXISTENT.warc.gz",
                    index_dir=index_dir,
                )
            self.assertIn("Could not resolve", str(ctx.exception))
        finally:
            import shutil

            shutil.rmtree(index_dir, ignore_errors=True)

    def test_bare_filename_no_index_file_raises(self):
        """Should raise ValueError when no local index file exists."""
        with self.assertRaises(ValueError) as ctx:
            resolve_warc_path(
                "CC-NEWS-20260204051206-06668.warc.gz",
                index_dir="/nonexistent/dir",
            )
        self.assertIn("get-index", str(ctx.exception))

    def test_empty_path_raises(self):
        """Should raise ValueError for empty input."""
        with self.assertRaises(ValueError):
            resolve_warc_path("")

    def test_whitespace_only_raises(self):
        """Should raise ValueError for whitespace-only input."""
        with self.assertRaises(ValueError):
            resolve_warc_path("   ")


if __name__ == "__main__":
    unittest.main()
