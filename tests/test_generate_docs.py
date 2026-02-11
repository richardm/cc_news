"""Tests for cc_news_analyzer.generate_docs module."""

import unittest

import click
from cc_news_analyzer.generate_docs import generate_docs


class TestGenerateDocs(unittest.TestCase):
    """Tests for the generate_docs function."""

    def setUp(self):
        """Build a small Click CLI for testing."""
        from cc_news_analyzer.cli import cli

        self.output = generate_docs(cli, prog_name="cc-news")

    def test_contains_root_heading(self):
        """Should contain a top-level heading with the prog name."""
        self.assertIn("# cc-news", self.output)

    def test_contains_root_description(self):
        """Should contain the root group's help text."""
        self.assertIn("CC News Analyzer", self.output)

    def test_contains_count_records_section(self):
        """Should contain a section for the count-records command."""
        self.assertIn("## cc-news count-records", self.output)

    def test_contains_get_index_section(self):
        """Should contain a section for the get-index command."""
        self.assertIn("## cc-news get-index", self.output)

    def test_contains_get_warc_section(self):
        """Should contain a section for the get-warc command."""
        self.assertIn("## cc-news get-warc", self.output)

    def test_contains_option_documentation(self):
        """Should document the --date option from get-index."""
        self.assertIn("--date", self.output)

    def test_contains_argument_documentation(self):
        """Should document the WARC_FILE argument from count-records."""
        self.assertIn("WARC_FILE", self.output)

    def test_contains_usage_blocks(self):
        """Should contain usage lines in code blocks."""
        self.assertIn("```", self.output)
        self.assertIn("Usage:", self.output)

    def test_returns_string(self):
        """Should return a string."""
        self.assertIsInstance(self.output, str)


class TestGenerateDocsWithCustomGroup(unittest.TestCase):
    """Tests for generate_docs with a custom Click group."""

    def test_custom_prog_name(self):
        """Should use the provided prog_name in headings."""

        @click.group()
        def my_cli():
            """My test CLI."""
            pass

        @my_cli.command("hello")
        @click.option("--name", default="world", help="Who to greet.")
        def hello_cmd(name):
            """Say hello."""
            pass

        output = generate_docs(my_cli, prog_name="my-tool")
        self.assertIn("# my-tool", output)
        self.assertIn("## my-tool hello", output)
        self.assertIn("--name", output)

    def test_empty_group(self):
        """Should handle a group with no subcommands."""

        @click.group()
        def empty_cli():
            """An empty CLI."""
            pass

        output = generate_docs(empty_cli, prog_name="empty")
        self.assertIn("# empty", output)
        self.assertIn("An empty CLI.", output)


if __name__ == "__main__":
    unittest.main()
