## Non-std libs
from dotenv import dotenv_values

DOTENV_ENTRIES = dotenv_values()

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
    'sps-garfield': ['sps-garfield'],
    'nickelsville-cd': ['nickelsville-cd'],
}

PHYS_LOC_TO_LOGICAL_LOC = {
    phy: logi
    for (logi, phys) in LOGICAL_LOC_TO_PHYS_LOCS.items()
    for phy in phys
}

## { ip : physical loc }
MONITOR_DEVICES = {
#    '10.10.0.2': 'FCS',
    '10.10.0.3': 'sps-franklin',
#    '10.10.0.204': 'lihi-southend',
    '10.10.0.206': 'nickelsville-cd',
}
