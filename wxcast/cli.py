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
        click.echo(
            ''.join(
                [click.style(title, fg=key_color),
                 click.style(value, fg=value_color)]
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
        click.echo_via_pager(click.style(response, fg='green'))


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
