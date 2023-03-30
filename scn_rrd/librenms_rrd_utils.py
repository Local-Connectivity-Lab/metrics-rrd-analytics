## Stdlib
from types import SimpleNamespace
from typing import Dict, List

## Non-std libs
import pandas as pd

## Local modules
from .config import DOTENV_ENTRIES
from . import rrd_utils

DEVICE_AGNOSTIC_RRD_FILENAMES = SimpleNamespace(
    latency='ping-perf.rrd',
    avail_weekly='availability-2592000.rrd',
    avail_daily='availability-86400.rrd',
)

## Only eNB devices have these rrd files.
ENB_DEVICE_RRD_FILENAMES = SimpleNamespace(
    clients='wireless-sensor-clients-rts-1.rrd'
)

## Only MikroTik RouterOS devices have these rrd files.
MIKROTIK_DEVICE_RRD_FILENAMES = SimpleNamespace(
    clients='routeros_leases.rrd'
)

def format_rrd_filepath(device_hostname: str, rrd_filename: str) -> str:
    '''
    LibreNMS manages RRD files as
        `/opt/librenms/rrd/<device_ip_or_hostname>/<foo>.rrd`.
    `rrdcached` is config'd w/ base dir at `/opt/librenms/rrd`.
    Hence, we query `rrdcached` with a filepath like
        `<device_ip_or_hostanme>/<foo>.rrd`.
    '''
    return f"{device_hostname}/{rrd_filename}"

def read_rrds(device_hostnames: List[str], rrd_filename: str, start_time: str, end_time: str = None) -> Dict[str, pd.DataFrame]:
    ret = dict()
    for device_hostname in device_hostnames:
        rrd_filepath = format_rrd_filepath(device_hostname, rrd_filename)
        pd = rrd_utils.read_rrd(DOTENV_ENTRIES['NMS_HOST_IP'], rrd_filepath, start_time, end_time)
        if pd is not None:
            ret[device_hostname] = pd
    return ret
