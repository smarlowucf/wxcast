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

import click

from collections import OrderedDict

from wxcast import api
from wxcast import utils


def print_license(ctx, param, value):
    """
    Eager option to print license information and exit.
    """
    if not value or ctx.resilient_parsing:
        return

    click.echo(
        'wxcast Copyright (C) 2021 Sean Marlow. (MIT License)\n\n'
        'See LICENSE for more information.'
    )
    ctx.exit()


@click.group()
@click.version_option()
@click.option(
    '--license',
    expose_value=False,
    is_eager=True,
    is_flag=True,
    callback=print_license,
    help='Display license information and exit.'
)
def main():
    """
    Retrieve the latest weather information in your terminal.

    Data provided by NWS and AVWX.

    NWS: https://forecast-v3.weather.gov/documentation \n
    AVWX: https://avwx.rest/
    """
    pass


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('location')
def forecast(no_color, location):
    """
    Retrieve current 7 day forecast for given location.

    Location can be a city, address or zip/postal code.

    Examples:
        wxcast forecast denver
        wxcast forecast "denver, co"

    :param location: Location string to get forecast for.
    :param no_color: If True do not style string output.
    """
    try:
        response = api.get_seven_day_forecast(location)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        data = OrderedDict(
            (d['name'], d['detailedForecast']) for d in response
        )
        utils.echo_dict(data, no_color)


@click.command()
@click.option(
    '-d', '--decoded',
    is_flag=True,
    help='Decode raw metar to string format.'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('icao')
def metar(decoded, no_color, icao):
    """
    Retrieve the latest METAR given an airport ICAO code.

    Example: wxcast metar -d KSLC

    :param decoded: Flag to decode the METAR output.
    :param no_color: If True do not style string output.
    :param icao: The airport ICAO code to retrieve METAR for.
    """
    try:
        response = api.get_metar(icao, decoded)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        if decoded:
            click.echo(
                ''.join([
                    utils.style_string(
                        'At ', no_color, fg='green'
                    ),
                    utils.style_string(
                        response['time'], no_color, fg='blue'
                    ),
                    utils.style_string(
                        ' the conditions are:', no_color, fg='green'
                    ),
                    '\n'
                ])
            )

            spaces = utils.get_max_key(response)

            try:
                # Try to convert elevation to ft and meters.
                response['elevation'] = '{}ft ({}m)'.format(
                    int(float(response['elevation']) * 3.28084),
                    response['elevation']
                )
            except (KeyError, Exception):
                pass

            utils.echo_dict(response, no_color, spaces=spaces)
        else:
            utils.echo_style(response, no_color, fg='blue')


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
def offices(no_color):
    """
    Retrieve the available weather forecast offices (WFO).

    Example: wxcast offices

    :param no_color: If True do not style string output.
    """
    try:
        response = api.get_wfo_list()
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_dict(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('wfo')
def products(no_color, wfo):
    """
    Retrieve the available text products for a given wfo.

    Example: wxcast products slc

    :param no_color: If True do not style string output.
    :param wfo: The weather forecast office abbreviation (BOU).
    """
    try:
        response = api.get_wfo_products(wfo)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_dict(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('wfo')
@click.argument('product')
def text(no_color, wfo, product):
    """
    Retrieve the NWS text product.

    Example: wxcast text slc afd

    :param no_color: If True do not style string output.
    :param wfo: The weather forecast office abbreviation (BOU).
    :param product: The text product to retrieve.
    """
    try:
        response = api.get_nws_product(wfo, product)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        click.echo_via_pager(response)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('wfo')
def office(no_color, wfo):
    """
    Retrieve information for a given wfo.

    Example: wxcast info slc

    :param no_color: If True do not style string output.
    :param wfo: The weather forecast office abbreviation (BOU).
    """
    try:
        response = api.get_wfo_info(wfo)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_dict(response, no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('wfo')
def stations(no_color, wfo):
    """
    Retrieve a list of stations for a given wfo.

    Example: wxcast info slc

    :param no_color: If True do not style string output.
    :param wfo: The weather forecast office abbreviation (BOU).
    """
    try:
        response = api.get_stations_for_wfo(wfo)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_style('\n'.join(response), no_color)


@click.command()
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
@click.argument('station_id')
def station(no_color, station_id):
    """
    Retrieve info for a weather station.

    Example: wxcast station kbna

    :param no_color: If True do not style string output.
    :param station_id: The weather station id.
    """
    try:
        response = api.get_station_info(station_id)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        try:
            # Try to convert elevation to ft and meters.
            response['elevation'] = '{}ft ({}m)'.format(
                int(float(response['elevation']) * 3.28084),
                response['elevation']
            )
        except (KeyError, Exception):
            pass

        utils.echo_dict(response, no_color)


main.add_command(metar)
main.add_command(text)
main.add_command(offices)
main.add_command(products)
main.add_command(forecast)
main.add_command(office)
main.add_command(stations)
main.add_command(station)
