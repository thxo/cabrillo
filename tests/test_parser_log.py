"""Test the parsing of Cabrillo logs."""
from datetime import datetime

import pytest

from cabrillo import QSO
from cabrillo.errors import InvalidLogException
from cabrillo.parser import parse_log_file, parse_log_text


def test_parse_cqwpx():
    """Test a well-formatted log from CQWPX."""
    cab = parse_log_file('tests/CQWPX.log')

    assert str(cab) == '<Cabrillo for AA1ZZZ>'
    assert cab.version == '3.0'
    assert cab.callsign == 'AA1ZZZ'
    assert cab.contest == 'CQ-WPX-CW'
    assert cab.category_operator == 'SINGLE-OP'
    assert cab.category_assisted == 'NON-ASSISTED'
    assert cab.category_band == 'ALL'
    assert cab.category_power == 'HIGH'
    assert cab.category_mode == 'CW'
    assert cab.category_transmitter == 'ONE'
    assert cab.category_overlay == 'TB-WIRES'
    assert cab.claimed_score == 24
    assert cab.club == 'Yankee Clipper Contest Club'
    assert cab.location == 'WMA'
    assert cab.created_by == 'WriteLog V10.72C'
    assert cab.address == ['11 Hollis Street']
    assert cab.address_city == 'Uxbridge'
    assert cab.address_state_province == 'MA'
    assert cab.address_postalcode == '01569'
    assert cab.address_country == 'USA'
    assert cab.operators == ['K5ZD']
    assert cab.soapbox == ['Put your comments here.',
                           'Use multiple lines if needed.']

    out_lines = cab.write_text().split('\n')
    correct_lines = open('tests/CQWPX.log').read().split('\n')
    assert len(out_lines) == len(correct_lines) and sorted(
        out_lines) == sorted(correct_lines)


def test_parse_yarc():
    """Test a log file from the YARC QSO Party."""
    cab = parse_log_file('tests/YARC.log')
    assert cab.certificate is True
    assert cab.x_anything.get('X-BUS-ROUTE', None) == '372'

    qso = QSO('14200', 'PH',
              datetime.strptime('Dec 01 2018 2:20PM', '%b %d %Y %I:%M%p'),
              'W200YARC', 'K4NYX', de_exch=['19', 'NY'], dx_exch=['045', 'FL'],
              t=None)
    x_qso = QSO('7127', 'PH',
                datetime.strptime('Dec 01 2018 9:11PM', '%b %d %Y %I:%M%p'),
                'W200YARC', 'W9JWC', de_exch=['19', 'NY'],
                dx_exch=['021', 'IL'],
                t=None)

    assert cab.qso[0] == qso
    assert cab.x_qso[0] == x_qso


def test_parse_unknown_keyword():
    """Test a log file with a junk keyword."""
    bad_text = 'START-OF-LOG: 3.0\nDOGS-SHOULD-VOTE: YES'

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)

    # When ignored is toggled, should not complain.
    assert parse_log_text(bad_text, ignore_unknown_key=True)


def test_parse_bad():
    """Test a badly delimited log."""
    bad_text = 'START-OF-LOG: 3.0\nblah'

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)


def test_parse_bad_claimed_score():
    """Test a badly formatted log with claim score that has unwanted number
    formatting.
    """
    bad_text = 'START-OF-LOG: 3.0\nCLAIMED-SCORE: 12,345,678'

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)
