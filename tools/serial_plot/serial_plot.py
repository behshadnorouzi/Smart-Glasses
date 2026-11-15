"""Live plot of integer samples received over a serial port.

The device is expected to send one integer per line, as the
firmware/analog_monitor sketch does. Close the plot window to stop.

    python serial_plot.py --port COM10
    python serial_plot.py --port /dev/ttyUSB0 --window 500
"""

import argparse
import sys
import time
from collections import deque

import matplotlib.pyplot as plt
import serial
from matplotlib.animation import FuncAnimation


class SampleReader:
    """Reads newline-terminated integers from a serial port without blocking."""

    def __init__(self, port):
        self._port = port
        self._pending = bytearray()

    def poll(self):
        """Return the list of integers received since the last call."""
        self._pending.extend(self._port.read(self._port.in_waiting))
        *lines, self._pending = self._pending.split(b"\n")

        samples = []
        for raw in lines:
            text = raw.strip()
            if not text:
                continue
            try:
                samples.append(int(text))
            except ValueError:
                # Partial line after reset or boot messages from the board.
                print(f"skipped: {bytes(text)!r}", file=sys.stderr)
        return samples


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--port", required=True, help="serial port, e.g. COM10 or /dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=115200, help="baud rate (default: 115200)")
    parser.add_argument("--window", type=int, default=300, help="number of samples shown (default: 300)")
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        port = serial.serial_for_url(args.port, args.baud, timeout=0)
    except serial.SerialException as exc:
        sys.exit(f"cannot open {args.port}: {exc}")

    reader = SampleReader(port)
    times = deque(maxlen=args.window)
    values = deque(maxlen=args.window)
    start = time.monotonic()

    fig, ax = plt.subplots()
    (line,) = ax.plot([], [], linewidth=1)
    ax.set_title(f"{args.port} @ {args.baud} baud")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("ADC reading")
    ax.grid(True, alpha=0.3)

    def update(_frame):
        samples = reader.poll()
        if samples:
            now = time.monotonic() - start
            times.extend([now] * len(samples))
            values.extend(samples)
            line.set_data(times, values)
            ax.relim()
            ax.autoscale_view()
        return (line,)

    # Keep a reference, otherwise the animation is garbage-collected.
    _animation = FuncAnimation(fig, update, interval=50, cache_frame_data=False)

    try:
        plt.show()
    finally:
        port.close()


if __name__ == "__main__":
    main()
