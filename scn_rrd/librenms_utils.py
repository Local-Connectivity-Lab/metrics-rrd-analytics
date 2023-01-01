## Stdlib
from typing import Any

## Non-std libs
import requests

## Local modules
from . import rrd_meta_utils

API_URL_PFX = f"http://{rrd_meta_utils.DOTENV_ENTRIES['NMS_HOST_NAME']}/api/v0"
API_HEADERS = {
    'Authorization': f"Bearer {rrd_meta_utils.DOTENV_ENTRIES['LIBRENMS_API_TOKEN']}"
}
def req_librenms(api_url_sfx: str):
    resp = requests.get(f"{API_URL_PFX}{api_url_sfx}", headers=API_HEADERS)
    assert resp.status_code == 200
    return resp.json()

def is_device_out_of_service(device_id_or_hostname: Any) -> bool:
    outages = req_librenms(f"/devices/{device_id_or_hostname}/outages")
    outages = outages['outages']

    most_recent_outage = None
    for outage in outages:
        if most_recent_outage is None or most_recent_outage['going_down'] < outage['going_down']:
            most_recent_outage = outage
    
    return most_recent_outage is not None and most_recent_outage['up_again'] is None
