# wxcast

A CLI utility for retrieving weather information.

[![Build Status](https://github.com/smarlowucf/wxcast/actions/workflows/test.yml/badge.svg)](https://github.com/smarlowucf/wxcast/actions/workflows/test.yml)

![wxcast decoded metar](https://raw.githubusercontent.com/smarlowucf/wxcast/master/images/metar-decoded.png)

## Overview

Provides weather information in terminal:

-   Weather text information from NWS API.
-   METAR info from NWS API.
-   Seven day forecasts based on location using geopy and NWS API.

## Installation

    pip install wxcast

## Requirements

- certifi
- Click&gt;=6.0
- geopy
- requests
- metar

## Test Requirements

- flake8
- pytest
- pytest-cov
- vcrpy

## [Docs](https://smarlowucf.github.io/wxcast/)

## Issues/Enhancements

Please submit issues and requests to
[Github](https://github.com/smarlowucf/wxcast/issues).

## Contributing

Contributions to **wxcast** are welcome and encouraged. See
[CONTRIBUTING](https://github.com/smarlowucf/wxcast/blob/master/CONTRIBUTING.md)
for info on getting started.

## License

Copyright (c) 2021 Sean Marlow.

Distributed under the terms of MIT license, see
[LICENSE](https://github.com/smarlowucf/wxcast/blob/master/LICENSE)
for details.
