# -*- coding: utf-8 -*-
#
# wxcast: A Python API and cli to collect weather information.
#
# Copyright (c) 2018 Sean Marlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests

from geopy.geocoders import ArcGIS

from wxcast.constants import HEADERS, NWS_API
from wxcast.exceptions import WxcastException


def get_metar(icao, decoded=False):
    """
    Retrieve METAR for ICAO.

    :param icao: Airport code.
    :param decoded: Flag to decode the METAR.
    :return: Returns raw METAR string or dictionary with decoded info.
    """
    try:
        icao = icao.upper()
        site = f'http://avwx.rest/api/metar/{icao}?options=info,translate'
        data = requests.get(site).json()

        if 'Error' in data:
            raise Exception(data['Error'])
    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the avwx rest api.'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve metar for {icao}: {error}'
        )

    if decoded:
        header = {
            'time': data['Time'],
            'icao': data['Station'],
            'fr': data['Flight-Rules']
        }
        output = {
            'data': data['Translate'],
            'header': header,
            'location': data['Info']
        }

        return output

    # else return raw metar
    return data['Raw-Report']


def get_nws_product(wfo, product):
    """
    Returns text from product for given WFO.

    :param wfo: Weather forecast office abbreviation code.
    :param product: The text product to return.
    :return: Product text value as string.
    """
    site = f'{NWS_API}/products/types/' \
        f'{product.upper()}/locations/{wfo.upper()}'

    try:
        response = requests.get(site, headers=HEADERS)
        if response.status_code == 404:
            raise Exception(
                'Unable to establish connection with NWS api.'
            )

        response = response.json()
        if not response.get('@graph'):
            raise Exception('WFO and product combination not found.')

        response = requests.get(
            response['@graph'][0]['@id'],
            headers=HEADERS
        ).json()
    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            f'Connection could not be established with the NWS website: '
            f'{str(e)}'
        )
    except Exception as error:
        raise WxcastException(
            f'No wx data found attempting to retrieve '
            f'{product} issued by {wfo}: {error}'
        )

    return response['productText']


def get_seven_day_forecast(location):
    """
    Retrieve seven day forecast for the given location.

    :param location: String value of location (address, name, zip, etc).
    :return: A dictionary with forecast split in periods.
    """
    geolocator = ArcGIS(
        user_agent='wxcast app. https://github.com/smarlowucf/wxcast'
    )
    geolocation = geolocator.geocode(location)

    if not geolocation:
        raise WxcastException(
            f'Location not found: {location}.'
        )

    latlong = f'{geolocation.latitude},{geolocation.longitude}'

    try:
        data = requests.get(
            f'{NWS_API}/points/{latlong}/forecast',
            headers=HEADERS
        ).json()
        if 'properties' not in data:
            raise Exception()
    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.'
        )
    except Exception as e:
        raise WxcastException(
            f'No forecast found for location: {location} '
            f'coordinates: {latlong}'
        )

    return data['properties']['periods']


def get_wfo_list():
    """
    Get a list of the available weather forecast offices (wfo).

    :return: Return dictionary of wfo {code: name}.
    """
    try:
        site = f'{NWS_API}/products/locations/'
        data = requests.get(site, headers=HEADERS).json()
    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            f'Connection could not be established with the avwx rest api: '
            f'{str(e)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve list of WFOs: {error}'
        )

    wfo_list = {}
    for code, name in data['locations'].items():
        if code and name:
            wfo_list[code] = name

    return wfo_list


def get_wfo_products(wfo):
    """
    Get a list of the text products available for the given WFO.

    :param wfo: The weather forecast office to retrieve product list for.
    :return: Return dictionary of text products {code: name}.
    """
    try:
        site = f'{NWS_API}/products/locations/{wfo.upper()}/types'
        data = requests.get(site, headers=HEADERS).json()

        if not data.get('@graph'):
            raise Exception('Invalid WFO code.')
    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            f'Connection could not be established with the nws rest api: '
            f'{str(e)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve products for WFO {wfo}: {error}'
        )

    return {d['productCode']: d['productName'] for d in data['@graph']}
