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

## Key = one of PHYS_LOCS.
## Value = rgb color
LOC_TO_COLOR_H = {
    'FCS': '#ff7003', # orangish
    'lihi-southend': '#ff2ae6', # fuscia
    'nickelsville-cd': '#b78300', # brownish
    'northlake': '#82c04a', # greenish
    'occ-oromo': '#e30044', # red-pink
    'sps-franklin': '#002dec', # eye-hurting blue
    'sps-garfield': '#10bacd', # nicer blue
}
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
