"""Test the parsing of Cabrillo logs."""
import pytest

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


def test_parse_cqwpx():
    """Test a badly delimited log."""
    bad_text = 'START-OF-LOG: 3.0\nblah'

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)
