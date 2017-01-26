# -*- coding: utf-8 -*-

import configparser
import os
import pandas
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
        response = requests.get(site,
                                headers=HEADERS,
                                verify='nws.pem').json()

        if '@graph' not in response:
            raise Exception(
                'No wx data found attempting to retrieve %s issued by %s.'
                % (product, wfo)
            )

        response = requests.get(response['@graph'][0]['@id'],
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
        return data['@graph']

    response = ['{}: {}'.format(d['productCode'],
                                d['productName']) for d in data['@graph']]

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


def get_forecast():
    try:
        lat = config.get('wx', 'lat')
        lon = config.get('wx', 'lon')
    except KeyError:
        raise Exception('Config file not found.')

    # New API information
    site = "http://forecast.weather.gov/MapClick.php?" \
           "lat={lat}" \
           "&lon={lon}" \
           "&unit=0" \
           "&lg=english" \
           "&FcstType=json".format(lat=lat, lon=lon)

    return requests.get(site).json()


def get_current_wx():
    data = get_forecast()['currentobservation']

    info = ["Name: {value}".format(value=data['name']),
            "Elevation: {value} ft".format(value=data['elev']),
            "Latitude: {value}".format(value=data['latitude']),
            "Longitude: {value}".format(value=data['longitude']),
            "Date: {value}".format(value=data['Date']),
            "Temperature: {value} F".format(value=data['Temp']),
            "Windchill: {value} F".format(value=data['WindChill']),
            "Dew Point: {value} F".format(value=data['Dewp']),
            "Relative Humidity: {value} %%".format(value=data['Relh']),
            "Winds: {value} mph".format(value=data['Winds']),
            "Wind Direction: {value}".format(value=data['Windd']),
            "Weather: {value}".format(value=data['Weather']),
            "Visibility: {value} mi.".format(value=data['Visibility']),
            "Sea-level Pressure: {value} Hg".format(value=data['SLP'])]

    return '\n'.join(info)


def get_seven_day_forecast():
    data = get_forecast()

    periods = data['time']['startPeriodName']
    short_descs = data['data']['weather']
    temps = data['data']['temperature']
    descs = data['data']['text']

    weather = pandas.DataFrame({
        "period": periods,
        "short_desc": short_descs,
        "temp": temps,
        "desc": descs
    })

    location = 'Location: %s \n\n' % data['location']['areaDescription']
    return location + weather.to_string(header=False, index=False)
