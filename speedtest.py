#!/usr/bin/env python3
"""Measure download speed by repeatedly downloading a URL.

Makes N sequential HTTP GET requests to a target URL (e.g. a heavy image),
fully downloading each response, then reports the total data downloaded,
the average time per request, and the download speed in MB/s.
"""

import argparse
import sys
import time

import requests

DEFAULT_REQUESTS = 10
DEFAULT_TIMEOUT = 30  # seconds
BYTES_PER_MB = 1_000_000  # decimal megabyte (see README for why decimal)


def download_once(url, timeout):
    """Download the URL once, returning (elapsed_seconds, num_bytes).

    Reads the full response body so the measured time covers the entire
    download, not just the time to first byte.
    """
    start = time.perf_counter()
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    num_bytes = len(response.content)  # .content reads the whole body
    elapsed = time.perf_counter() - start
    return elapsed, num_bytes


def measure(url, n, timeout):
    """Run n sequential downloads and return aggregate statistics."""
    total_bytes = 0
    total_time = 0.0

    for i in range(1, n + 1):
        elapsed, num_bytes = download_once(url, timeout)
        total_bytes += num_bytes
        total_time += elapsed
        print(
            f"  request {i}/{n}: {num_bytes / BYTES_PER_MB:.2f} MB in {elapsed:.3f} s"
        )

    return total_bytes, total_time


def format_report(url, n, total_bytes, total_time):
    """Build the human-readable summary report."""
    avg_time = total_time / n

    if total_time > 0:
        speed_mbps = (total_bytes / BYTES_PER_MB) / total_time
        speed_line = f"Download speed:       {speed_mbps:.2f} MB/s"
    else:
        # Guard against a division by zero on absurdly fast/cached responses.
        speed_line = "Download speed:       n/a (total time was zero)"

    return "\n".join(
        [
            "",
            f"Target:               {url}",
            f"Requests:             {n}",
            f"Total downloaded:     {total_bytes / BYTES_PER_MB:.2f} MB",
            f"Average request time: {avg_time:.3f} s",
            speed_line,
        ]
    )


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Measure download speed by repeatedly downloading a URL."
    )
    parser.add_argument(
        "url",
        help="URL to download, e.g. a heavy image",
    )
    parser.add_argument(
        "-n",
        "--requests",
        type=int,
        default=DEFAULT_REQUESTS,
        dest="count",
        help=f"number of sequential requests (default: {DEFAULT_REQUESTS})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"per-request timeout in seconds (default: {DEFAULT_TIMEOUT})",
    )
    args = parser.parse_args(argv)

    if args.count < 1:
        parser.error("--requests must be at least 1")

    return args


def main(argv=None):
    args = parse_args(argv)

    print(f"Downloading {args.url} {args.count} times...")
    try:
        total_bytes, total_time = measure(args.url, args.count, args.timeout)
    except requests.RequestException as exc:
        print(f"Error: request failed: {exc}", file=sys.stderr)
        return 1

    if total_bytes == 0:
        print("Error: downloaded 0 bytes; nothing to measure.", file=sys.stderr)
        return 1

    print(format_report(args.url, args.count, total_bytes, total_time))
    return 0


if __name__ == "__main__":
    sys.exit(main())
