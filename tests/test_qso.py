"""Test the QSO class."""
from datetime import datetime

import pytest

from cabrillo import QSO
from cabrillo.qso import frequency_to_band
from cabrillo.errors import InvalidQSOException


def test_yarc():
    """Test the QSO class with YARC QSO Party exchanges."""
    qso = QSO(
        "14313",
        "PH",
        datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p"),
        "KX0XXX",
        "KX9XXX",
        de_exch=["59", "10", "CO"],
        dx_exch=["44", "20", "IN"],
        t=None,
        valid=False,
    )
    assert qso.freq == "14313"
    assert qso.mo == "PH"
    assert qso.date == datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p")
    assert qso.de_call == "KX0XXX"
    assert qso.dx_call == "KX9XXX"
    assert qso.de_exch == ["59", "10", "CO"]
    assert qso.dx_exch == ["44", "20", "IN"]
    assert qso.t is None
    assert (
        str(qso) == "X-QSO: 14313 PH 2018-05-30 2210 KX0XXX 59 10 CO KX9XXX 44 " "20 IN"
    )


def test_with_xmtr():
    """Test the QSO class with a transmitter designation."""
    qso = QSO(
        "241G",
        "PH",
        datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p"),
        "KX0XXX",
        "KX9XXX",
        de_exch=["59", "CO"],
        dx_exch=["44", "IL"],
        t=1,
    )
    assert qso.freq == "241G"
    assert qso.mo == "PH"
    assert qso.date == datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p")
    assert qso.de_call == "KX0XXX"
    assert qso.dx_call == "KX9XXX"
    assert qso.de_exch == ["59", "CO"]
    assert qso.dx_exch == ["44", "IL"]
    assert qso.t == 1
    assert str(qso) == "QSO: 241G PH 2018-05-30 2210 KX0XXX 59 CO KX9XXX 44 " "IL 1"


def test_invalid_mode():
    """Test the QSO class with invalid modes."""
    with pytest.raises(ValueError) as _:
        QSO(
            freq="LIGHT",
            mo="MCW",       # MCW is *a* mode, but not one that the ADIF or Cabrillo spec supports
            date=datetime.now(),
            de_call="KX0XXX",
            dx_call="KX9XXX",
            valid=True,
        )


def test_automatic_list():
    """Test automatic creation of lists for exchanges."""
    qso = QSO(
        freq="LIGHT",
        mo="CW",
        date=datetime.now(),
        de_call="KX0XXX",
        dx_call="KX9XXX",
        valid=False,
    )
    assert qso.de_exch == []
    assert qso.dx_exch == []


def test_frequency_to_band():
    """Test the frequency_to_band method."""
    # Recognized bands.
    assert frequency_to_band(14000) == "14000"
    assert frequency_to_band(14300) == "14000"
    assert frequency_to_band("14300") == "14000"

    # Other data.
    assert frequency_to_band(100000000) == 100000000
    assert frequency_to_band("100000000") == "100000000"
    assert frequency_to_band("LIGHT") == "LIGHT"


def test_qso_match():
    """Test QSO matching between a pair of QSOs."""
    # We start off with a correct pair with same data.
    qso1 = QSO(
        "14313",
        "PH",
        datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p"),
        "KX0XXX",
        "KX9XXX",
        de_exch=["59", "10", "CO"],
        dx_exch=["44", "20", "IN"],
        t=None,
        valid=True,
    )
    qso2 = QSO(
        "14313",
        "PH",
        datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p"),
        "KX9XXX",
        "KX0XXX",
        de_exch=["44", "20", "IN"],
        dx_exch=["59", "10", "CO"],
        t=None,
        valid=False,
    )

    assert qso1.match_against(qso2) is True
    assert qso2.match_against(qso1) is True

    # Differing callsigns should lead to False.
    qso1.dx_call = "W1AW"
    assert qso1.match_against(qso2) is False
    assert qso2.match_against(qso1) is False
    qso1.dx_call = "KX9XXX"

    # Differing modes should lead to False.
    qso1.mo = "CW"
    assert qso1.match_against(qso2) is False
    assert qso2.match_against(qso1) is False
    qso1.mo = "PH"

    # Times that are two different should lead to False.
    # Exactly 30 minutes difference is allowed by default.
    qso1.date = datetime.strptime("May 30 2018 10:40PM", "%b %d %Y %I:%M%p")
    assert qso1.match_against(qso2) is True
    assert qso2.match_against(qso1) is True
    # Clients may limit the time delta to be less.
    assert qso1.match_against(qso2, max_time_delta=29) is False
    assert qso2.match_against(qso1, max_time_delta=29) is False
    # Also OK to disable checking altogether.
    qso1.date = datetime.now()
    assert qso1.match_against(qso2, max_time_delta=-1) is True
    assert qso2.match_against(qso1, max_time_delta=-1) is True
    # Bad time delta passed should lead to error raised.
    with pytest.raises(ValueError) as _:
        qso1.match_against(qso2, max_time_delta=-100)
    qso1.date = datetime.strptime("May 30 2018 10:10PM", "%b %d %Y %I:%M%p")

    # Differing exchanges should lead to False if we are checking.
    qso1.dx_exch = ["59", "80", "HI"]
    assert qso1.match_against(qso2) is False
    assert qso2.match_against(qso1) is False
    # But otherwise ignored if user explictly disables checking.
    assert qso1.match_against(qso2, check_exch=False) is True
    assert qso2.match_against(qso1, check_exch=False) is True
    qso1.dx_exch = ["44", "20", "IN"]

    # Band checking.
    # Same frequency.
    qso1.freq = "146520"
    qso2.freq = "146520"
    assert qso1.match_against(qso2) is True
    # Same band, differing frequency.
    qso1.freq = "14350"
    qso2.freq = "14300"
    assert qso1.match_against(qso2) is True
    # Different bands, band recognized.
    qso1.freq = "14300"
    qso2.freq = "7000"
    assert qso1.match_against(qso2) is False
    # Different bands, band not recognized.
    qso1.freq = "14300"
    qso2.freq = "143000"
    assert qso1.match_against(qso2) is False
    # Special bands not mentioned in Cabrillo.
    # 10MHz.
    qso1.freq = "10100"
    qso2.freq = "10150"
    assert qso1.match_against(qso2) is True
    # 18MHz.
    qso1.freq = "18068"
    qso2.freq = "18168"
    assert qso1.match_against(qso2) is True
    # 24MHz.
    qso1.freq = "24890"
    qso2.freq = "24990"
    assert qso1.match_against(qso2) is True
    # Different WARC bands -> False.
    qso1.freq = "14168"
    qso2.freq = "24890"
    assert qso1.match_against(qso2) is False
    # Unrecognized junk -> False.
    # Different WARC bands -> False.
    qso1.freq = "LIGHT"
    qso2.freq = "INTERNET"
    assert qso1.match_against(qso2) is False
    # Different band, band checking disabled.
    assert qso1.match_against(qso2, check_band=False) is True
