# -*- coding: utf-8 -*-
#
# wxcast: A Python API and cli to collect weather information.
#
# Copyright (C) 2017 Sean Marlow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests

from geopy.geocoders import Nominatim

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
        site = f'http://avwx.rest/api/metar/{icao}?options=info,translate'
        data = requests.get(site).json()

        if 'Error' in data:
            raise Exception()
    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the avwx rest api.'
        )
    except Exception:
        raise WxcastException(f'Invalid ICAO: {icao}, metar not found.')

    if decoded:
        header = {
            'time': data['Time'],
            'icao': data['Station'],
            'fr': data['Flight-Rules']
        }
        output = {
            'data': data['Translations'],
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
            raise Exception()

        response = response.json()
        if not response.get('features', None):
            raise Exception()

        response = requests.get(
            response['features'][0]['@id'],
            headers=HEADERS
        ).json()
    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            f'Connection could not be established with the NWS website: '
            f'{str(e)}'
        )
    except Exception:
        raise WxcastException(
            f'No wx data found attempting to retrieve '
            f'{product} issued by {wfo}.'
        )

    return response['productText']


def get_seven_day_forecast(location):
    """
    Retrieve seven day forecast for the given location.

    :param location: String value of location (address, name, zip, etc).
    :return: A dictionary with forecast split in periods.
    """
    geolocator = Nominatim()
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


def get_wfo_products(wfo):
    """
    Get a list of the text products available for the given WFO.

    :param wfo: The weather forecast office to retrieve product list for.
    :return: Return dictionary of text products {code: name}.
    """
    try:
        site = f'{NWS_API}/products/locations/{wfo.upper()}/types'
        data = requests.get(site, headers=HEADERS).json()

        if 'features' not in data:
            raise Exception()
    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            f'Connection could not be established with the avwx rest api: '
            f'{str(e)}'
        )
    except Exception:
        raise WxcastException(f'Could not retrieve products for WFO: {wfo}.')

    return {d['productCode']: d['productName'] for d in data['features']}
