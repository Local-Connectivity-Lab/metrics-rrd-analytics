## Stdlib
import os
from pathlib import Path
import sys
from types import SimpleNamespace
from typing import Tuple

## Non-std libs
from dotenv import dotenv_values
import pandas as pd

DOTENV_ENTRIES = dotenv_values()

DEVICE_AGNOSTIC_RRD_FILENAMES = SimpleNamespace(
    latency='ping-perf.rrd',
    avail_weekly='availability-2592000.rrd',
)

## Only eNB devices have these rrd files.
ENB_DEVICE_RRD_FILENAMES = SimpleNamespace(
    clients='wireless-sensor-clients-rts-1.rrd'
)

## Only MikroTik RouterOS devices have these rrd files.
MIKROTIK_DEVICE_RRD_FILENAMES = SimpleNamespace(
    clients='routeros_leases.rrd'
)

_META_FILEPATH='./data/meta.tsv'

def write_meta(df: pd.DataFrame) -> None:
    os.makedirs(Path(_META_FILEPATH).parent, exist_ok=True)
    df.to_csv(_META_FILEPATH, sep='\t', index=False)

_cached_meta: Tuple[float, pd.DataFrame] = None
def read_meta() -> pd.DataFrame:
    global _cached_meta
    try:
        mod_time = os.stat(_META_FILEPATH).st_mtime
    except FileNotFoundError as e:
        print('Please run 01-setup.ipynb to populate meta info about RRD files.', file=sys.stderr)
        raise e
    if _cached_meta is None or _cached_meta[0] != mod_time:
        meta_df = pd.read_csv(_META_FILEPATH, sep='\t')
        _cached_meta = (mod_time, meta_df)
    return _cached_meta[1]
