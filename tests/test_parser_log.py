"""Test the parsing of Cabrillo logs."""
from datetime import datetime

import pytest

import path_helper

from cabrillo import QSO
from cabrillo.errors import InvalidLogException, InvalidQSOException
from cabrillo.parser import parse_log_file, parse_log_text


def test_parse_cqwpx():
    """Test valid logs from CQWPX."""
    for filename in ['tests/CQWPX.log', 'tests/CQWPX_bad_style.log']:
        cab = parse_log_file(filename)

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
        assert cab.category_station == 'DISTRIBUTED'
        assert cab.claimed_score == 24
        assert cab.club == 'Yankee Clipper Contest Club'
        assert cab.location == 'WMA'
        assert cab.created_by == 'WriteLog V10.72C'
        assert cab.address == ['11 Hollis Street']
        assert cab.address_city == 'Uxbridge'
        assert cab.address_state_province == 'MA'
        assert cab.address_postalcode == '01569'
        assert cab.address_country == 'USA'
        assert cab.operators == ['AA1XXX', 'AA2XXX', 'AA3XXX']
        assert cab.soapbox == ['Put your comments here.',
                               'Use multiple lines if needed.',
                               'Once you said "SOAPBOX:", the rest of the line is free-form.']

        out_lines = cab.text()
        with open('tests/CQWPX.log') as infile:
            correct_lines = infile.read()
        assert out_lines == correct_lines

def test_parse_cqwpx_claimed_score_empty():
    cab = parse_log_file('tests/CQWPX_claimed_score_empty.log')
    assert 0 == cab.claimed_score

def test_parse_iaru():
    cab = parse_log_file('tests/iaru.log')
    assert cab.operators == ['@DJ3EI']
    assert 2 == len(cab.qso)
    assert cab.qso[0].dx_exch == ["599", "REF"]
    assert cab.qso[0].dx_call == "TM0HQ"
    assert 1 == len(cab.valid_qso)
    assert cab.valid_qso[0].dx_call == "EI0HQ"
    assert 1 == len(cab.x_qso)
    assert cab.x_qso[0].dx_exch == ["599", "REF"]


def test_badorder():
    with pytest.raises(InvalidLogException) as _:
        parse_log_file('tests/badorder.log')
    cab_unordered = parse_log_file('tests/badorder.log', ignore_order=True)
    with pytest.raises(InvalidLogException) as _:
        cab_unordered.text()


def test_parse_yarc():
    """Test a log file from the YARC QSO Party."""
    cab = parse_log_file('tests/YARC.log')
    assert cab.certificate is True
    # Check the X-... come out in the order they occure in the file.
    # (This is not demanded by the Cabrillo spec, but seems sensible to do.)
    x_anything_items = list(cab.x_anything.items())
    assert 3 == len(x_anything_items)
    assert x_anything_items[0] == ('X-LOREM', 'Ipsum')
    assert x_anything_items[1] == ('X-ORDER', 'Maybe matters.')
    assert x_anything_items[2] == ('X-BUS-ROUTE', '372')

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


def test_parse_grid_locator():
    """Test that the GRID-LOCATOR keyword is parsed correctly."""
    empty = (None, "START-OF-LOG: 3.0\nGRID-LOCATOR:")
    short = ("FK42", "START-OF-LOG: 3.0\nGRID-LOCATOR: FK42")
    long = ("FK42AA", "START-OF-LOG: 3.0\nGRID-LOCATOR: FK42aA")
    spaces = ("FK42AA", "START-OF-LOG: 3.0\nGRID-LOCATOR:    FK42AA   ")

    for grid, text in [empty, short, long, spaces]:
        cab = parse_log_text(text)
        assert cab.grid_locator == grid

    bad_grids = ["00aa", "fk4200", "fk42AAA", "00fk42", "fk42a", "fk42a0"]
    for grid in bad_grids:
        bad_text = "START-OF-LOG: 3.0\nGRID-LOCATOR: {}".format(grid)
        with pytest.raises(InvalidLogException) as _:
            parse_log_text(bad_text)


def test_parse_extended_grid_locator():
    extended_8 = ("FN42EB12", "START-OF-LOG: 3.0\nGRID-LOCATOR: FN42eb12")
    extended_10 = ("FN42EB12AB", "START-OF-LOG: 3.0\nGRID-LOCATOR: fn42eb12ab")

    for grid, text in [extended_8, extended_10]:
        cab = parse_log_text(text)
        assert cab.grid_locator == grid


def test_empty_grid_locator_is_none():
    """Test that an empty GRID-LOCATOR is stored as None, not empty string."""
    text = "START-OF-LOG: 3.0\nGRID-LOCATOR:\nEND-OF-LOG:\n"
    cab = parse_log_text(text)
    assert cab.grid_locator is None


def test_claimed_score_zero_roundtrip():
    """Test that claimed_score=0 survives roundtrip (not dropped as falsy)."""
    text = "START-OF-LOG: 3.0\nCLAIMED-SCORE: 0\nEND-OF-LOG:\n"
    cab = parse_log_text(text)
    assert cab.claimed_score == 0
    output = cab.text()
    assert 'CLAIMED-SCORE: 0' in output
    cab2 = parse_log_text(output)
    assert cab2.claimed_score == 0


def test_offtime_roundtrip():
    text = "START-OF-LOG: 3.0\nOFFTIME: 2009-05-30 0003 2009-05-30 0500\nEND-OF-LOG:\n"
    cab = parse_log_text(text)
    assert cab.offtime == [datetime(2009, 5, 30, 0, 3),
                           datetime(2009, 5, 30, 5, 0)]
    output = cab.text()
    assert 'OFFTIME: 2009-05-30 0003 2009-05-30 0500' in output
    cab2 = parse_log_text(output)
    assert cab2.offtime == cab.offtime


def test_parse_nonstandard_mode_check_mode_false():
    text = ("START-OF-LOG: 3.0\n"
            "QSO: 14000 CW/DIGITAL 2020-01-01 0000 W1AW 599 1 VA2RAC 599 4\n"
            "END-OF-LOG:\n")
    with pytest.raises(InvalidQSOException):
        parse_log_text(text)
    cab = parse_log_text(text, check_mode=False)
    assert cab.qso[0].mo == 'CW/DIGITAL'


def test_parse_laqp():
    # Non-standard mode CW/Digital
    with pytest.raises(InvalidQSOException):
        parse_log_file('tests/LAQP.log')
    cab = parse_log_file('tests/LAQP.log', check_mode=False)
    assert cab.callsign == 'KX5XXX'
    assert cab.contest == 'LA-QSO-PARTY'
    assert cab.claimed_score == 0  # empty -> 0
    assert cab.category_station == 'ROVER'
    assert cab.operators == ['KX5XXX', '@KX5XXX']
    assert cab.qso[0].mo == 'CW/Digital'
    assert cab.qso[0].de_exch == ['599', 'BEAU']
    assert cab.qso[0].dx_exch == ['599', 'ORLE']


def test_parse_gb0wr():
    # Bare 'CATEGORY:' is a DXLog.net vendor extension
    with pytest.raises(InvalidLogException):
        parse_log_file('tests/GB0WR.log')
    cab = parse_log_file('tests/GB0WR.log', ignore_unknown_key=True)
    assert cab.callsign == 'GB0WR'
    assert cab.contest == 'IARU-HF'
    assert cab.grid_locator == 'JO02JI'
    assert cab.operators == ['G4CWH', 'EI6JK']
    assert len(cab.qso) == 4
    # Multi-TX QSOs with transmitter id
    assert cab.qso[0].t == 0
    assert cab.qso[0].de_exch == ['599', '27']
    assert cab.qso[0].dx_exch == ['599', '29']
    # HQ-station exchange (society abbreviation)
    assert cab.qso[3].dx_exch == ['599', 'BFRA']


def test_parse_i44z():
    # Multi-TX log with ordering violation between TX streams.
    with pytest.raises(InvalidLogException):
        parse_log_file('tests/I44Z.log')
    cab = parse_log_file('tests/I44Z.log', ignore_order=True)
    assert cab.callsign == 'I44Z'
    assert cab.category_transmitter == 'TWO'
    assert len(cab.qso) == 6
    # TX0 (CW, t=0) and TX1 (PH, t=1) interleaved
    assert cab.qso[2].t == 0
    assert cab.qso[2].mo == 'CW'
    assert cab.qso[3].t == 1
    assert cab.qso[3].mo == 'PH'
    # Output refused in ignore_order mode
    with pytest.raises(InvalidLogException):
        cab.text()


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
