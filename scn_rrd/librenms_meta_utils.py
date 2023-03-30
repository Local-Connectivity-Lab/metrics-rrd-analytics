## Stdlib
import os
from pathlib import Path
import sys
from typing import Optional, Tuple

## Non-std libs
import pandas as pd

_META_FILEPATH = './data/meta.tsv'

def write_meta(df: pd.DataFrame) -> None:
    os.makedirs(Path(_META_FILEPATH).parent, exist_ok=True)
    df.to_csv(_META_FILEPATH, sep='\t', index=False)

def meta_mod_time() -> float:
    try:
        return os.stat(_META_FILEPATH).st_mtime
    except FileNotFoundError as e:
        print('Please run 01-setup.ipynb to populate meta info about RRD files.', file=sys.stderr)
        raise e

## (mod_time, df)
_cached_meta: Optional[ Tuple[float, pd.DataFrame] ] = None

def read_meta() -> pd.DataFrame:
    global _cached_meta
    mod_time = meta_mod_time()
    if _cached_meta is None or _cached_meta[0] != mod_time:
        meta_df = pd.read_csv(_META_FILEPATH, sep='\t')
        _cached_meta = (mod_time, meta_df)
    return _cached_meta[1]
