## Stdlib
import os
from types import SimpleNamespace

## Non-std libs
import pandas as pd
import rrdtool

RRD_DIRPATH_PROD = '/opt/librenms/rrd'
RRD_DIRPATH_LOCAL = './data'

## site :: nickname :: rrd relative file path
RRD_RELPATHS = {
    'fcs': SimpleNamespace(
        uplink='fcs1/port-id1874.rrd',
        avail_weekly='fcs1/availability-2592000.rrd',
    ),
    'garfield': SimpleNamespace(
        uplink='sps-garfield/port-id190.rrd',
        avail_weekly='sps-garfield/availability-2592000.rrd',
    ),
    'occ': SimpleNamespace(
        uplink='scn-occ/port-id5175.rrd',
        avail_weekly='scn-occ/availability-2592000.rrd',
    ),
    'tcn_surge': SimpleNamespace(
        uplink='tcn-surge/port-id507.rrd',
        avail_weekly='tcn-surge/availability-2592000.rrd',
    )
}

def rrd_path(relpath: str, dirpath: str = RRD_DIRPATH_LOCAL) -> str:
    return f'{dirpath}/{relpath}'

def rrd_to_pandas(rrd_relpath: str, start_time: str, end_time: str = None) -> pd.DataFrame:
    '''
    @arg rrd_relpath: RRD_RELPATHS.foo.bar
    @arg start_time and end_time: https://oss.oetiker.ch/rrdtool/doc/rrdfetch.en.html#AT-STYLE_TIME_SPECIFICATION
        end_time defaults to RRD's last received update.
    '''
    rrd_fullpath = rrd_path(rrd_relpath)
    info = rrdtool.info(rrd_fullpath)

    if end_time is None:
        end_time = str(info['last_update'])

    ((start, end, step), ds, rows) = rrdtool.fetch(
        rrd_fullpath, 'AVERAGE',
        '--start', start_time,
        '--end', end_time)

    ts = range(start, end, step)

    assert len(ts) == len(rows)

    ret_cols = ('time',) + ds
    ret_rows = ((t,) + row for (t, row) in zip(ts, rows))
    df = pd.DataFrame(ret_rows, columns=ret_cols)
    return df
