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

import click

from wxcast import api
from wxcast import utils


def print_license(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(
        'wxcast Copyright (C) 2017 sean Marlow. (GPL-3.0+)\n\n'
        'This program comes with ABSOLUTELY NO WARRANTY.\n'
        'This is free software, and you are welcome to redistribute it'
        ' under certain conditions. See LICENSE for more information.'
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
    Retrieve the latest weather information right in your terminal.

    Data provided by NWS and AVWX.

    NWS: https://forecast-v3.weather.gov/documentation \n
    AVWX: https://avwx.rest/
    """
    pass


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
                        response['header']['time'], no_color, fg='blue'
                    ),
                    utils.style_string(
                        ' the conditions for ', no_color, fg='green'
                    ),
                    utils.style_string(
                        response['header']['icao'], no_color, fg='blue'
                    ),
                    utils.style_string(
                        ' are ', no_color, fg='green'
                    ),
                    utils.style_string(
                        response['header']['fr'], no_color, fg='blue'
                    ),
                    '\n'
                ])
            )

            spaces = max([
                utils.get_max_key(response['data']),
                utils.get_max_key(response['location'])
            ])

            utils.echo_dict(response['data'], no_color, spaces=spaces)
            click.echo('')

            try:
                # Try to convert elevation to ft and meters.
                response['location']['Elevation'] = '{}ft ({}m)'.format(
                    int(float(response['location']['Elevation']) * 3.28084),
                    response['location']['Elevation']
                )
            except:
                pass

            utils.echo_dict(response['location'], no_color, spaces=spaces)

        else:
            utils.echo_style(response, no_color, fg='blue')


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
    """
    try:
        response = api.retrieve_nws_product(wfo, product)
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
def products(no_color, wfo):
    """
    Retrieve the available text products for a given wfo.

    Example: wxcast products slc
    """
    try:
        response = api.get_wfo_products(wfo)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        utils.echo_dict(response, no_color)


@click.command()
@click.option(
    '-L',
    '--location',
    default='default',
    help='Location from config file to use for forecast.'
)
@click.option(
    '--no-color',
    is_flag=True,
    help='Remove ANSI color and styling from output.'
)
def forecast(location, no_color):
    """
    Retrieve current 7 day forecast for given location.

    Example: wxcast forecast -L denver
    """
    try:
        response = api.get_seven_day_forecast(location=location)
    except Exception as e:
        utils.echo_style(str(e), no_color, fg='red')
    else:
        data = {d['name']: d['detailedForecast'] for d in response}
        utils.echo_dict(data, no_color)


main.add_command(metar)
main.add_command(text)
main.add_command(products)
main.add_command(forecast)
