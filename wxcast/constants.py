# -*- coding: utf-8 -*-

import requests


FEET_PER_METER = 3.28084
HEADERS = requests.utils.default_headers()
HEADERS.update(
    {
        'User-Agent': 'wxcast app. https://github.com/smarlowucf/wxcast',
    }
)
NWS_API = 'https://api.weather.gov'
