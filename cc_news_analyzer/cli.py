"""CLI entrypoint for CC News Analyzer."""

import click
from warcio.archiveiterator import ArchiveIterator


@click.group()
def cli():
    """CC News Analyzer - Analyze Common Crawl News WARC datasets."""
    pass


@cli.command("count-records")
@click.argument("warc_file", type=click.Path(exists=True))
def count_records(warc_file: str):
    """Count the number of WARC records with a WARC-Record-ID in a file."""
    count = 0
    with open(warc_file, "rb") as f:
        for record in ArchiveIterator(f):
            if record.rec_headers.get_header("WARC-Record-ID"):
                count += 1
    click.echo(f"Total WARC records with WARC-Record-ID: {count}")


if __name__ == "__main__":
    cli()
