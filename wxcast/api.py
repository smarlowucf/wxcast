# -*- coding: utf-8 -*-

import configparser
import os
import pandas
import requests

from bs4 import BeautifulSoup
from metar import Metar
from wxcast.constants import FEET_PER_METER

try:
    config_file = os.path.expanduser("~") + "/.wxcast"
    config = configparser.ConfigParser()
    config.read(config_file)
except FileNotFoundError:
    pass


def retrieve_nws_product(wfo, product):
    site = "http://forecast.weather.gov/product.php?" \
           "site=NWS" \
           "&issuedby={wfo}" \
           "&product={product}" \
           "&format=TXT" \
           "&version=1" \
           "&glossary=0".format(wfo=wfo,
                                product=product)
    page = requests.get(site)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup.find(class_="glossaryProduct").get_text()


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


def get_forecast():
    try:
        lat = config.get('wx', 'lat')
        lon = config.get('wx', 'lon')
    except KeyError:
        raise Exception('Config file not found.')

    site = "http://forecast.weather.gov/MapClick.php?" \
           "lat={lat}" \
           "&lon={lon}" \
           "&unit=0" \
           "&lg=english" \
           "&FcstType=json".format(lat=lat, lon=lon)

    return requests.get(site).json()


def get_forecast_discussion(wfo):
    return retrieve_nws_product(wfo, 'AFD')


def get_hazardous_wx_outlook(wfo):
    return retrieve_nws_product(wfo, 'HWO')


def get_metar(icao, decoded=False):
    site = "http://avwx.rest/api/metar/{icao}?options=info".format(icao=icao)
    data = requests.get(site).json()

    if decoded:
        output = Metar.Metar(data['Raw-Report']).string()

        elevation = int(float(data['Info']['Elevation']) * FEET_PER_METER)
        info = ["Name: {value}".format(value=data['Info']['Name']),
                "City: {value}".format(value=data['Info']['State']),
                "Country: {value}".format(value=data['Info']['Country']),
                "Elevation: {value} ft".format(value=elevation),
                "Latitude: {value}".format(value=data['Info']['Latitude']),
                "Longitude: {value}".format(value=data['Info']['Longitude'])]

        info = '\n'.join(info)
        return output + '\n\n' + info

    return data['Raw-Report']


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


def get_zone_forecast(wfo):
    return retrieve_nws_product(wfo, 'ZFP')


if __name__ == "__main__":
    print(get_forecast_discussion('SLC'))
