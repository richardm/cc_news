"""CLI entrypoint for CC News Analyzer."""

import click

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


if __name__ == "__main__":
    cli()
