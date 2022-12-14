## Non-std libs
import matplotlib.pyplot as plt

## Local libs
from .. import graph_utils, rrd_utils

def graph():
    site_to_df = dict()
    for site in ['fcs', 'garfield', 'occ', 'tcn_surge']:
        rrd_relpath = rrd_utils.RRD_RELPATHS[site].uplink
        df = rrd_utils.rrd_to_pandas(rrd_relpath, '-6mon')
        site_to_df[site] = df

    fig, ax = plt.subplots()
    ax.set_title('EPC uplink data rate')
    for (site, df) in site_to_df.items():
        ax.plot(df['time'], df['INOCTETS'], label=f'{site} inbound')
        ax.plot(df['time'], df['OUTOCTETS'], label=f'{site} outbound')
    ax.set_ylabel('Byte/sec')
    ax.tick_params(axis='x', labelrotation=90)
    ax.xaxis.set_major_formatter(graph_utils.format_xtick_ts_as_date)
    ax.legend()
