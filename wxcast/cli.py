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

from textwrap import TextWrapper
from wxcast import api


def print_license(ctx, param, value):
    click.secho(
        'wxcast Copyright (C) 2017 sean Marlow. (GPL-3.0+)',
        fg='yellow'
    )
    click.secho(
        '\nThis program comes with ABSOLUTELY NO WARRANTY.',
        fg='yellow'
    )
    click.secho(
        'This is free software, and you are welcome to redistribute it'
        ' under certain conditions. See LICENSE for more information.',
        fg='yellow'
    )
    ctx.exit()


@click.group()
@click.version_option()
@click.option(
    '-l',
    '--license',
    is_flag=True,
    callback=print_license,
    help='Display license information and exit.'
)
def main(license):
    """Retrieve the latest weather information.

    Data provided by the NWS and avwx APIs.
    """
    pass


@click.command()
@click.argument('icao')
@click.option('-d', '--decoded',
              is_flag=True,
              help='Decode raw metar to string format.')
def metar(icao, decoded):
    """Retrieve latest metar from airport.

    Example: wxcast metar -d KSLC
    """
    try:
        response = api.get_metar(icao, decoded)
    except Exception as e:
        click.secho(str(e), fg='red')
    else:
        if decoded:
            click.echo(
                ''.join(
                    [click.style('At ', fg='green'),
                     click.style(response['header']['time'], fg='blue'),
                     click.style(' the conditions for ', fg='green'),
                     click.style(response['header']['icao'], fg='blue'),
                     click.style(' are ', fg='green'),
                     click.style(response['header']['fr'], fg='blue'),
                     '\n']
                )
            )

            spaces = max(
                [get_max_key(response['data']),
                 get_max_key(response['location'])]
            )
            echo_dict(response['data'], spaces=spaces)
            click.echo('')
            echo_dict(response['location'], spaces=spaces)

        else:
            click.secho(response, fg='blue')


def echo_dict(data, key_color='green', spaces=None, value_color='blue'):
    if not spaces:
        spaces = get_max_key(data)

    for key, value in data.items():
        title = '{spaces}{key}:  '.format(
            spaces=' ' * (spaces - len(key)),
            key=key
        )
        wrapper = TextWrapper(width=(82 - spaces),
                              subsequent_indent=' ' * (spaces + 3))
        click.echo(
            ''.join(
                [click.style(title, fg=key_color),
                 wrapper.fill(click.style(value, fg=value_color))]
            )
        )


def get_max_key(data):
    return max(map(len, data))


@click.command()
@click.argument('wfo')
@click.argument('product')
def text(wfo, product):
    """Retrieve NWS text products.

    Example: wxcast text slc afd
    """
    try:
        response = api.retrieve_nws_product(wfo, product)
    except Exception as e:
        click.secho(str(e), fg='red')
    else:
        click.echo_via_pager(response)


@click.command()
@click.argument('wfo')
def products(wfo):
    """Retrieve the available text products for a given wfo.

    Example: wxcast products slc
    """
    try:
        response = api.get_wfo_products(wfo)
    except Exception as e:
        click.secho(str(e), fg='red')
    else:
        echo_dict(response)


@click.command()
@click.option('-L', '--location', default='default',
              help='Location from config file to use for forecast.')
def forecast(location):
    """Retreive current weather conditions and 7 day forecast.

    Example: wxcast wx
    """
    response = api.get_seven_day_forecast(location=location)
    click.echo_via_pager(response)


main.add_command(metar)
main.add_command(text)
main.add_command(products)
main.add_command(forecast)


if __name__ == "__main__":
    main()
