import vcr

from click.testing import CliRunner

from wxcast.cli import main


def test_print_license():
    license = 'wxcast Copyright (C) 2018 Sean Marlow. (MIT License)\n\n' \
        'See LICENSE for more information.\n'

    runner = CliRunner()
    result = runner.invoke(main, ['--license'])
    assert result.exit_code == 0
    assert result.output == license


@vcr.use_cassette('tests/cassettes/forecast.yml')
def test_forecast():
    runner = CliRunner()
    result = runner.invoke(main, ['forecast', 'denver, co'])
    assert result.exit_code == 0

    with open('tests/cassettes/forecast.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/forecast_invalid.yml')
def test_forecast_invalid():
    runner = CliRunner()
    result = runner.invoke(main, ['forecast', 'Fake, FK'])
    assert result.exit_code == 0

    with open('tests/cassettes/forecast_invalid.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/metar.yml')
def test_metar():
    runner = CliRunner()
    result = runner.invoke(main, ['metar', 'KDEN'])
    assert result.exit_code == 0

    with open('tests/cassettes/metar.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/metar_invalid.yml')
def test_metar_invalid():
    runner = CliRunner()
    result = runner.invoke(main, ['metar', 'KFAKE'])
    assert result.exit_code == 0

    with open('tests/cassettes/metar_invalid.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/decoded_metar.yml')
def test_decoded_metar():
    runner = CliRunner()
    result = runner.invoke(main, ['metar', '-d', 'KDEN'])
    assert result.exit_code == 0

    with open('tests/cassettes/decoded_metar.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/products.yml')
def test_products():
    runner = CliRunner()
    result = runner.invoke(main, ['products', 'bou'])
    assert result.exit_code == 0

    with open('tests/cassettes/products.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/products_invalid.yml')
def test_products_invalid():
    runner = CliRunner()
    result = runner.invoke(main, ['products', 'fake'])
    assert result.exit_code == 0

    with open('tests/cassettes/products_invalid.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/text_afd.yml')
def test_text_afd():
    runner = CliRunner()
    result = runner.invoke(main, ['text', 'bou', 'afd'])
    assert result.exit_code == 0

    with open('tests/cassettes/text_afd.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/text_afd_invalid.yml')
def test_text_afd_invalid():
    runner = CliRunner()
    result = runner.invoke(main, ['text', 'fake', 'afd'])
    assert result.exit_code == 0

    with open('tests/cassettes/text_afd_invalid.out', 'r') as f:
        out = f.read()

    assert out == result.output


@vcr.use_cassette('tests/cassettes/offices.yml')
def test_offices():
    runner = CliRunner()
    result = runner.invoke(main, ['offices'])
    assert result.exit_code == 0

    with open('tests/cassettes/offices.out', 'r') as f:
        out = f.read()

    assert out == result.output
