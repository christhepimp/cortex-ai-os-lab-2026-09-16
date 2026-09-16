#!/usr/bin/env python3
"""Cortex supervisor stub.

Talks to a rooted emulator over adb. Observes Linux/Android state.
Does not replace the kernel. Dry-run by default.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys


def adb(*args: str) -> str:
    cmd = ["adb", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"adb failed: {cmd}")
    return proc.stdout.strip()


def snapshot() -> dict[str, str]:
    keys = {
        "uname": ["shell", "uname", "-a"],
        "id": ["shell", "id"],
        "release": ["shell", "getprop", "ro.build.version.release"],
        "kernel": ["shell", "cat", "/proc/version"],
    }
    out = {}
    for name, args in keys.items():
        try:
            out[name] = adb(*args)
        except Exception as exc:  # noqa: BLE001
            out[name] = f"error: {exc}"
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Cortex AI OS lab supervisor")
    parser.add_argument("--live", action="store_true", help="require adb; default also works as dry demo")
    args = parser.parse_args()

    print("Cortex lab supervisor")
    print("Policy: observe only. Linux kernel stays.")

    if not shutil.which("adb"):
        print("adb not on PATH. Install platform-tools, then rerun --live.")
        if args.live:
            return 2
        print("Dry snapshot:")
        print("  uname: (no emulator)")
        return 0

    try:
        devices = adb("devices")
        print(devices)
        snap = snapshot()
        for k, v in snap.items():
            print(f"{k}: {v}")
    except Exception as exc:  # noqa: BLE001
        print(f"adb error: {exc}")
        return 1 if args.live else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
