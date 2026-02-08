"""Functions for analyzing WARC files."""

import os
from typing import Any

from warcio.archiveiterator import ArchiveIterator


def list_warc_files(directory: str) -> list[dict[str, Any]]:
    """List WARC files in a directory with basic metadata.

    Scans the given directory (non-recursively) for files ending in ``.warc``
    or ``.warc.gz`` and returns their names and sizes.

    Args:
        directory: Path to the directory to scan.

    Returns:
        A list of dicts, each containing:
            - ``name`` (str): The filename.
            - ``path`` (str): The full file path.
            - ``size_bytes`` (int): File size in bytes.
            - ``size_mb`` (float): File size in megabytes, rounded to 1 decimal.

    Raises:
        FileNotFoundError: If the directory does not exist.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    results: list[dict[str, Any]] = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith((".warc", ".warc.gz")):
            full_path = os.path.join(directory, filename)
            size_bytes = os.path.getsize(full_path)
            results.append({
                "name": filename,
                "path": full_path,
                "size_bytes": size_bytes,
                "size_mb": round(size_bytes / (1024 * 1024), 1),
            })

    return results


def count_records(warc_path: str) -> int:
    """Count WARC records that have a WARC-Record-ID header.

    Args:
        warc_path: Path to a ``.warc`` or ``.warc.gz`` file.

    Returns:
        The number of records containing a ``WARC-Record-ID`` header.

    Raises:
        FileNotFoundError: If the WARC file does not exist.
    """
    if not os.path.isfile(warc_path):
        raise FileNotFoundError(f"WARC file not found: {warc_path}")

    count = 0
    with open(warc_path, "rb") as f:
        for record in ArchiveIterator(f):
            if record.rec_headers.get_header("WARC-Record-ID"):
                count += 1

    return count
