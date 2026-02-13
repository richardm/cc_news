"""CLI entrypoint for CC News Analyzer."""

import os
import urllib.error
from datetime import datetime

import click
from warcio.exceptions import ArchiveLoadFailed

from cc_news_analyzer.index import (
    download_warc_by_path,
    fetch_warc_paths,
    parse_month_date,
    resolve_warc_path,
)
from cc_news_analyzer.warc import count_articles as _count_articles
from cc_news_analyzer.warc import count_records as _count_records

WARC_EXTENSIONS = (".warc", ".warc.gz")
DEFAULT_DOWNLOAD_DIR = ".tmp"


class WarcFilePath(click.Path):
    """A Click path type that validates WARC file extension and suggests .tmp/."""

    name = "WARC_FILE"

    def convert(self, value, param, ctx):
        """Validate the WARC file path."""
        path = value

        # Check if file exists
        if not os.path.exists(path):
            # Check if it exists in .tmp/
            basename = os.path.basename(path)
            tmp_path = os.path.join(DEFAULT_DOWNLOAD_DIR, basename)
            if os.path.exists(tmp_path):
                self.fail(
                    f"File '{path}' not found. Did you mean '{tmp_path}'?",
                    param,
                    ctx,
                )
            self.fail(f"Path '{path}' does not exist.", param, ctx)

        # Validate extension
        if not path.endswith(WARC_EXTENSIONS):
            self.fail(
                f"'{path}' does not appear to be a WARC file (expected .warc or .warc.gz extension).",
                param,
                ctx,
            )

        return path


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """CC News Analyzer - Analyze Common Crawl News WARC datasets."""
    pass


@cli.command("count-records")
@click.argument("warc_file", type=WarcFilePath())
def count_records_cmd(warc_file: str):
    """Count the number of WARC records with a WARC-Record-ID in a file."""
    try:
        total = _count_records(warc_file)
    except ArchiveLoadFailed as exc:
        raise click.ClickException(
            f"Failed to read WARC file: {warc_file} -- is this a valid .warc or .warc.gz file?"
        ) from exc
    click.echo(f"Total WARC records with WARC-Record-ID: {total}")


@cli.command("count-articles")
@click.argument("warc_file", type=WarcFilePath())
def count_articles_cmd(warc_file: str):
    """Count article records (HTML responses) in a WARC file.

    Articles are WARC response records with an HTML content type.
    This is distinct from count-records, which counts all WARC record types.
    """
    try:
        total = _count_articles(warc_file)
    except ArchiveLoadFailed as exc:
        raise click.ClickException(
            f"Failed to read WARC file: {warc_file} -- is this a valid .warc or .warc.gz file?"
        ) from exc
    click.echo(f"Total articles: {total}")


@cli.command("get-index")
@click.option(
    "--date",
    default=None,
    help="Month to fetch in MM-YYYY format (defaults to current month).",
)
def get_index_cmd(date: str | None):
    """Download the CC-NEWS WARC index and list available files."""
    if date:
        try:
            year, month = parse_month_date(date)
        except ValueError as exc:
            raise click.ClickException(str(exc)) from exc
    else:
        now = datetime.now()
        year, month = now.year, now.month

    dest_dir = ".tmp"
    paths = fetch_warc_paths(year, month, dest_dir)

    click.echo(f"Found {len(paths)} WARC file(s) for {year}-{month:02d}:")
    for path in paths:
        click.echo(path)


@cli.command("get-warc")
@click.argument("warc_path")
@click.option(
    "--dest",
    default=".tmp",
    help="Destination directory for the downloaded file (defaults to .tmp).",
)
def get_warc_cmd(warc_path: str, dest: str):
    """Download a WARC file from the CC-NEWS dataset.

    WARC_PATH can be a relative path (e.g.
    crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz),
    a full URL, or a bare filename (requires a local index from get-index).
    """
    try:
        resolved = resolve_warc_path(warc_path, index_dir=dest)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    try:
        local_path = download_warc_by_path(resolved, dest)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc
    except urllib.error.HTTPError as exc:
        raise click.ClickException(
            f"Download failed (HTTP {exc.code}): {exc.url}\n"
            f"Hint: WARC_PATH should be a relative path like "
            f"'crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz'.\n"
            f"Run 'cc-news get-index' to see available files."
        ) from exc
    except OSError as exc:
        raise click.ClickException(
            f"Download failed: {exc}\n"
            f"Hint: WARC_PATH should be a relative path like "
            f"'crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz'.\n"
            f"Run 'cc-news get-index' to see available files."
        ) from exc

    click.echo(f"Downloaded: {local_path}")


if __name__ == "__main__":
    cli()
