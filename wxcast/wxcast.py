# -*- coding: utf-8 -*-
import pandas
import requests

from bs4 import BeautifulSoup
from metar import Metar

FEET_PER_METER = 3.28084


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


def get_current_wx(lat, lon):
    data = get_forecast(lat, lon)['currentobservation']

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


def get_forecast(lat, lon):
    site = "http://forecast.weather.gov/MapClick.php?" \
           "lat={lat}" \
           "&lon={lon}" \
           "&unit=0" \
           "&lg=english" \
           "&FcstType=json".format(lat=lat, lon=lon)

    return requests.get(site).json()


def get_forecast_discussion(wfo):
    retrieve_nws_product(wfo, 'AFD')


def get_hazardous_wx_outlook(wfo):
    retrieve_nws_product(wfo, 'HWO')


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


def get_seven_day_forecast(lat, lon):
    data = get_forecast(lat, lon)

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
    retrieve_nws_product(wfo, 'ZFP')


if __name__ == "__main__":
    print(get_seven_day_forecast("40.2769", "-111.6817"))
