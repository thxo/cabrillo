"""Test the parsing of individual QSO lines."""
from datetime import datetime

import pytest
import path_helper

from cabrillo.errors import InvalidQSOException
from cabrillo.parser import parse_qso


def test_cqwpx_single():
    """Test a CQ WPX QSO in the SINGLE transmitter category."""
    qso = parse_qso('7005 CW 2009-05-30 0002 AA1ZZZ 599 1 S50A 599 4', True)
    assert qso.freq == '7005'
    assert qso.mo == 'CW'
    assert qso.date == datetime.strptime('200905300002', '%Y%m%d%H%M')
    assert qso.de_call == 'AA1ZZZ'
    assert qso.de_exch == ['599', '1']
    assert qso.dx_call == 'S50A'
    assert qso.dx_exch == ['599', '4']
    assert qso.t is None
    assert qso.valid


def test_cqwpx_two():
    """Test a CQ WPX QSO in the TWO transmitter category with transmitter
    ID designation in each QSO.
    """
    line = '3799 PH 1999-03-06 0711 HC8N          ' \
           '59  001    W1AW 59  001    0'
    qso = parse_qso(line, False)
    assert qso.freq == '3799'
    assert qso.mo == 'PH'
    assert qso.date == datetime.strptime('199903060711', '%Y%m%d%H%M')
    assert qso.de_call == 'HC8N'
    assert qso.de_exch == ['59', '001']
    assert qso.dx_call == 'W1AW'
    assert qso.dx_exch == ['59', '001']
    assert qso.t == 0
    assert not qso.valid


def test_cqwpx_malformed():
    """Test a CQ WPX QSO in the SINGLE category with malformed exchange."""
    # Uneven exchange.
    with pytest.raises(InvalidQSOException) as _:
        parse_qso('7005 CW 2009-05-30 0002 AA1ZZZ 599 CT 001 S50A 599 004', True)

    # Invalid transmitter ID when uneven.
    with pytest.raises(InvalidQSOException) as _:
        parse_qso('7005 CW 2009-05-30 0002 AA1ZZZ 599 CT 001 S50A 599 3', False)


def test_no_exchange():
    """Test a hypothetical contest with no exchange."""
    assert parse_qso('7005 CW 2009-05-30 0002 AA1ZZZ 599 S50A 599', True)

    # Test transmitter ID.
    qso = parse_qso('7005 CW 2009-05-30 0002 AA1ZZZ 599 S50A 599 1', False)
    assert qso.t == 1


def test_invalid_qso():
    """Test a QSO line that is far too short."""
    with pytest.raises(InvalidQSOException) as _:
        parse_qso('7005 CW 2009-05-30 1230 S50A', True)


def test_invalid_date_raises_qso_exception():
    with pytest.raises(InvalidQSOException) as exc_info:
        parse_qso('14000 CW 2020-13-45 9999 W1AW 599 1 VA2RAC 599 4', True)
    assert 'date' in str(exc_info.value).lower() or 'time' in str(exc_info.value).lower()


def test_yarc_qso():
    """Test the YARC QSO Party which has multiple exchanges."""
    line = '14000 PH 2018-12-01 1640 W4Y  16 VA     W2Y        19 NY'
    qso = parse_qso(line, True)
    assert qso.freq == '14000'
    assert qso.mo == 'PH'
    assert qso.date == datetime.strptime('201812011640', '%Y%m%d%H%M')
    assert qso.de_call == 'W4Y'
    assert qso.de_exch == ['16', 'VA']
    assert qso.dx_call == 'W2Y'
    assert qso.dx_exch == ['19', 'NY']
    assert qso.t is None


def test_nonstandard_mode_strict():
    with pytest.raises(InvalidQSOException):
        parse_qso('14000 CW/DIGITAL 2020-01-01 0000 W1AW 599 1 K3LR 599 4', True)


def test_nonstandard_mode_lenient():
    qso = parse_qso('14000 CW/DIGITAL 2020-01-01 0000 W1AW 599 1 K3LR 599 4',
                    True, check_mode=False)
    assert qso.mo == 'CW/DIGITAL'
    assert qso.freq == '14000'
    assert qso.de_call == 'W1AW'
