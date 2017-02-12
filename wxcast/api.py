# -*- coding: utf-8 -*-

import configparser
import os
import requests

from wxcast.constants import FEET_PER_METER, HEADERS, NWS_API
from wxcast.exceptions import WxcastException

try:
    config_file = os.path.expanduser("~") + "/.wxcast"
    config = configparser.ConfigParser()
    config.read(config_file)
except FileNotFoundError:
    pass


def retrieve_nws_product(wfo, product):
    site = "{api}/products" \
           "/types/{product}" \
           "/locations/{wfo}".format(api=NWS_API, wfo=wfo.upper(),
                                     product=product.upper())

    try:
        response = requests.get(site, headers=HEADERS, verify='nws.pem')

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

        response = requests.get(response['features'][0]['@id'],
                                headers=HEADERS,
                                verify='nws.pem').json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the NWS website.')
    except Exception as e:
        raise WxcastException(str(e))

    return response['productText']


def get_wfo_products(wfo, json=False):
    try:
        site = "{api}/products/locations/{wfo}/types".format(api=NWS_API,
                                                             wfo=wfo.upper())
        data = requests.get(site,
                            headers=HEADERS,
                            verify='nws.pem').json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the avwx rest api.')
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    if json:
        return data['features']

    response = ['{}: {}'.format(d['productCode'],
                                d['productName']) for d in data['features']]

    return '\n'.join(response)


def get_metar(icao, decoded=False, json=False):
    try:
        site = "http://avwx.rest/api/metar/" \
               "{icao}?options=info,translate".format(icao=icao)
        data = requests.get(site).json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the avwx rest api.')
    except Exception as e: 
        raise WxcastException('An error has occurred: %s' % str(e))

    if 'Error' in data:
        raise WxcastException(data['Error'])

    if json:
        return data

    if decoded:
        output = ["Altimeter: {}".format(data['Translations']['Altimeter']),
                  "Clouds: {}".format(data['Translations']['Clouds']),
                  "Dewpoint: {}".format(data['Translations']['Dewpoint']),
                  "Other: {}".format(data['Translations']['Other']),
                  "Temperature: {}".format(
                      data['Translations']['Temperature']),
                  "Visibility: {}".format(data['Translations']['Visibility']),
                  "Wind: {}".format(data['Translations']['Wind'])]

        elevation = int(float(data['Info']['Elevation']) * FEET_PER_METER)
        info = ["Name: {}".format(data['Info']['Name']),
                "City: {}".format(data['Info']['State']),
                "Country: {}".format(data['Info']['Country']),
                "Elevation: {} ft".format(elevation),
                "Latitude: {}".format(data['Info']['Latitude']),
                "Longitude: {}".format(data['Info']['Longitude'])]

        info = '\n'.join(info)
        output = '\n'.join(output)
        header = "{raw}\n\nAt {time} the conditions " \
                 "at {icao} are {fr}.".format(raw=data['Raw-Report'],
                                              time=data['Time'],
                                              icao=data['Station'],
                                              fr=data['Flight-Rules'])

        return header + '\n\n' + output + '\n\n' + info

    # else return raw metar
    return data['Raw-Report']


def get_hourly_forecast(lat=None, lon=None, location='default'):
    if not lat or not lon:
        try:
            lat = config.get(location, 'lat')
            lon = config.get(location, 'lon')
        except KeyError:
            raise WxcastException('Config file not found.')

    site = "{api}/points" \
           "/{lat},{lon}" \
           "/forecast/hourly".format(api=NWS_API, lat=lat, lon=lon)

    try:
        data = requests.get(site, headers=HEADERS, verify='nws.pem').json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.')
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    return data['properties']['periods']


def get_seven_day_forecast(lat=None, lon=None, location='default', json=False):
    if not lat or not lon:
        try:
            lat = config.get(location, 'lat')
            lon = config.get(location, 'lon')
        except KeyError:
            raise WxcastException('Config file not found.')

    site = "{api}/points" \
           "/{lat},{lon}" \
           "/forecast".format(api=NWS_API, lat=lat, lon=lon)

    try:
        data = requests.get(site, headers=HEADERS, verify='nws.pem').json()

    except requests.exceptions.ConnectionError:
        raise WxcastException(
            'Connection could not be established with the nws rest api.')
    except Exception as e:
        raise WxcastException('An error has occurred: %s' % str(e))

    if json:
        return data['properties']['periods']

    periods = ['%s:\n%s' % (d['name'], d['detailedForecast'])
               for d in data['properties']['periods']]
    return '\n\n'.join(periods)
