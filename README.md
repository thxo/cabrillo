cabrillo
---------------------

![build workflow badge](https://github.com/thxo/cabrillo/actions/workflows/test.yml/badge.svg)

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

## Construct a Log

For an up-to-date list of attributes to use in constructing objects
manually, see `cabrillo/cabrillo.py` and `cabrillo/qso.py`. This is helpful if your software maintains QSOs in a different database format and you are just exporting logs in the very end. For example:

```python
>>> from cabrillo import QSO, Cabrillo
>>> from datetime import datetime
# >>> help(QSO)
# >>> help(Cabrillo)
>>> qso1 = QSO('14313', 'PH', datetime.strptime('May 30 2018 10:15PM', '%b %d %Y %I:%M%p'), 'KX0XXX', 'KX9XXX', de_exch=['59', '10', 'CO'], dx_exch=['44', '20', 'IN'], t=None)
>>> cab = Cabrillo(callsign='KX0XXX', email='kx0xxx@example.com', grid_locator='AB12', soapbox=['Son of a gun!', 'DX IS!'])
>>> cab.qso.append(qso1)
>>> print(cab.text())
START-OF-LOG: 3.0
CALLSIGN: KX0XXX
EMAIL: kx0xxx@example.com
GRID-LOCATOR: AB12
CREATED-BY: cabrillo (Python)
SOAPBOX: Son of a gun!
SOAPBOX: DX IS!
QSO: 14313 PH 2018-05-30 2215 KX0XXX 59 10 CO KX9XXX 44 20 IN
END-OF-LOG:
```

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

# Tips

## Ignoring Malorder

Cabrillo logs must be time-sorted. If you want to read files that are
not so sorted, but other than that are Cabrillo files, you can do so by
adding a keyword argument `ignore_order=False` to either `parse_log_file`
or `parse_log_text`. If you do that, the resulting Cabrillo object
will refuse to generate (potentially non-)Cabrillo output.

## Contributing

Pull requests are appreciated! Please test your changes using `pytest`.

```sh
# Activate a virtual environment using your favorite tool.
$ pip -r requirements_test.txt
$ pytest --cov-report term-missing --cov
*snip*
---------- coverage: platform linux, python 3.12.1-final-0 -----------
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
cabrillo/__init__.py           4      0   100%
cabrillo/cabrillo.py          60      0   100%
cabrillo/data.py              44      0   100%
cabrillo/errors.py             3      0   100%
cabrillo/parser.py            62      0   100%
cabrillo/qso.py               59      0   100%
tests/path_helper.py           6      0   100%
tests/test_cabrillo.py        62      0   100%
tests/test_parser_log.py      89      0   100%
tests/test_parser_qso.py      51      0   100%
tests/test_qso.py            100      0   100%
--------------------------------------------------------
TOTAL                        540      0   100%


====================================================================== 24 passed in 0.21s =======================================================================

```
