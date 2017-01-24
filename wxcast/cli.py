# -*- coding: utf-8 -*-

import click

from wxcast import api


@click.group()
def main():
    pass


@click.command()
@click.argument('icao')
@click.option('-d', '--decoded', is_flag=True, help='Decode raw metar to string format.')
def metar(icao, decoded):
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
    try:
        response = api.retrieve_nws_product(wfo, product)
    except Exception as e:
        click.secho(str(e), fg='red')
    else:
        click.echo_via_pager(response)


@click.command()
@click.argument('wfo')
def products(wfo):
    try:
        response = api.get_wfo_products(wfo)
    except Exception as e:
        click.secho(str(e), fg='red')
    else:
        click.echo_via_pager(response)


@click.command()
@click.option('-s', '--seven-day', is_flag=True, help='Display seven day forecast.')
def wx(seven_day):
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
