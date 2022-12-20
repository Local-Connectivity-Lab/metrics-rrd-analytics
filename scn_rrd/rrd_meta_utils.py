## Stdlib
import os
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Tuple

## Non-std libs
import pandas as pd

## nickname :: rrd filename
DEVICE_AGNOSTIC_RRD_FILENAMES = SimpleNamespace(
    latency='ping-perf.rrd',
    avail_weekly='availability-2592000.rrd',
)

_DEVICES_PORTS_FILE='./data/devices_ports.csv'

def write_devices_ports(df: pd.DataFrame) -> None:
    os.makedirs(Path(_DEVICES_PORTS_FILE).parent, exist_ok=True)
    df.to_csv(_DEVICES_PORTS_FILE, index=False)

_cached_devices_ports: Tuple[float, pd.DataFrame] = None
def read_devices_ports() -> pd.DataFrame:
    global _cached_devices_ports
    try:
        mod_time = os.stat(_DEVICES_PORTS_FILE).st_mtime
    except FileNotFoundError as e:
        print('Please run 01-setup.ipynb to populate meta info about RRD files.', file=sys.stderr)
        raise e
    if _cached_devices_ports is None or _cached_devices_ports[0] != mod_time:
        df = pd.read_csv(_DEVICES_PORTS_FILE)
        _cached_devices_ports = (mod_time, df)
    return _cached_devices_ports[1]
