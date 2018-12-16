"""Test the Cabrillo class."""

from datetime import datetime
from os import linesep

import pytest

from cabrillo import Cabrillo, QSO
from cabrillo.data import VALID_CATEGORIES_MAP
from cabrillo.errors import InvalidLogException


def test_all_attributes():
    """Test the functionality of the Cabrillo class when all arguments are
    set."""
    # Modified from https://www.cqwpx.com/cabrillo.htm
    offtime = [datetime.strptime('May 30 2009 12:03AM', '%b %d %Y %I:%M%p'),
               datetime.strptime('May 30 2009 12:05AM', '%b %d %Y %I:%M%p')]
    qso = [QSO('7005', 'CW',
               datetime.strptime('May 30 2009 12:02AM', '%b %d %Y %I:%M%p'),
               'AA1ZZZ', '599', 'S50A', '599', de_exch=['1'], dx_exch=['4'],
               t=None),
           QSO('7006', 'CW',
               datetime.strptime('May 30 2009 12:15AM', '%b %d %Y %I:%M%p'),
               'AA1ZZZ', '599', 'EF8M', '599', de_exch=['2'], dx_exch=['34'],
               t=None)
           ]
    cab = Cabrillo(callsign='AA1ZZZ', contest='CQ-WPX-CW',
                   category_operator='SINGLE-OP',
                   category_assisted='NON-ASSISTED', category_band='ALL',
                   category_power='HIGH', category_mode='CW',
                   category_transmitter='ONE', category_overlay='TB-WIRES',
                   category_station='FIXED', category_time='24-HOURS',
                   certificate=True, email='test@test.arpa', offtime=offtime,
                   claimed_score=24, club='Yankee Clipper Contest Club',
                   location='WMA', created_by='WriteLog V10.72C',
                   name='Randy Thompson', address=['11 Hollis Street'],
                   address_city='Uxbridge', address_state_province='MA',
                   address_postalcode='01569', address_country='USA',
                   operators=['K5ZD', 'KX0XXX'], qso=qso, x_qso=qso,
                   soapbox=['Put your comments here.',
                            'Use multiple lines if needed.'])

    # Test constructor.
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
    assert cab.category_station == 'FIXED'
    assert cab.category_time == '24-HOURS'
    assert cab.certificate is True
    assert cab.email == 'test@test.arpa'
    assert cab.offtime == offtime
    assert cab.claimed_score == 24
    assert cab.club == 'Yankee Clipper Contest Club'
    assert cab.location == 'WMA'
    assert cab.created_by == 'WriteLog V10.72C'
    assert cab.address == ['11 Hollis Street']
    assert cab.address_city == 'Uxbridge'
    assert cab.address_state_province == 'MA'
    assert cab.address_postalcode == '01569'
    assert cab.address_country == 'USA'
    assert cab.operators == ['K5ZD', 'KX0XXX']
    assert cab.qso == qso
    assert cab.x_qso == qso
    assert cab.soapbox == ['Put your comments here.',
                           'Use multiple lines if needed.']

    # Writing test.
    correct = ['START-OF-LOG: 3.0', 'CALLSIGN: AA1ZZZ', 'CONTEST: CQ-WPX-CW',
               'CATEGORY-OPERATOR: SINGLE-OP',
               'CATEGORY-ASSISTED: NON-ASSISTED', 'CATEGORY-BAND: ALL',
               'CATEGORY-POWER: HIGH', 'CATEGORY-MODE: CW',
               'CATEGORY-TRANSMITTER: ONE', 'CATEGORY-OVERLAY: TB-WIRES',
               'CATEGORY-STATION: FIXED', 'CATEGORY-TIME: 24-HOURS',
               'CERTIFICATE: YES', 'EMAIL: test@test.arpa',
               'OFFTIME: 2009-05-30 0003 2009-05-30 0005',
               'CLAIMED-SCORE: 24', 'CLUB: Yankee Clipper Contest Club',
               'LOCATION: WMA', 'CREATED-BY: WriteLog V10.72C',
               'NAME: Randy Thompson', 'ADDRESS: 11 Hollis Street',
               'ADDRESS-CITY: Uxbridge', 'ADDRESS-STATE-PROVINCE: MA',
               'ADDRESS-POSTALCODE: 01569', 'ADDRESS-COUNTRY: USA',
               'OPERATORS: K5ZD KX0XXX', 'SOAPBOX: Put your comments here.',
               'SOAPBOX: Use multiple lines if needed.',
               'QSO: 7005 CW 2009-05-30 0002 AA1ZZZ 599 1 S50A 599 4',
               'QSO: 7006 CW 2009-05-30 0015 AA1ZZZ 599 2 EF8M 599 34',
               'X-QSO: 7005 CW 2009-05-30 0002 AA1ZZZ 599 1 S50A 599 4',
               'X-QSO: 7006 CW 2009-05-30 0015 AA1ZZZ 599 2 EF8M 599 34',
               'END-OF-LOG:']
    lines = cab.write_text().split(linesep)
    assert len(correct) == len(lines) and sorted(correct) == sorted(lines)


def test_unicode():
    """Test the functionality of the Cabrillo class when there is Unicode text.
    """
    cab = Cabrillo('VR2TEST',
                   address=['毛澤大道東89號', '鶴咀'], address_city='石澳')
    lines = cab.write_text().split(linesep)
    correct = ['START-OF-LOG: 3.0', 'CALLSIGN: VR2TEST',
               'ADDRESS: 毛澤大道東89號', 'ADDRESS: 鶴咀', 'ADDRESS-CITY: 石澳',
               'CREATED-BY: cabrillo (Python)', 'END-OF-LOG:']
    assert len(correct) == len(lines) and sorted(correct) == sorted(lines)


def test_yes_no():
    """Test the conversion from boolean to YES/NO."""
    assert 'CERTIFICATE: YES' in Cabrillo('TEST100TEST',
                                          certificate=True).write_text()
    assert 'CERTIFICATE: NO' in Cabrillo('TEST100TEST',
                                          certificate=False).write_text()


def test_exceptions():
    """Test exceptions thrown in Cabrillo."""
    # If we do not enable checking, it should construct properly.
    assert Cabrillo('TEST100TEST', category_power='ITALIAN-QRP',
                    check_categories=False)

    for category in VALID_CATEGORIES_MAP.keys():
        with pytest.raises(InvalidLogException) as _:
            Cabrillo('TEST100TEST', **{category: 'ABSOLUTE-JUNK-DATA'})
