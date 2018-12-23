cabrillo [![Build Status](https://travis-ci.com/thxo/cabrillo.svg?branch=master)](https://travis-ci.com/wubcrow/cabrillo)
---------------------
A Python library to parse Cabrillo-format amateur radio contest logs. 

# Getting Started
```python
>>> from cabrillo.parser import parse_log_file
>>> cab = parse_log_file('tests/CQWPX.log')
>>> cab.callsign
'AA1ZZZ'
>>> cab.qso
[<cabrillo.qso.QSO object at 0x10cb09f28>, <cabrillo.qso.QSO object at 0x10cbc8860>]
>>> cab.write_text()
'START-OF-LOG: 3.0\nCALLSIGN: AA1ZZZ\nCONTEST: CQ-WPX-CW\n[...snip...]END-OF-LOG:'
```

# Attributes
Use these attributes to access and construct individual objects.

```
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
 |        multi-op.
 |        category_overlay: One of CATEGORY-OVERLAY.
 |        certificate: If certificate by post. Boolean.
 |        claimed_score: Claimed score in int.
 |        club: Club represented.
 |        created_by: Software responsible for creating this log file.
 |        Optional and defaults to "cabrillo (Python)".
 |        email: Email address of the submitter.
 |        location: State/section/ID depending on contest.
 |        name: Name.
 |        address: Mailing address in list, each entry is each line.
 |        address_city: Optional granular address info.
 |        address_state_province: Optional granular address info.
 |        address_postalcode: Optional granular address info.
 |        address_country: Optional granular address info.
 |        operators: List containing each operator's callsign of the station.
 |        offtime: List containing two datetime objects denoting start and
 |        end of off-time.
 |        soapbox: List containing each line of soapbox text at their own entry.
 |        qso: QSO data containing QSO objects.
 |        x_qso: Ignored QSO data containing QSO objects.
 |        x_anything: A dict of ignored/unknown attributes.
```
 
 ```
 class QSO(builtins.object)
 |  QSO(freq, mo, date, de_call, dx_call, de_exch=None, dx_exch=None, t=None)
 |  
 |  Representation of a single QSO.
 |  
 |  Attributes:
 |      freq: Frequency in str representation.
 |      mo: Two letter of QSO. See MODES.
 |      date: UTC time in datetime.datetime object.
 |      de_call: Sent callsign.
 |      de_exch: Sent exchange incl. RST. List of each component.
 |      dx_call: Received callsign.
 |      dx_exch: Received exchange incl. RST. List of each component.
 |      t: Transmitter ID for multi-transmitter categories in int. 0/1.
 ```