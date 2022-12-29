## A module containing an alternative way to retrieve RRD info, by running `rrdtool fetch` remotely then parsing its stdout locally.

## Stdlib
import re
import subprocess
from typing import List, Optional

## Non-std libs
import pandas as pd

def read_rrd_via_stdout(
    remote_host: str, remote_user: str, remote_pw: str,
    rrd_filepath: str, start_time: str, end_time: str = None,
) -> Optional[pd.DataFrame]:
    '''
    @arg start_time and end_time: https://oss.oetiker.ch/rrdtool/doc/rrdfetch.en.html#AT-STYLE_TIME_SPECIFICATION
        end_time defaults to 'now'.
    '''
    if end_time is None:
        end_time = 'now'

    remote_cmd = [
        'sshpass', '-p', f"{remote_pw}",
        'ssh', f"{remote_user}@{remote_host}",
        f"rrdtool fetch {rrd_filepath} AVERAGE --start {start_time} --end {end_time}"
    ]
    proc_res = subprocess.run(remote_cmd, stdout=subprocess.PIPE)

    stdout_str = proc_res.stdout.decode('ascii')
    stdout_lines = stdout_str.split('\n')
    (ds_names_line, _empty_line, *row_lines) = stdout_lines

    ds_names = re.split('\s+', ds_names_line)
    ds_names = list(filter(None, ds_names))
    ds_names = ['time'] + ds_names

    rows = []
    row_lines = filter(None, row_lines)
    for row_line in row_lines:
        tokens = re.split('\s+', row_line)
        if tokens[0].endswith(':'):
            tokens[0] = tokens[0][:-1]
        tokens[0] = int(tokens[0])
        for j in range(1, len(tokens)):
            tokens[j] = float(tokens[j])
        rows.append(tokens)

    df = pd.DataFrame(data=rows, columns=ds_names)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
    