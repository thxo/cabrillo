cabrillo [![Build Status](https://travis-ci.com/thxo/cabrillo.svg?branch=master)](https://travis-ci.com/thxo/cabrillo)
---------------------
A Python library to parse Cabrillo-format amateur radio contest logs, with no external dependencies.

# Getting Started

## Basic Parsing

```python
>>> from cabrillo.parser import parse_log_file
>>> cab = parse_log_file('tests/CQWPX.log')
>>> cab.callsign
'AA1ZZZ'
>>> cab.qso
[<cabrillo.qso.QSO object at 0x10cb09f28>, <cabrillo.qso.QSO object at 0x10cbc8860>]
>>> cab.text()
'START-OF-LOG: 3.0\nCREATED-BY: WriteLog V10.72C\nCALLSIGN: AA1ZZZ\n[...snip...]END-OF-LOG:\n'
```

You can also write to a file:

```python
with open('out.cbr', 'w') as o:
    cab.write(o)
```

The same works for text-file-like objects.

Finally, if you desire to parse Cabrillo data already present as a Python string,
you can do so with, e.g.,

```python
from cabrillo.parser import parse_log_text

cabrillo_text = """START-OF-LOG: 3.0
END-OF-LOG:
"""

cab = parse_log_text(cabrillo_text)
```

## Ignoring malorder

Cabrillo logs must be time-sorted. If you want to read files that are
not so sorted, but other than that are Cabrillo files, you can do so by
adding a keyword argument `ignore_order=False` to either `parse_log_file`
or `parse_log_text`. If you do that, the resulting Cabrillo object
will refuse to generate (potentially non-)Cabrillo output.

## Matching Two QSOs in Contest Scoring

```python
>>> # We start off with a pair with complementary data.
>>> from cabrillo import QSO
>>> from datetime import datetime
>>> qso1 = QSO('14313', 'PH', datetime.strptime('May 30 2018 10:15PM', '%b %d %Y %I:%M%p'), 'KX0XXX', 'KX9XXX', de_exch=['59', '10', 'CO'], dx_exch=['44', '20', 'IN'], t=None)
>>> qso2 = QSO('14313', 'PH', datetime.strptime('May 30 2018 10:10PM', '%b %d %Y %I:%M%p'), 'KX9XXX', 'KX0XXX', de_exch=['44', '20', 'IN'], dx_exch=['59', '10', 'CO'], t=None)
>>> qso1.match_against(qso2)
True
>>> qso1.freq = '14000'  # Same band, still will match.
>>> qso1.match_against(qso2)
True
>>> qso1.match_against(qso2, max_time_delta=1)  # Make time checking less lenient.
False
>>> # All flags.
>>> qso1.match_against(qso2, max_time_delta=30, check_exch=True, check_band=True)
```

# Attributes

Use these attributes to access and construct individual objects.

```python
class Cabrillo(builtins.object)
 |  Cabrillo(check_categories=True, **d)
 |  
 |  Representation of a Cabrillo log file.
 |  
 |  Attributes:
 |        version: The only supported version is '3.0'.
 |        callsign: Call sign of station.
 |        contest: Contest identification.
 |        category_assisted: One of CATEGORY_ASSISTED.
 |        category_band: One of CATEGORY_BAND.
 |        category_mode: One of CATEGORY_MODE.
 |        category_operator: One of CATEGORY_OPERATOR.
 |        category_power: One of CATEGORY-POWER.
 |        category_station: One of CATEGORY-STATION.
 |        category_time: One of CATEGORY-TIME.
 |        category_transmitter: One of CATEGORY-TRANSMITTER. Optional for
 |          multi-op.
 |        category_overlay: One of CATEGORY-OVERLAY.
 |        certificate: If certificate by post. Boolean.
 |        claimed_score: Claimed score in int.
 |        club: Club represented.
 |        created_by: Software responsible for creating this log file.
 |          Optional, defaults to "cabrillo (Python)".
 |        email: Email address of the submitter.
 |        location: State/section/ID depending on contest.
 |        name: Log submitter's name.
 |        address: Mailing address, as a list, one entry per line.
 |        address_city: Optional granular address info.
 |        address_state_province: Optional granular address info.
 |        address_postalcode: Optional granular address info.
 |        address_country: Optional granular address info.
 |        operators: List of operators' callsigns.
 |        offtime: List containing two datetime objects denoting start and
 |          end of off-time.
 |        soapbox: List of lines of soapbox text.
 |        qso: List of all QSO objects, including ignored QSOs.
 |        valid_qso: List of all valid QSOs (excluding X-QSO) (read-only).
 |        x_qso: List of QSO objects for ignored QSOs (X-QSO only) (read-only).
 |        x_anything: An ordered mapping of ignored/unknown attributes of the Cabrillo file.
```

```python
 class QSO(builtins.object)
 |  QSO(freq, mo, date, de_call, dx_call, de_exch=[], dx_exch=[], t=None, valid=True)
 |  
 |  Representation of a single QSO.
 |  
 |  Attributes:
 |      freq: Frequency in kHz in str representation.
 |      mo: Transmission mode of QSO.
 |      date: UTC time as datetime.datetime object.
 |      de_call: Sent callsign.
 |      de_exch: Sent exchange. List, first item is RST, second tends to be context exchange.
 |      dx_call: Received callsign.
 |      dx_exch: Received exchange. List, first item is RST, second tends to be context exchange.
 |      t: Transmitter ID for multi-transmitter categories in int. 0/1.
 |      valid: True for QSO that counts, False for an X-QSO.
```

## Contributors

Pull requests are appreciated!

The following instructions show how to obtain the sourcecode and execute the tests.
They assume Python 3.3 or later: 

```sh
git clone https://github.com/thxo/cabrillo.git
cd cabrillo
python3 -m venv python-venv
source python-venv/bin/activate
pip install -r requirements_test.txt
python -m pytest --cov-report term-missing --cov cabrillo -v
```

On a Windows machine, using `cmd.exe`, substitute
`python-venv/Scripts/activate` for
`source python-venv/bin/activate`.
