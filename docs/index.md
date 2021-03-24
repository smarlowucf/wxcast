# wxcast

A CLI utility for retrieving weather information.

![wxcast metar](https://raw.githubusercontent.com/smarlowucf/wxcast/master/images/metar.png)
![wxcast decoded metar](https://raw.githubusercontent.com/smarlowucf/wxcast/master/images/metar-decoded.png)

## Overview

Provides weather information in the terminal:

-   Weather text information from NWS API.
-   METAR and conditions info from NWS API and python-metar.
-   Seven day forecasts based on location using geopy and NWS API.

## Installation

    pip install wxcast

## Usage

### Conditions

Provides the current weather conditions at a given weather station:

    >>> wxcast conditions -t F kdik
           time:  Wed Mar 24 22:56:00 2021
    temperature:  48.9 F
      dew point:  16.0 F
           wind:  S at 11 knots
     visibility:  10 miles
       pressure:  1005.4 mb
            sky:  clear

###  METAR

Provides the METAR information for a given airport ICAO:

    >>> wxcast metar kden
    KDEN 232253Z 36018KT 10SM FEW033 BKN065 BKN200 04/M03 A2985 RMK AO2 SLP104 T00441028 $

The data can be decoded and pretty printed to terminal using the
-d/--decoded option.

    >>> wxcast metar -d kden
    At Tue Mar 23 22:53:00 2021 the conditions are:

               station:  KDEN
                  type:  routine report, cycle 23 (automatic report)
                  time:  Tue Mar 23 22:53:00 2021
           temperature:  4.4 C
             dew point:  -2.8 C
                  wind:  N at 18 knots
            visibility:  10 miles
              pressure:  1010.8 mb
                   sky:  a few clouds at 3300 feet, broken clouds at 6500 feet,
                         broken clouds at 20000 feet
    sea level pressure:  1010.4 mb
               remarks:  Automated station (type 2)$
             elevation:  5433ft (1656m)

### Products

Provides the available text products for a given WFO (weather forecast
office).

    >>> wxcast products bou
    AFD:  Area Forecast Discussion
    CAP:  Common Alerting Protocol
    FDI:  Fire Danger Indices
    FWF:  Routine Fire Wx Fcst (With/Without 6-10 Day Outlook)
    FWL:  Land Management Forecasts
    FWM:  Miscellaneous Fire Weather Product
    FWN:  Fire Weather Notification
    FWO:  Fire Weather Observation
    FWS:  Suppression Forecast
    HML:  AHPS XML
    HRR:  Weather Roundup
    HWO:  Hazardous Weather Outlook
    OSO:  Other Surface Observations
    PFM:  Point Forecast Matrices
    PNS:  Public Information Statement
    RFW:  Red Flag Warning
    RR2:  Hydro-Met Data Report Part 2
    RR3:  Hydro-Met Data Report Part 3
    RR9:  Hydro-Met Data Report Part 9
    RRS:  HADS Data
    RTP:  Regional Max/Min Temp and Precipitation Table
    SRG:  Soaring Guidance
    STQ:  Spot Forecast Request
    SYN:  Regional Weather Synopsis
    TVL:  Travelers Forecast
    VFT:  Terminal Aerodrome Forecast (TAF) Verification
    ZFP:  Zone Forecast Product

### Text Product

Provides the text information for the given product and WFO. Displays
text in a pager window for easier reading and scrolling.

    >>> wxcast text bou afd

### Forecast

Provides the seven day NWS forecast for the given location.

    >>> wxcast forecast denver
            Tonight:  Rain showers likely. Cloudy. Low around 42, with temperatures
                      rising to around 45 overnight. North northeast
                      wind around 7 mph. Chance of precipitation is
                      60%. New rainfall amounts less than a tenth of an
                      inch possible.
             Monday:  A chance of rain showers. Mostly cloudy, with a high near 53.
                      North northeast wind around 7 mph. Chance of
                      precipitation is 30%. New rainfall amounts less
                      than a tenth of an inch possible.
       Monday Night:  A slight chance of showers and thunderstorms before midnight.
                      Mostly cloudy, with a low around 41. South
                      southeast wind around 3 mph. Chance of
                      precipitation is 20%. New rainfall amounts less
                      than a tenth of an inch possible.
    ...

The location can be a city, address or zip/postal code.

    >>> wxcast forecast 80303
    ...

If there are spaces in the location it must be surrounded by quotes.

    >>> wxcast forecast "325 Broadway Boulder, CO"
    ...

### Weather Forecast Offices (WFO List)

Provides information about NWS forecast offices.

    >>> wxcast offices
    ABQ:  Albuquerque, NM
    ABR:  Aberdeen, SD
    AER:  Anchorage East
    AFC:  Anchorage, AK
    AFG:  Fairbanks, AK
    AJK:  Juneau, AK
    AKQ:  Wakefield, VA
    ALU:  Anchorage West
    ALY:  Albany, NY
    AMA:  Amarillo, TX
    APX:  Gaylord, MI
    ARX:  La Crosse, WI
    BGM:  Binghamton, NY
    BIS:  Bismarck, ND
    BMX:  NWS Birmingham, Alabama
    BOI:  Boise, ID
    BOU:  Denver/Boulder, CO
    BOX:  Boston / Norton, MA
    BRO:  Brownsville/Rio Grande Valley, TX
    BTV:  Burlington, VT
    ...

### Weather Forecast Office Information (WFO Info)

Provides information about a given NWS forecast office.

    >>> wxcast office ABQ
       name:  Albuquerque, NM
    address:  2341 Clark Carr Loop SE, Albuquerque, NM 87106-5633
    ...

### Weather Stations (Stations list)

Provides a list of weather stations for a given NWS forecast office.

    >>> wxcast stations bis
    KBIS
    KJMS
    KSDY
    KDIK
    KISN
    KMOT
    KN60
    KHEI
    KDVL
    KBWP
    K20U
    K06D
    KS25
    KGWR
    K9D7
    K46D
    K7L2
    KHZE
    KBAC
    K2D5
    K5H4
    K08D

### Weather Station Information (Weather station info)

Provides information about a given weather station.

    >>> wxcast station kbwp
         name:  Wahpeton, Harry Stern Airport
    time zone:  America/Chicago
    elevation:  968ft (295.0464m)