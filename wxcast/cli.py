# -*- coding: utf-8 -*-

import click

from wxcast import api


@click.group()
def main():
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
            click.echo_via_pager(response)
        else:
            click.secho(response, fg='white')


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
        click.echo_via_pager(response)


@click.command()
@click.option('-s', '--seven-day',
              is_flag=True,
              help='Display seven day forecast.')
def wx(seven_day):
    """Retreive current weather conditions and 7 day forecast.

    Example: wxcast wx
    """
    if seven_day:
        response = api.get_seven_day_forecast()
        click.secho(response, fg='white')
    else:
        response = api.get_current_wx()
        click.secho(response, fg='white')


main.add_command(metar)
main.add_command(text)
main.add_command(products)
main.add_command(wx)


if __name__ == "__main__":
    main()
