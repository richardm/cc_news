"""Functions for working with CC-NEWS WARC index files."""

import gzip
import os
import shutil
import urllib.request
from datetime import datetime

CC_NEWS_BASE_URL = "https://data.commoncrawl.org"


def parse_month_date(date_str: str) -> tuple[int, int]:
    """Parse a ``MM-YYYY`` date string into (year, month).

    Args:
        date_str: A date string in ``MM-YYYY`` format (e.g. ``"02-2026"``).

    Returns:
        A tuple of ``(year, month)`` as integers.

    Raises:
        ValueError: If the string is not in ``MM-YYYY`` format or the values
            are out of range.
    """
    if not date_str or "-" not in date_str:
        raise ValueError(f"Invalid date format: {date_str!r}. Expected MM-YYYY.")

    parts = date_str.split("-")
    if len(parts) != 2:
        raise ValueError(f"Invalid date format: {date_str!r}. Expected MM-YYYY.")

    mm_str, yyyy_str = parts

    if len(mm_str) != 2 or len(yyyy_str) != 4:
        raise ValueError(f"Invalid date format: {date_str!r}. Expected MM-YYYY.")

    try:
        month = int(mm_str)
        year = int(yyyy_str)
    except ValueError:
        raise ValueError(
            f"Invalid date format: {date_str!r}. Expected MM-YYYY."
        ) from None

    if month < 1 or month > 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")

    return year, month


def build_index_url(year: int, month: int) -> str:
    """Build the CC-NEWS WARC index URL for a given year and month.

    Args:
        year: The four-digit year (e.g. 2026).
        month: The month number (1-12).

    Returns:
        The full URL to the gzipped WARC paths index file.

    Raises:
        ValueError: If year or month are out of reasonable range.
    """
    if year < 2016 or year > 2030:
        raise ValueError(f"Year must be between 2016 and 2030, got {year}")
    if month < 1 or month > 12:
        raise ValueError(f"Month must be between 1 and 12, got {month}")

    return f"{CC_NEWS_BASE_URL}/crawl-data/CC-NEWS/{year}/{month:02d}/warc.paths.gz"


def build_current_month_index_url() -> str:
    """Build the CC-NEWS WARC index URL for the current month.

    Returns:
        The full URL to the gzipped WARC paths index file for the current month.
    """
    now = datetime.now()
    return build_index_url(now.year, now.month)


def fetch_warc_paths(year: int, month: int, dest_dir: str) -> list[str]:
    """Download the CC-NEWS index for a given month and return the WARC paths.

    Downloads the gzipped index file, decompresses it, and parses the list of
    relative WARC paths.

    Args:
        year: The four-digit year.
        month: The month number (1-12).
        dest_dir: Directory to store the downloaded index files.

    Returns:
        A list of relative WARC paths (e.g.
        ``"crawl-data/CC-NEWS/2026/02/CC-NEWS-20260201022924-06627.warc.gz"``).

    Raises:
        ValueError: If year or month are out of range.
        OSError: If the download or decompression fails.
    """
    os.makedirs(dest_dir, exist_ok=True)

    index_url = build_index_url(year, month)
    gz_path = os.path.join(dest_dir, "warc.paths.gz")
    txt_path = os.path.join(dest_dir, "warc.paths")

    # Download the gzipped index
    urllib.request.urlretrieve(index_url, gz_path)

    # Decompress
    with gzip.open(gz_path, "rb") as f_in, open(txt_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

    # Parse paths
    with open(txt_path) as f:
        paths = [line.strip() for line in f if line.strip()]

    return paths


def download_warc_by_path(warc_path: str, dest_dir: str) -> str:
    """Download a WARC file given its relative path in the CC-NEWS dataset.

    The relative path is the format returned by :func:`fetch_warc_paths`, e.g.
    ``"crawl-data/CC-NEWS/2026/02/CC-NEWS-20260204051206-06668.warc.gz"``.

    Args:
        warc_path: Relative WARC path within the Common Crawl dataset.
        dest_dir: Directory where the file should be saved.

    Returns:
        The local file path of the downloaded WARC file.

    Raises:
        ValueError: If *warc_path* is empty or has no filename component.
        OSError: If the download fails.
    """
    if not warc_path or not warc_path.strip():
        raise ValueError("WARC path must not be empty.")

    filename = os.path.basename(warc_path.strip())
    if not filename:
        raise ValueError(f"Cannot determine filename from WARC path: {warc_path!r}")

    url = f"{CC_NEWS_BASE_URL}/{warc_path.strip()}"
    return download_warc(url, dest_dir)


def build_warc_urls(warc_paths: list[str]) -> list[str]:
    """Convert relative WARC paths to full download URLs.

    Args:
        warc_paths: List of relative WARC paths as returned by
            :func:`fetch_warc_paths`.

    Returns:
        A list of full download URLs.
    """
    return [f"{CC_NEWS_BASE_URL}/{path}" for path in warc_paths]


def download_warc(url: str, dest_dir: str) -> str:
    """Download a WARC file from the given URL.

    Args:
        url: The full URL to the WARC file.
        dest_dir: Directory where the file should be saved.

    Returns:
        The local file path of the downloaded WARC file.

    Raises:
        OSError: If the download fails.
    """
    os.makedirs(dest_dir, exist_ok=True)

    filename = os.path.basename(url)
    if not filename:
        raise ValueError(f"Cannot determine filename from URL: {url}")

    dest_path = os.path.join(dest_dir, filename)
    urllib.request.urlretrieve(url, dest_path)

    return dest_path
