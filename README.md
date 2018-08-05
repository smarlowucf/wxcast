# wxcast

A CLI utility for retrieving weather information.

[![Build Status](https://travis-ci.org/smarlowucf/wxcast.svg?branch=master)](https://travis-ci.org/smarlowucf/wxcast)

![wxcast metar](https://raw.githubusercontent.com/smarlowucf/wxcast/master/images/metar.gif)

## Overview

Provides weather information in terminal:

-   Weather text information from NWS API.
-   METAR info from AVWX API.
-   Seven day forecasts based on location using geopy and NWS API.

## Installation

    pip install wxcast

## Requirements

-   certifi
-   Click&gt;=6.0
-   geopy
-   requests

## Test Requirements

-   flake8
-   pytest
-   pytest-cov
-   vcrpy

## [Docs](https://smarlowucf.github.io/wxcast/)

## Issues/Enhancements

Please submit issues and requests to
[Github](https://github.com/smarlowucf/wxcast/issues).

## Contributing

Contributions to **wxcast** are welcome and encouraged. See
[CONTRIBUTING](https://github.com/smarlowucf/wxcast/blob/master/CONTRIBUTING.md)
for info on getting started.

## License

Copyright (c) 2017 Sean Marlow.

Distributed under the terms of GPL-3.0+ license, see
[LICENSE](https://github.com/smarlowucf/wxcast/blob/master/LICENSE)
for details.
