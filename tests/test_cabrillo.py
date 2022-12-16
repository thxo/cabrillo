"""Test the Cabrillo class."""

from datetime import datetime

import pytest

from cabrillo import Cabrillo, QSO
from cabrillo.data import VALID_CATEGORIES_MAP
from cabrillo.errors import InvalidLogException


def test_all_attributes():
    """Test the functionality of the Cabrillo class when all arguments are
    set."""
    # Modified from https://www.cqwpx.com/cabrillo.htm
    offtime = [
        datetime.strptime("May 30 2009 12:03AM", "%b %d %Y %I:%M%p"),
        datetime.strptime("May 30 2009 12:05AM", "%b %d %Y %I:%M%p"),
    ]
    qso = [
        QSO(
            "7005",
            "CW",
            datetime.strptime("May 30 2009 12:02AM", "%b %d %Y %I:%M%p"),
            "AA1ZZZ",
            "S50A",
            de_exch=["599", "1"],
            dx_exch=["599", "4"],
            t=None,
        ),
        QSO(
            "7007",
            "CW",
            datetime.strptime("May 30 2009 12:02AM", "%b %d %Y %I:%M%p"),
            "AA1XZZ",
            "S50A",
            de_exch=["599", "1"],
            dx_exch=["599", "4"],
            t=None,
            valid=False,
        ),
        QSO(
            "7006",
            "CW",
            datetime.strptime("May 30 2009 12:15AM", "%b %d %Y %I:%M%p"),
            "AA1ZZZ",
            "EF8M",
            de_exch=["599", "2"],
            dx_exch=["599", "34"],
            t=None,
        ),
        QSO(
            "7008",
            "CW",
            datetime.strptime("May 30 2009 12:17AM", "%b %d %Y %I:%M%p"),
            "AA1ZZZ",
            "EF8M",
            de_exch=["599", "2"],
            dx_exch=["599", "34"],
            t=None,
            valid=False,
        ),
    ]
    x_qso = [qso[1], qso[3]]
    valid_qso = [qso[0], qso[2]]
    cab = Cabrillo(
        callsign="AA1ZZZ",
        contest="CQ-WPX-CW",
        category_operator="SINGLE-OP",
        category_assisted="NON-ASSISTED",
        category_band="ALL",
        category_power="HIGH",
        category_mode="CW",
        category_transmitter="ONE",
        category_overlay="TB-WIRES",
        category_station="FIXED",
        category_time="24-HOURS",
        certificate=True,
        email="test@test.arpa",
        offtime=offtime,
        claimed_score=24,
        club="Yankee Clipper Contest Club",
        location="WMA",
        created_by="WriteLog V10.72C",
        name="Randy Thompson",
        address=["11 Hollis Street"],
        address_city="Uxbridge",
        address_state_province="MA",
        address_postalcode="01569",
        address_country="USA",
        operators=["K5ZD", "KX0XXX"],
        qso=qso,
        soapbox=["Put your comments here.", "Use multiple lines if needed."],
        x_anything={"X-TEST-1": "ignore"},
    )

    # Test constructor.
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
    assert cab.category_station == "FIXED"
    assert cab.category_time == "24-HOURS"
    assert cab.certificate is True
    assert cab.email == "test@test.arpa"
    assert cab.offtime == offtime
    assert cab.claimed_score == 24
    assert cab.club == "Yankee Clipper Contest Club"
    assert cab.location == "WMA"
    assert cab.created_by == "WriteLog V10.72C"
    assert cab.address == ["11 Hollis Street"]
    assert cab.address_city == "Uxbridge"
    assert cab.address_state_province == "MA"
    assert cab.address_postalcode == "01569"
    assert cab.address_country == "USA"
    assert cab.operators == ["K5ZD", "KX0XXX"]
    assert cab.qso == qso
    assert cab.x_qso == x_qso
    assert cab.valid_qso == valid_qso
    assert cab.soapbox == ["Put your comments here.", "Use multiple lines if needed."]

    # Writing test.
    correct = """START-OF-LOG: 3.0
CALLSIGN: AA1ZZZ
OPERATORS: K5ZD KX0XXX
CONTEST: CQ-WPX-CW
CLAIMED-SCORE: 24
CERTIFICATE: YES
CATEGORY-OPERATOR: SINGLE-OP
CATEGORY-ASSISTED: NON-ASSISTED
CATEGORY-BAND: ALL
CATEGORY-POWER: HIGH
CATEGORY-MODE: CW
CATEGORY-STATION: FIXED
CATEGORY-TIME: 24-HOURS
CATEGORY-TRANSMITTER: ONE
CATEGORY-OVERLAY: TB-WIRES
OFFTIME: 2009-05-30 0003 2009-05-30 0005
CLUB: Yankee Clipper Contest Club
NAME: Randy Thompson
EMAIL: test@test.arpa
LOCATION: WMA
ADDRESS: 11 Hollis Street
ADDRESS-CITY: Uxbridge
ADDRESS-STATE-PROVINCE: MA
ADDRESS-POSTALCODE: 01569
ADDRESS-COUNTRY: USA
CREATED-BY: WriteLog V10.72C
SOAPBOX: Put your comments here.
SOAPBOX: Use multiple lines if needed.
X-TEST-1: ignore
QSO: 7005 CW 2009-05-30 0002 AA1ZZZ 599 1 S50A 599 4
X-QSO: 7007 CW 2009-05-30 0002 AA1XZZ 599 1 S50A 599 4
QSO: 7006 CW 2009-05-30 0015 AA1ZZZ 599 2 EF8M 599 34
X-QSO: 7008 CW 2009-05-30 0017 AA1ZZZ 599 2 EF8M 599 34
END-OF-LOG:
"""
    assert correct == cab.text()


def test_unicode():
    """Test the functionality of the Cabrillo class when there is Unicode text."""
    cab = Cabrillo(callsign="VR2TEST", address=["毛澤大道東89號", "鶴咀"], address_city="石澳")
    correct = """START-OF-LOG: 3.0
CALLSIGN: VR2TEST
ADDRESS: 毛澤大道東89號
ADDRESS: 鶴咀
ADDRESS-CITY: 石澳
CREATED-BY: cabrillo (Python)
END-OF-LOG:
"""
    assert correct == cab.text()


def test_yes_no():
    """Test the conversion from boolean to YES/NO."""
    assert (
        "CERTIFICATE: YES" in Cabrillo(callsign="TEST100TEST", certificate=True).text()
    )
    assert (
        "CERTIFICATE: NO" in Cabrillo(callsign="TEST100TEST", certificate=False).text()
    )


def test_exceptions():
    """Test exceptions thrown in Cabrillo."""
    # If we do not enable checking, it should construct properly.
    assert Cabrillo(
        callsign="TEST100TEST", category_power="ITALIAN-QRP", check_categories=False
    )

    for category in VALID_CATEGORIES_MAP.keys():
        with pytest.raises(InvalidLogException) as _:
            Cabrillo(callsign="TEST100TEST", **{category: "ABSOLUTE-JUNK-DATA"})

    # For now, this program only supports Cabrillo v3.
    with pytest.raises(InvalidLogException) as _:
        Cabrillo(callsign="TEST100TEST", version="2.0")

    # Check if version changed mid-way.
    with pytest.raises(InvalidLogException) as _:
        cab = Cabrillo(callsign="TEST100TEST", version="3.0")
        cab.version = 2.0
        cab.text()
