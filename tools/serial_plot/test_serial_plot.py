"""Tests for SampleReader using pyserial's loop:// virtual port."""

import serial

from serial_plot import SampleReader


def make_reader():
    port = serial.serial_for_url("loop://", 115200, timeout=0)
    return port, SampleReader(port)


def test_empty_port_returns_nothing():
    _, reader = make_reader()
    assert reader.poll() == []


def test_partial_line_waits_for_newline():
    port, reader = make_reader()
    port.write(b"12")
    assert reader.poll() == []
    port.write(b"3\r\n")
    assert reader.poll() == [123]


def test_multiple_lines_and_blank_lines():
    port, reader = make_reader()
    port.write(b"1\r\n2\n\r\n3\n")
    assert reader.poll() == [1, 2, 3]


def test_garbage_is_skipped(capsys):
    port, reader = make_reader()
    port.write(b"ets Jun  8 2016 boot\r\n\xff\xfe\n42\n")
    assert reader.poll() == [42]
    assert "skipped" in capsys.readouterr().err
