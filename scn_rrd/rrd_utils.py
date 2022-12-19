## Stdlib
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
from typing import Dict, Tuple

## Non-std libs
from dotenv import dotenv_values
import pandas as pd
import rrdtool

DOTENV_ENTRIES = dotenv_values()

## nickname :: rrd filename
DEVICE_AGNOSTIC_RRD_FILENAMES = SimpleNamespace(
    latency='ping-perf.rrd',
    avail_weekly='availability-2592000.rrd',
)

DEVICES_PORTS_FILE='./data/devices_ports.csv'

def write_devices_ports(df: pd.DataFrame) -> None:
    os.makedirs(Path(DEVICES_PORTS_FILE).parent, exist_ok=True)
    df.to_csv(DEVICES_PORTS_FILE, index=False)

_cached_devices_ports: Tuple[float, pd.DataFrame] = None
def read_devices_ports() -> pd.DataFrame:
    global _cached_devices_ports
    mod_time = os.stat(DEVICES_PORTS_FILE).st_mtime
    if _cached_devices_ports is None or _cached_devices_ports[0] != mod_time:
        df = pd.read_csv(DEVICES_PORTS_FILE)
        _cached_devices_ports = (mod_time, df)
    return _cached_devices_ports[1]

def format_rrd_filepath(device_hostname: str, rrd_filename: str) -> str:
    return f"/opt/librenms/rrd/{device_hostname}/{rrd_filename}"

# Caveat: It's unknown whether scp causes some race condition with other procs writing to the file.
# We do have rrdcached enabled. An alternative is to query rrdcached api
#   (https://oss.oetiker.ch/rrdtool/doc/rrdcached.en.html#FETCH_filename_CF_[start_[end]_[ds_...]])
#   but then we'd have to netcat to it and parse raw bytes, rather than the convenient `rrdtool.fetch()`.
# Another anternative is to simply run all analyses on the nms server.
#   To do this, we need to provision more hardware from the cloud.
def download_rrd(remote_filepath: str, local_filepath: str) -> None:
    ssh_key_filepath = f"~/.ssh/{DOTENV_ENTRIES['SSH_KEY_FILENAME']}"
    nms_host = DOTENV_ENTRIES['NMS_HOST_NAME']
    remote_cmd = f"scp -i {ssh_key_filepath} {nms_host}:{remote_filepath} {local_filepath}"
    ret = os.system(remote_cmd)
    assert ret == 0

def rrd_to_dataframe(rrd_fullpath: str, start_time: str, end_time: str = None) -> pd.DataFrame:
    '''
    @arg start_time and end_time: https://oss.oetiker.ch/rrdtool/doc/rrdfetch.en.html#AT-STYLE_TIME_SPECIFICATION
        end_time defaults to the time of RRD's last received update.
    '''
    if end_time is None:
        info = rrdtool.info(rrd_fullpath)
        end_time = str(info['last_update'])

    ((start, end, step), ds, rows) = rrdtool.fetch(
        rrd_fullpath, 'AVERAGE',
        '--start', start_time,
        '--end', end_time)

    ts = range(start, end, step)    # `end` is exclusive.
    assert len(ts) == len(rows)

    ts = pd.to_datetime(ts, unit='s')
    df_cols = ('time',) + ds
    df_rows = ((t,) + row for (t, row) in zip(ts, rows))
    df = pd.DataFrame(data=df_rows, columns=df_cols)
    return df

def read_rrd(device_hostname: str, rrd_filename: str, start_time: str, end_time: str = None) -> pd.DataFrame:
    rrd_filepath = format_rrd_filepath(device_hostname, rrd_filename)

    with tempfile.NamedTemporaryFile() as f:
        download_rrd(rrd_filepath, f.name)

        return rrd_to_dataframe(f.name, start_time, end_time)
