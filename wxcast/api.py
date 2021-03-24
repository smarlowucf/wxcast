# -*- coding: utf-8 -*-
#
# wxcast: A Python API and cli to collect weather information.
#
# Copyright (c) 2021 Sean Marlow
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

from collections import OrderedDict
from geopy.geocoders import ArcGIS
from metar import Metar

from wxcast.constants import HEADERS, NWS_API
from wxcast.exceptions import WxcastException


def metar_to_dict(metar_obj, temp_unit='C', pressure_unit='MB'):
    data = {}
    data['station'] = metar_obj.station_id

    if metar_obj.type:
        data['type'] = metar_obj.report_type()
    if metar_obj.time:
        data['time'] = metar_obj.time.ctime()
    if metar_obj.temp:
        data['temperature'] = metar_obj.temp.string(temp_unit)
    if metar_obj.dewpt:
        data['dew point'] = metar_obj.dewpt.string(temp_unit)
    if metar_obj.wind_speed:
        data['wind'] = metar_obj.wind()
    if metar_obj.wind_speed_peak:
        data['peak wind'] = metar_obj.peak_wind()
    if metar_obj.wind_shift_time:
        data['wind shift'] = metar_obj.wind_shift()
    if metar_obj.vis:
        data['visibility'] = metar_obj.visibility()
    if metar_obj.runway:
        data['visual range'] = metar_obj.runway_visual_range()
    if metar_obj.press:
        data['pressure'] = metar_obj.press.string(pressure_unit)
    if metar_obj.weather:
        data['weather'] = metar_obj.present_weather()
    if metar_obj.sky:
        data['sky'] = metar_obj.sky_conditions(', ')
    if metar_obj.press_sea_level:
        data['sea level pressure'] = metar_obj.press_sea_level.string(
            pressure_unit
        )
    if metar_obj.max_temp_6hr:
        data['6 hour max temp'] = str(metar_obj.max_temp_6hr)
    if metar_obj.max_temp_6hr:
        data['6 hour min temp'] = str(metar_obj.min_temp_6hr)
    if metar_obj.max_temp_24hr:
        data['24 hour max temp'] = str(metar_obj.max_temp_24hr)
    if metar_obj.max_temp_24hr:
        data['24 hour min temp'] = str(metar_obj.min_temp_24hr)
    if metar_obj.precip_1hr:
        data['1 hour precip'] = str(metar_obj.precip_1hr)
    if metar_obj.precip_3hr:
        data['3 hour precip'] = str(metar_obj.precip_3hr)
    if metar_obj.precip_6hr:
        data['6 hour precip'] = str(metar_obj.precip_6hr)
    if metar_obj.precip_24hr:
        data['24 hour precip'] = str(metar_obj.precip_24hr)
    if metar_obj.ice_accretion_1hr:
        data['1 hour ice'] = str(metar_obj.ice_accretion_1hr)
    if metar_obj.ice_accretion_3hr:
        data['3 hour ice'] = str(metar_obj.ice_accretion_3hr)
    if metar_obj.ice_accretion_6hr:
        data['6 hour ice'] = str(metar_obj.ice_accretion_6hr)
    if metar_obj._remarks:
        data['remarks'] = metar_obj.remarks(', ')
    if metar_obj._unparsed_remarks:
        data['remarks'] = data.get('remarks', '') + ', '.join(
            metar_obj._unparsed_remarks
        )

    return data


def get_metar(station_id, temp_unit='C', decoded=False):
    """
    Retrieve METAR for ICAO.

    :param icao: Airport code.
    :param decoded: Flag to decode the METAR.
    :return: Returns raw METAR string or dictionary with decoded info.
    """
    try:
        site = f'{NWS_API}/stations/{station_id}/observations/latest'
        data = requests.get(site).json()

        if data.get('status', 200) == 404:
            raise Exception(
                f'{station_id} is not a valid station id.'
            )

        raw_metar = data['properties']['rawMessage']

        if not raw_metar:
            raise Exception(
                'No metar data in response, try again in a few minutes.'
            )
    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the NWS rest api.'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve metar for {station_id}: {error}'
        )

    if decoded:
        data_obj = Metar.Metar(raw_metar)
        json_data = metar_to_dict(data_obj, temp_unit=temp_unit)
        json_data['elevation'] = data['properties']['elevation']['value']
        return json_data

    # else return raw metar
    return raw_metar


def get_nws_product(wfo, product):
    """
    Returns text from product for given WFO.

    :param wfo: Weather forecast office abbreviation code.
    :param product: The text product to return.
    :return: Product text value as string.
    """
    site = '{NWS_API}/products/types/{product}/locations/{wfo}'.format(
        NWS_API=NWS_API,
        product=product.upper(),
        wfo=wfo.upper()
    )

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
        ).json(object_pairs_hook=OrderedDict)
    except requests.exceptions.ConnectionError as error:
        raise WxcastException(
            f'Connection could not be established with the NWS website: '
            f'{str(error)}'
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

    latlong = '{lat},{lon}'.format(
        lat=geolocation.latitude,
        lon=geolocation.longitude
    )

    try:
        point_data = get_point_info(latlong)
        data = requests.get(
            f'{NWS_API}/gridpoints/{point_data["wfo"]}/'
            f'{point_data["x"]},{point_data["y"]}/forecast',
            headers=HEADERS
        ).json(object_pairs_hook=OrderedDict)
        if 'properties' not in data:
            raise Exception()
    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.'
        )
    except Exception:
        raise WxcastException(
            f'No forecast found for location: {location} '
            f'coordinates: {latlong}'
        )

    return data['properties']['periods']


def get_point_info(location):
    """
    Retrieve point forecast info for the given location.

    :param location: String value of coordinates (lat/lon).
    :return: A dictionary with info on a point forecast location.
    """
    try:
        data = requests.get(
            f'{NWS_API}/points/{location}',
            headers=HEADERS
        ).json(object_pairs_hook=OrderedDict)
        if 'properties' not in data:
            raise Exception()
    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.'
        )
    except Exception:
        raise WxcastException(
            f'No point found for coordinates: {location}.'
        )

    point_data = {
        'wfo': data['properties']['gridId'],
        'x': data['properties']['gridX'],
        'y': data['properties']['gridY']
    }

    return point_data


def get_wfo_list():
    """
    Get a list of the available weather forecast offices (wfo).

    :return: Return dictionary of wfo {code: name}.
    """
    try:
        site = f'{NWS_API}/products/locations/'
        data = requests.get(site, headers=HEADERS).json(
            object_pairs_hook=OrderedDict
        )
    except requests.exceptions.ConnectionError as error:
        raise WxcastException(
            f'Connection could not be established with the avwx rest api: '
            f'{str(error)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve list of WFOs: {error}'
        )

    wfo_list = OrderedDict()
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
        data = requests.get(site, headers=HEADERS).json(
            object_pairs_hook=OrderedDict
        )

        if not data.get('@graph'):
            raise Exception('Invalid WFO code.')
    except requests.exceptions.ConnectionError as error:
        raise WxcastException(
            f'Connection could not be established with the nws rest api: '
            f'{str(error)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve products for WFO {wfo}: {error}'
        )

    return OrderedDict(
        (d['productCode'], d['productName']) for d in data['@graph']
    )


def get_wfo_info(wfo):
    """
    Get information for the given WFO.

    :param wfo: The weather forecast office to retrieve info for.
    :return: Return dictionary of text info {code: name}.
    """
    try:
        site = f'{NWS_API}/offices/{wfo.upper()}'
        data = requests.get(site, headers=HEADERS).json(
            object_pairs_hook=OrderedDict
        )

        if not data.get('@id'):
            raise Exception('Invalid WFO code.')
    except requests.exceptions.ConnectionError as error:
        raise WxcastException(
            f'Connection could not be established with the nws rest api: '
            f'{str(error)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve info for WFO {wfo}: {error}'
        )

    wfo_data = {
        'name': data['name'],
        'telephone': data['telephone'],
        'fax number': data['faxNumber'],
        'email': data['email'],
        'address': f'{data["address"]["streetAddress"]}, '
                   f'{data["address"]["addressLocality"]}, '
                   f'{data["address"]["addressRegion"]} '
                   f'{data["address"]["postalCode"]}'
    }

    return wfo_data


def get_stations_for_wfo(wfo):
    """
    Get a list of weather stations for the given WFO.

    :param wfo: The weather forecast office to retrieve station list for.
    :return: Return dictionary of text info {code: name}.
    """
    try:
        site = f'{NWS_API}/offices/{wfo.upper()}'
        data = requests.get(site, headers=HEADERS).json(
            object_pairs_hook=OrderedDict
        )

        if not data.get('@id'):
            raise Exception('Invalid WFO code.')
    except requests.exceptions.ConnectionError as error:
        raise WxcastException(
            f'Connection could not be established with the nws rest api: '
            f'{str(error)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve weather stations for WFO {wfo}: {error}'
        )

    stations = [
        station.rsplit('/', maxsplit=1)[-1] for
        station in data['approvedObservationStations']
    ]

    return stations


def get_station_info(station_id):
    """
    Get information for a given weather station.

    :param station_id: The weather station id to retrieve info for.
    :return: Return dictionary of text info {code: name}.
    """
    try:
        site = f'{NWS_API}/stations/{station_id.upper()}'
        data = requests.get(site, headers=HEADERS).json(
            object_pairs_hook=OrderedDict
        )

        if not data.get('@context'):
            raise Exception('Invalid station id.')
    except requests.exceptions.ConnectionError as error:
        raise WxcastException(
            f'Connection could not be established with the nws rest api: '
            f'{str(error)}'
        )
    except Exception as error:
        raise WxcastException(
            f'Could not retrieve info for weather station {station_id}: '
            f'{error}'
        )

    station_data = {
        'name': data['properties']['name'],
        'time zone': data['properties']['timeZone'],
        'elevation': data['properties']['elevation']['value']
    }

    return station_data
