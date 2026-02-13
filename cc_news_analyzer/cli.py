"""CLI entrypoint for CC News Analyzer."""

from datetime import datetime

import click

from cc_news_analyzer.index import (
    download_warc_by_path,
    fetch_warc_paths,
    parse_month_date,
)
from cc_news_analyzer.warc import count_articles as _count_articles
from cc_news_analyzer.warc import count_records as _count_records


@click.group()
def cli():
    """CC News Analyzer - Analyze Common Crawl News WARC datasets."""
    pass


@cli.command("count-records")
@click.argument("warc_file", type=click.Path(exists=True))
def count_records_cmd(warc_file: str):
    """Count the number of WARC records with a WARC-Record-ID in a file."""
    total = _count_records(warc_file)
    click.echo(f"Total WARC records with WARC-Record-ID: {total}")


@cli.command("count-articles")
@click.argument("warc_file", type=click.Path(exists=True))
def count_articles_cmd(warc_file: str):
    """Count article records (HTML responses) in a WARC file.

    Articles are WARC response records with an HTML content type.
    This is distinct from count-records, which counts all WARC record types.
    """
    total = _count_articles(warc_file)
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
    """Download a WARC file from the CC-NEWS dataset by its relative path.

    WARC_PATH is the relative path, e.g.
    crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz
    """
    try:
        local_path = download_warc_by_path(warc_path, dest)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Downloaded: {local_path}")


if __name__ == "__main__":
    cli()
