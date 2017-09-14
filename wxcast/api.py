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

import configparser
import os
import requests

from wxcast.constants import CONFIG_FILE, HEADERS, NWS_API
from wxcast.exceptions import WxcastException


def retrieve_nws_product(wfo, product):
    site = "{api}/products/types/{product}/locations/{wfo}".format(
        api=NWS_API,
        wfo=wfo.upper(),
        product=product.upper()
    )

    try:
        response = requests.get(site, headers=HEADERS)

        if response.status_code == 404:
            raise Exception(
                'No wx data found attempting to retrieve %s issued by %s.'
                % (product, wfo)
            )

        response = response.json()
        if not response.get('features', None):
            raise Exception(
                'No wx data found attempting to retrieve %s issued by %s.'
                % (product, wfo)
            )

        response = requests.get(
            response['features'][0]['@id'],
            headers=HEADERS
        ).json()

    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            'Connection could not be established with the NWS website: %s'
            % str(e)
        )
    except Exception as e:
        raise WxcastException(str(e))

    return response['productText']


def get_wfo_products(wfo):
    try:
        site = "{api}/products/locations/{wfo}/types".format(
            api=NWS_API,
            wfo=wfo.upper()
        )
        data = requests.get(site, headers=HEADERS).json()

    except requests.exceptions.ConnectionError as e:
        raise WxcastException(
            'Connection could not be established with the avwx rest api: %s'
            % str(e)
        )
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    response = {d['productCode']: d['productName'] for d in data['features']}
    return response


def get_metar(icao, decoded=False):
    try:
        site = "http://avwx.rest/api/metar/{icao}?options=info,translate" \
            .format(icao=icao)
        data = requests.get(site).json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the avwx rest api.'
        )
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    if 'Error' in data:
        raise WxcastException(data['Error'])

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


def get_hourly_forecast(lat=None, lon=None, location='default'):
    if not lat or not lon:
        try:
            lat = config.get(location, 'lat')
            lon = config.get(location, 'lon')
        except KeyError:
            raise WxcastException('Config file not found.')

    site = "{api}/points/{lat},{lon}/forecast/hourly".format(
        api=NWS_API,
        lat=lat,
        lon=lon
    )

    try:
        data = requests.get(site, headers=HEADERS).json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.'
        )
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    return data['properties']['periods']


def get_seven_day_forecast(lat=None, lon=None, location='default', json=False):
    if not (lat and lon):
        if not os.path.exists(CONFIG_FILE):
            raise WxcastException('Config file: ~/.wxcast not found.')

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        try:
            lat = config.get(location, 'lat')
            lon = config.get(location, 'lon')
        except configparser.NoSectionError:
            raise WxcastException('Location: %s not in config file ~/.wxcast' % location)
        except configparser.NoOptionError as e:
            raise WxcastException('Error in config file: %s' % e)

    site = "{api}/points/{lat},{lon}/forecast".format(
        api=NWS_API,
        lat=lat,
        lon=lon
    )

    try:
        data = requests.get(site, headers=HEADERS).json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.'
        )
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    if json:
        return data['properties']['periods']

    periods = [
        '%s:\n%s' % (d['name'], d['detailedForecast'])
        for d in data['properties']['periods']
    ]
    return '\n\n'.join(periods)
