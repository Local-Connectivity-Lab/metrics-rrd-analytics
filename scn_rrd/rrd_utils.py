## Stdlib
from enum import StrEnum
import os
from typing import Dict
from types import SimpleNamespace

## Non-std libs
import pandas as pd
import rrdtool

class RrdDirpath(StrEnum):
    PROD = '/opt/librenms/rrd'
    LOCAL = './data'

## site :: nickname :: rrd relative file path
RRD_RELPATHS = {
    'fcs': SimpleNamespace(
        uplink='fcs1/port-id1874.rrd',
        avail_weekly='fcs1/availability-2592000.rrd',
        ping='fcs1/ping-perf.rrd',
    ),
    'garfield': SimpleNamespace(
        uplink='sps-garfield/port-id190.rrd',
        avail_weekly='sps-garfield/availability-2592000.rrd',
        ping='sps-garfield/ping-perf.rrd',
    ),
    'occ': SimpleNamespace(
        uplink='scn-occ/port-id5175.rrd',
        avail_weekly='scn-occ/availability-2592000.rrd',
        ping='scn-occ/ping-perf.rrd',
    ),
    'tcn_surge': SimpleNamespace(
        uplink='tcn-surge/port-id507.rrd',
        avail_weekly='tcn-surge/availability-2592000.rrd',
        ping='tcn-surge/ping-perf.rrd',
    )
}

def rrd_path(dirpath: RrdDirpath, relpath: str) -> str:
    return f'{dirpath}/{relpath}'

def rrd_to_dataframe(rrd_relpath: str, start_time: str, end_time: str = None) -> pd.DataFrame:
    '''
    @arg rrd_relpath: RRD_RELPATHS.foo.bar
    @arg start_time and end_time: https://oss.oetiker.ch/rrdtool/doc/rrdfetch.en.html#AT-STYLE_TIME_SPECIFICATION
        end_time defaults to the time of RRD's last received update.
    '''
    rrd_fullpath = rrd_path(RrdDirpath.LOCAL, rrd_relpath)

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

def collect_rrd_dataframes(nickname: str, start_time: str, end_time: str = None) -> Dict[str, pd.DataFrame]:
    site_to_df = dict()
    for (site, nickname_to_relpath) in RRD_RELPATHS.items():
        rrd_relpath = getattr(nickname_to_relpath, nickname)
        if rrd_relpath is not None:
            df = rrd_to_dataframe(rrd_relpath, start_time, end_time)
            site_to_df[site] = df
    return site_to_df
