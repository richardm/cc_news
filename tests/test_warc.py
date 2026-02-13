"""Tests for cc_news_analyzer.warc module."""

import unittest
from unittest.mock import MagicMock, mock_open, patch

from cc_news_analyzer.warc import count_articles


def _make_record(warc_type, content_type=None, has_http_headers=True):
    """Create a mock WARC record with the given type and content type."""
    record = MagicMock()
    record.rec_headers.get_header.side_effect = lambda h: {
        "WARC-Type": warc_type,
        "WARC-Record-ID": "<urn:uuid:test>",
    }.get(h)

    if has_http_headers and content_type is not None:
        record.http_headers.get_header.side_effect = lambda h, default="": {
            "Content-Type": content_type,
        }.get(h, default)
    elif not has_http_headers:
        record.http_headers = None
    else:
        record.http_headers.get_header.side_effect = lambda h, default="": default

    return record


class TestCountArticles(unittest.TestCase):
    """Tests for count_articles()."""

    def test_raises_on_missing_file(self):
        """Should raise FileNotFoundError when the file does not exist."""
        with self.assertRaises(FileNotFoundError):
            count_articles("/no/such/file.warc")

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_counts_only_response_records_with_html(
        self, _mock_isfile, _mock_open, mock_iterator
    ):
        """Should count only response records with text/html content type."""
        mock_iterator.return_value = [
            _make_record("response", "text/html"),
            _make_record("request"),
            _make_record("response", "text/html"),
            _make_record("warcinfo", has_http_headers=False),
        ]

        result = count_articles("test.warc")

        self.assertEqual(result, 2)

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_ignores_non_html_responses(self, _mock_isfile, _mock_open, mock_iterator):
        """Should not count response records with non-HTML content types."""
        mock_iterator.return_value = [
            _make_record("response", "text/html"),
            _make_record("response", "application/json"),
            _make_record("response", "image/png"),
            _make_record("response", "application/pdf"),
        ]

        result = count_articles("test.warc")

        self.assertEqual(result, 1)

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_ignores_request_records(self, _mock_isfile, _mock_open, mock_iterator):
        """Should not count request records even if they reference HTML."""
        mock_iterator.return_value = [
            _make_record("request", "text/html"),
            _make_record("request"),
        ]

        result = count_articles("test.warc")

        self.assertEqual(result, 0)

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_ignores_warcinfo_records(self, _mock_isfile, _mock_open, mock_iterator):
        """Should not count warcinfo records."""
        mock_iterator.return_value = [
            _make_record("warcinfo", has_http_headers=False),
        ]

        result = count_articles("test.warc")

        self.assertEqual(result, 0)

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_returns_zero_for_empty_warc(self, _mock_isfile, _mock_open, mock_iterator):
        """Should return zero when the WARC file has no records."""
        mock_iterator.return_value = []

        result = count_articles("test.warc")

        self.assertEqual(result, 0)

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_counts_html_with_charset(self, _mock_isfile, _mock_open, mock_iterator):
        """Should count response records with text/html; charset=utf-8."""
        mock_iterator.return_value = [
            _make_record("response", "text/html; charset=utf-8"),
            _make_record("response", "text/html; charset=iso-8859-1"),
        ]

        result = count_articles("test.warc")

        self.assertEqual(result, 2)

    @patch("cc_news_analyzer.warc.ArchiveIterator")
    @patch("builtins.open", new_callable=mock_open)
    @patch("cc_news_analyzer.warc.os.path.isfile", return_value=True)
    def test_response_without_http_headers(
        self, _mock_isfile, _mock_open, mock_iterator
    ):
        """Should not count response records that lack HTTP headers."""
        mock_iterator.return_value = [
            _make_record("response", has_http_headers=False),
        ]

        result = count_articles("test.warc")

        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()
