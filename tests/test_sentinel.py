import hashlib
from types import SimpleNamespace
from unittest.mock import Mock

import psutil

import sentinel


def test_get_file_hash_returns_sha256_of_source_file():
    expected_hash = hashlib.sha256()
    with open(sentinel.__file__, "rb") as source_file:
        expected_hash.update(source_file.read())

    assert sentinel.get_file_hash() == expected_hash.hexdigest()


def test_get_file_hash_returns_none_and_logs_error_when_file_cannot_be_read(
    monkeypatch,
):
    def raise_error(*args, **kwargs):
        raise OSError("cannot read source")

    monkeypatch.setattr("builtins.open", raise_error)
    logger = Mock()
    monkeypatch.setattr(sentinel.security_logger, "error", logger)

    assert sentinel.get_file_hash() is None
    logger.assert_called_once()
    assert "cannot read source" in logger.call_args.args[0]


def test_check_process_logs_only_processes_over_threshold(monkeypatch, caplog):
    processes = [
        SimpleNamespace(info={"name": "busy", "pid": 10, "cpu_percent": 12.5}),
        SimpleNamespace(info={"name": "idle", "pid": 11, "cpu_percent": 2.0}),
    ]
    monkeypatch.setattr(sentinel.psutil, "process_iter", lambda fields: processes)

    with caplog.at_level("WARNING", logger="process_monitor"):
        sentinel.check_process(threshold=10.0)

    assert "busy (PID: 10)" in caplog.text
    assert "idle (PID: 11)" not in caplog.text


def test_check_process_ignores_processes_that_disappear(monkeypatch):
    class DisappearingProcess:
        info = {"name": "gone", "pid": 12, "cpu_percent": 20.0}

        @property
        def info(self):
            raise psutil.NoSuchProcess(pid=12)

    monkeypatch.setattr(
        sentinel.psutil,
        "process_iter",
        lambda fields: [DisappearingProcess()],
    )

    sentinel.check_process(threshold=10.0)


def test_check_network_logs_listening_ports_and_flags_port_4444(
    monkeypatch, caplog
):
    connections = [
        SimpleNamespace(
            status="LISTEN",
            laddr=SimpleNamespace(port=8080, ip="127.0.0.1"),
        ),
        SimpleNamespace(
            status="LISTEN",
            laddr=SimpleNamespace(port=4444, ip="0.0.0.0"),
        ),
        SimpleNamespace(
            status="ESTABLISHED",
            laddr=SimpleNamespace(port=5555, ip="127.0.0.1"),
        ),
    ]
    monkeypatch.setattr(
        sentinel.psutil,
        "net_connections",
        lambda kind: connections,
    )

    with caplog.at_level("INFO", logger="network_monitor"):
        sentinel.check_network()

    assert "Port Listening: 8080 on IP: 127.0.0.1" in caplog.text
    assert "Port Listening: 4444 on IP: 0.0.0.0" in caplog.text
    assert "Potential Malicious Port 4444 detected" in caplog.text
    assert "Port Listening: 5555" not in caplog.text
