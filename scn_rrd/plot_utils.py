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

LOGICAL_LOC_TO_PHYS_LOCS = {
    'FCS': ['FCS'],
    'northlake': ['northlake'],
    'occ-oromo': ['occ-oromo', 'lihi-southend'],
    'sps-franklin': ['sps-franklin'],
    'sps-garfield': ['sps-garfield', 'nickelsville-cd']
}

PHYS_LOC_TO_LOGICAL_LOC = {
    phy: logi
    for (logi, phys) in LOGICAL_LOC_TO_PHYS_LOCS.items()
    for phy in phys
}

## Key = one of PHYS_LOCS.
## Value = color hue, between 0 and 1.
LOC_TO_COLOR_H = {
    loc : i / len(PHYS_LOCS)
    for (i, loc) in enumerate(PHYS_LOCS)
}
