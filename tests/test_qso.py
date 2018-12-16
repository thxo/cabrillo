"""Test the QSO class."""
from datetime import datetime

import pytest

from cabrillo import QSO
from cabrillo.errors import InvalidQSOException


def test_yarc():
    """Test the QSO class with YARC QSO Party exchanges."""
    qso = QSO('14313', 'PH',
              datetime.strptime('May 30 2018 10:10PM', '%b %d %Y %I:%M%p'),
              'KX0XXX', 'KX9XXX',
              de_exch=['59', '10', 'CO'], dx_exch=['44', '20', 'IN'], t=None)
    assert qso.freq == '14313'
    assert qso.mo == 'PH'
    assert qso.date == datetime.strptime('May 30 2018 10:10PM',
                                         '%b %d %Y %I:%M%p')
    assert qso.de_call == 'KX0XXX'
    assert qso.dx_call == 'KX9XXX'
    assert qso.de_exch == ['59', '10', 'CO']
    assert qso.dx_exch == ['44', '20', 'IN']
    assert qso.t is None
    assert str(qso) == '14313 PH 2018-05-30 2210 KX0XXX 59 10 CO KX9XXX 44 ' \
                       '20 IN'


def test_with_xmtr():
    """Test the QSO class with a transmitter designation."""
    qso = QSO('241G', 'PH',
              datetime.strptime('May 30 2018 10:10PM', '%b %d %Y %I:%M%p'),
              'KX0XXX', 'KX9XXX',
              de_exch=['59', 'CO'], dx_exch=['44', 'IL'], t=1)
    assert qso.freq == '241G'
    assert qso.mo == 'PH'
    assert qso.date == datetime.strptime('May 30 2018 10:10PM',
                                         '%b %d %Y %I:%M%p')
    assert qso.de_call == 'KX0XXX'
    assert qso.dx_call == 'KX9XXX'
    assert qso.de_exch == ['59', 'CO']
    assert qso.dx_exch == ['44', 'IL']
    assert qso.t == 1
    assert str(qso) == '241G PH 2018-05-30 2210 KX0XXX 59 CO KX9XXX 44 ' \
                       'IL 1'


def test_invalid_mode():
    """Test the QSO class with invalid modes."""
    with pytest.raises(InvalidQSOException) as _:
        QSO(freq='LIGHT', mo='MCW', date=datetime.now(), de_call='KX0XXX',
            dx_call='KX9XXX')


def test_automatic_list():
    """Test automatic creation of lists for exchanges."""
    qso = QSO(freq='LIGHT', mo='CW', date=datetime.now(), de_call='KX0XXX',
              dx_call='KX9XXX')
    assert qso.de_exch == []
    assert qso.dx_exch == []
