## Stdlib
import os
import tempfile
from typing import Dict, List, Optional

## Non-std libs
import pandas as pd
import rrdtool

## Local modules
from .rrd_meta_utils import DOTENV_ENTRIES

def format_rrd_filepath(device_hostname: str, rrd_filename: str) -> str:
    return f"/opt/librenms/rrd/{device_hostname}/{rrd_filename}"

# Caveat: It's unknown whether scp causes some race condition with other procs writing to the file.
# We do have rrdcached enabled. An alternative is to query rrdcached api
#   (https://oss.oetiker.ch/rrdtool/doc/rrdcached.en.html#FETCH_filename_CF_[start_[end]_[ds_...]])
#   but then we'd have to netcat to it and parse raw bytes, rather than the convenient `rrdtool.fetch()`.
# Another anternative is to simply run all analyses on the nms server.
#   To do this, we need to provision more hardware from the cloud.
def download_rrd(remote_filepath: str, local_filepath: str) -> bool:
    '''
    @return bool: success
    '''
    ssh_key_filepath = f"~/.ssh/{DOTENV_ENTRIES['SSH_KEY_FILENAME']}"
    nms_host = DOTENV_ENTRIES['NMS_HOST_NAME']
    nms_user = DOTENV_ENTRIES['NMS_USER_NAME']
    scp_cmd = f"scp -i {ssh_key_filepath} {nms_user}@{nms_host}:{remote_filepath} {local_filepath}"
    ret = os.system(scp_cmd)
    return ret == 0

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

def read_rrd_via_scp(device_hostname: str, rrd_filename: str, start_time: str, end_time: str = None) -> Optional[pd.DataFrame]:
    rrd_filepath = format_rrd_filepath(device_hostname, rrd_filename)

    with tempfile.NamedTemporaryFile() as f:
        success = download_rrd(rrd_filepath, f.name)
        if success:
            return rrd_to_dataframe(f.name, start_time, end_time)
        else:
            return None

def read_rrds(device_hostnames: List[str], rrd_filename: str, start_time: str, end_time: str = None) -> Dict[str, pd.DataFrame]:
    ret = dict()
    for device_hostname in device_hostnames:
        rrd = read_rrd_via_scp(device_hostname, rrd_filename, start_time, end_time)
        if rrd is not None:
            ret[device_hostname] = rrd
    return ret
