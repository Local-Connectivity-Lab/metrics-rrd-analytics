## Stdlib
from typing import Dict, Optional, Tuple

## Local moduels
from . import rrd_meta_utils

## Whitelisted locations to include in our plots.
## Must match with `location`s as managed in our LibreNMS instance.
PHYS_LOCS = [
    'FCS',
    'lihi-southend',
    'nickelsville-cd',
    'northlake',
    'occ-oromo',
    'sps-franklin',
    'sps-garfield',
]

## Each value must be one of `PHYS_LOCS`.
PHYS_LOC_TO_LOGICAL_LOC = {
    'FCS': 'FCS',
    'lihi-southend': 'occ-oromo',
    'nickelsville-cd': 'sps-garfield',
    'northlake': 'northlake',
    'occ-oromo': 'occ-oromo',
    'sps-garfield': 'sps-garfield',
    'sps-franklin': 'sps-franklin',
}

## Key = one of PHYS_LOCS.
## Value = color hue, between 0 and 1.
LOC_TO_COLOR_H = {
    loc : i / len(PHYS_LOCS)
    for (i, loc) in enumerate(PHYS_LOCS)
}
