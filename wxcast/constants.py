# -*- coding: utf-8 -*-

import requests


HEADERS = requests.utils.default_headers()
HEADERS.update(
    {
        'User-Agent': 'wxcast app. https://github.com/smarlowucf/wxcast',
    }
)
NWS_API = 'https://api.weather.gov'
