## Stdlib
from datetime import datetime

def format_xtick_ts(sec_since_epoch: int, _tick_pos: int) -> str:
    return datetime.fromtimestamp(sec_since_epoch)

def format_xtick_ts_as_date(sec_since_epoch: int, _tick_pos: int) -> str:
    return datetime.fromtimestamp(sec_since_epoch).strftime('%Y-%m-%d')
