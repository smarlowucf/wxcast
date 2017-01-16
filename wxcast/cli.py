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
    response = api.get_metar(icao, decoded)
    click.secho(response, fg='white')


@click.command()
@click.argument('wfo')
@click.argument('product')
def text(wfo, product):
    if product == 'ZFP':
        response = api.get_zone_forecast(wfo)
    elif product == 'HWO':
        response = api.get_hazardous_wx_outlook(wfo)
    elif product == 'AFD':
        response = api.get_forecast_discussion(wfo)
    else:
        click.secho('%s is not supported. :(' % product, fg='red')
        return 1

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
main.add_command(wx)


if __name__ == "__main__":
    main()
