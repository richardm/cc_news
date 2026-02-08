"""CLI entrypoint for CC News Analyzer."""

from datetime import datetime

import click

from cc_news_analyzer.index import fetch_warc_paths, parse_month_date
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


if __name__ == "__main__":
    cli()
