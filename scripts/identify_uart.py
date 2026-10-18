#!/usr/bin/env python3
"""Read-only Klipper MCU identity/status probe; stop Klipper before using.

Run with the Klipper virtualenv Python. Set KLIPPER_DIR if ~/klipper differs.
Use an outer timeout as documented because connect_uart retries internally.
No flash, restart, configuration, motion, output or heating commands are sent.
Based on the independent probe used successfully for this installation.
"""
import json
import logging
import os
from pathlib import Path
import sys

klipper_dir = Path(os.environ.get("KLIPPER_DIR", str(Path.home() / "klipper")))
sys.path.insert(0, str(klipper_dir / "klippy"))
import reactor
import serialhdl

logging.basicConfig(level=logging.WARNING)
r = reactor.Reactor()
s = serialhdl.SerialReader(r)
result = {"port": "/dev/serial0", "baud": 250000, "pass": False}

def check(eventtime):
    try:
        s.connect_uart(result["port"], result["baud"])
        parser = s.get_msgparser()
        version, build = parser.get_version_info()
        constants = parser.get_constants()
        result.update(version=version, build=build, constants=constants)
        assert constants["MCU"] == "stm32f401xc", "Unexpected MCU"
        assert constants["RESERVE_PINS_serial"] == "PA3,PA2", "Unexpected UART pins"
        assert constants["SERIAL_BAUD"] == 250000, "Unexpected MCU baud"
        replies = []
        queries = [("get_config", "config"), ("get_uptime", "uptime")]
        queries += [("get_clock", "clock")] * 20
        for command, response in queries:
            replies.append({"command": command,
                            "reply": s.send_with_response(command, response)})
            r.pause(r.monotonic() + 0.03)
        result.update(replies=replies, stats=s.stats(r.monotonic()), **{"pass": True})
    except Exception as exc:
        result["error"] = str(exc)
    finally:
        s.disconnect()
        r.end()

r.register_callback(check)
r.run()
r.finalize()
Path("uart-identity-result.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
sys.exit(0 if result["pass"] else 1)
