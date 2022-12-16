"""Test the parsing of Cabrillo logs."""
from datetime import datetime

import pytest

from cabrillo import QSO
from cabrillo.errors import InvalidLogException
from cabrillo.parser import parse_log_file, parse_log_text


def test_parse_cqwpx():
    """Test valid logs from CQWPX."""
    for filename in ["tests/CQWPX.log", "tests/CQWPX_bad_style.log"]:
        cab = parse_log_file(filename)

        assert str(cab) == "<Cabrillo for AA1ZZZ>"
        assert cab.version == "3.0"
        assert cab.callsign == "AA1ZZZ"
        assert cab.contest == "CQ-WPX-CW"
        assert cab.category_operator == "SINGLE-OP"
        assert cab.category_assisted == "NON-ASSISTED"
        assert cab.category_band == "ALL"
        assert cab.category_power == "HIGH"
        assert cab.category_mode == "CW"
        assert cab.category_transmitter == "ONE"
        assert cab.category_overlay == "TB-WIRES"
        assert cab.claimed_score == 24
        assert cab.club == "Yankee Clipper Contest Club"
        assert cab.location == "WMA"
        assert cab.created_by == "WriteLog V10.72C"
        assert cab.address == ["11 Hollis Street"]
        assert cab.address_city == "Uxbridge"
        assert cab.address_state_province == "MA"
        assert cab.address_postalcode == "01569"
        assert cab.address_country == "USA"
        assert cab.operators == ["AA1XXX", "AA2XXX", "AA3XXX"]
        assert cab.soapbox == [
            "Put your comments here.",
            "Use multiple lines if needed.",
            'Once you said "SOAPBOX:", the rest of the line is free-form.',
        ]

        out_lines = cab.text()
        with open("tests/CQWPX.log") as infile:
            correct_lines = infile.read()
        assert out_lines == correct_lines


def test_parse_iaru():
    cab = parse_log_file("tests/iaru.log")
    assert cab.operators == ["@DJ3EI"]
    assert 2 == len(cab.qso)
    assert cab.qso[0].dx_exch == ["599", "REF"]
    assert cab.qso[0].dx_call == "TM0HQ"
    assert 1 == len(cab.valid_qso)
    assert cab.valid_qso[0].dx_call == "EI0HQ"
    assert 1 == len(cab.x_qso)
    assert cab.x_qso[0].dx_exch == ["599", "REF"]


def test_badorder():
    with pytest.raises(InvalidLogException) as _:
        parse_log_file("tests/badorder.log")
    cab_unordered = parse_log_file("tests/badorder.log", ignore_order=True)
    with pytest.raises(InvalidLogException) as _:
        cab_unordered.text()


def test_parse_yarc():
    """Test a log file from the YARC QSO Party."""
    cab = parse_log_file("tests/YARC.log")
    assert cab.certificate is True
    # Check the X-... come out in the order they occure in the file.
    # (This is not demanded by the Cabrillo spec, but seems sensible to do.)
    x_anything_items = list(cab.x_anything.items())
    assert 3 == len(x_anything_items)
    assert x_anything_items[0] == ("X-LOREM", "Ipsum")
    assert x_anything_items[1] == ("X-ORDER", "Maybe matters.")
    assert x_anything_items[2] == ("X-BUS-ROUTE", "372")

    qso = QSO(
        "14200",
        "PH",
        datetime.strptime("Dec 01 2018 2:20PM", "%b %d %Y %I:%M%p"),
        "W200YARC",
        "K4NYX",
        de_exch=["19", "NY"],
        dx_exch=["045", "FL"],
        t=None,
    )
    x_qso = QSO(
        "7127",
        "PH",
        datetime.strptime("Dec 01 2018 9:11PM", "%b %d %Y %I:%M%p"),
        "W200YARC",
        "W9JWC",
        de_exch=["19", "NY"],
        dx_exch=["021", "IL"],
        t=None,
    )

    assert cab.qso[0] == qso
    assert cab.x_qso[0] == x_qso


def test_parse_unknown_keyword():
    """Test a log file with a junk keyword."""
    bad_text = "START-OF-LOG: 3.0\nDOGS-SHOULD-VOTE: YES"

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)

    # When ignored is toggled, should not complain.
    assert parse_log_text(bad_text, ignore_unknown_key=True)


def test_parse_bad():
    """Test a badly delimited log."""
    bad_text = "START-OF-LOG: 3.0\nblah"

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)


def test_parse_bad_claimed_score():
    """Test a badly formatted log with claim score that has unwanted number
    formatting.
    """
    bad_text = "START-OF-LOG: 3.0\nCLAIMED-SCORE: 12,345,678"

    with pytest.raises(InvalidLogException) as _:
        parse_log_text(bad_text)
