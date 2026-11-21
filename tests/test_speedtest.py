"""Tests for speedtest.py.

Three layers, all deterministic and CI-safe:
  * pure-function unit tests  -> format_report, parse_args
  * mocked-request unit test  -> measure() loop logic (no real network)
  * hermetic integration test -> real HTTP against a localhost http.server
"""

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest import mock

import pytest

import speedtest


# --------------------------------------------------------------------------- #
# Pure-function unit tests
# --------------------------------------------------------------------------- #

def test_format_report_computes_speed_and_average():
    # 15 MB over 3 requests in 3.0 s total -> 5.00 MB/s, avg 1.000 s
    report = speedtest.format_report(
        "http://x", n=3, total_bytes=15_000_000, total_time=3.0
    )
    assert "Total downloaded:     15.00 MB" in report
    assert "Average request time: 1.000 s" in report
    assert "Download speed:       5.00 MB/s" in report


def test_format_report_handles_zero_time():
    report = speedtest.format_report(
        "http://x", n=1, total_bytes=1000, total_time=0.0
    )
    assert "n/a" in report  # guarded against division by zero


def test_parse_args_defaults():
    args = speedtest.parse_args(["http://example.com"])
    assert args.url == "http://example.com"
    assert args.count == speedtest.DEFAULT_REQUESTS  # 10
    assert args.timeout == speedtest.DEFAULT_TIMEOUT


def test_parse_args_rejects_non_positive_count():
    with pytest.raises(SystemExit):  # argparse error -> SystemExit
        speedtest.parse_args(["http://example.com", "-n", "0"])


# --------------------------------------------------------------------------- #
# Mocked-request unit test: measure() loop logic
# --------------------------------------------------------------------------- #

def test_measure_runs_n_times_and_aggregates():
    fake_response = mock.Mock()
    fake_response.content = b"x" * 2048        # 2048 bytes per request
    fake_response.raise_for_status = mock.Mock()

    with mock.patch("speedtest.requests.get", return_value=fake_response) as get:
        total_bytes, total_time = speedtest.measure("http://x", n=4, timeout=5)

    assert get.call_count == 4                 # exactly N sequential requests
    assert total_bytes == 2048 * 4
    assert total_time >= 0.0


# --------------------------------------------------------------------------- #
# Hermetic integration test: real HTTP against a localhost server
# --------------------------------------------------------------------------- #

PAYLOAD = b"y" * 100_000  # 100 KB fixed payload


class _FixedPayloadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(len(PAYLOAD)))
        self.end_headers()
        self.wfile.write(PAYLOAD)

    def log_message(self, *args):  # silence server logging during tests
        pass


@pytest.fixture
def local_server():
    server = HTTPServer(("127.0.0.1", 0), _FixedPayloadHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}/"
    finally:
        server.shutdown()
        server.server_close()


def test_measure_against_local_server(local_server):
    total_bytes, total_time = speedtest.measure(local_server, n=3, timeout=10)
    assert total_bytes == len(PAYLOAD) * 3
    assert total_time > 0.0


def test_main_exits_zero_on_success(local_server, capsys):
    exit_code = speedtest.main([local_server, "-n", "2"])
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Download speed:" in out
    assert "MB/s" in out
