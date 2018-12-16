#!/usr/bin/env python3
"""Contains code pertaining to parsing and holding individual Cabrillo data.
"""
import os

from cabrillo import data
from cabrillo.errors import InvalidLogException


class Cabrillo:
    """Representation of a Cabrillo log file.

    Attributes:
          version: The only supported version is '3.0'.
          callsign: Call sign of station. Required.
          contest: Contest identification.
          category_assisted: One of CATEGORY_ASSISTED.
          category_band: One of CATEGORY_BAND.
          category_mode: One of CATEGORY_MODE.
          category_operator: One of CATEGORY_OPERATOR.
          category_power: One of CATEGORY-POWER.
          category_station: One of CATEGORY-STATION.
          category_time: One of CATEGORY-TIME.
          category_transmitter: One of CATEGORY-TRANSMITTER. Optional for
          multi-op.
          category_overlay: One of CATEGORY-OVERLAY.
          certificate: If certificate by post. Boolean.
          claimed_score: Claimed score in int.
          club: Club represented.
          created_by: Software responsible for creating this log file.
          Optional and defaults to "cabrillo (Python)".
          email: Email address of the submitter.
          location: State/section/ID depending on contest.
          name: Name.
          address: Mailing address in list, each entry is each line.
          address_city: Optional granular address info.
          address_state_province: Optional granular address info.
          address_postalcode: Optional granular address info.
          address_country: Optional granular address info.
          operators: List containing each operator's callsign of the station.
          offtime: List containing two datetime objects denoting start and
          end of off-time.
          soapbox: List containing each line of soapbox text at their own entry.
          qso: QSO data containing QSO objects.
          x_qso: Ignored QSO data containing QSO objects.
          x_anything: A dictionary of intentionally ignored attributes.
    """

    def __init__(self, callsign, version='3.0', contest=None,
                 category_assisted=None, category_band=None,
                 category_mode=None, category_operator=None,
                 category_power=None, category_station=None,
                 category_time=None, category_transmitter=None,
                 category_overlay=None, certificate=None,
                 claimed_score=None, club=None,
                 created_by='cabrillo (Python)', email=None, location=None,
                 name=None, address=None, address_city=None,
                 address_state_province=None, address_postalcode=None,
                 operators=None, offtime=None, soapbox=None, qso=None,
                 x_qso=None, x_anything=None, check_categories=True):
        """Construct a Cabrillo object.

        Please in no way rely on the order of the fields. Use named
        parameters only.

        Attributes:
            callsign: Callsign of station submitting the log. This is the
            only required field.
            check_categories: Check if categories given are in the Cabrillo
            specification.
            See class attributes for other parameters.

        Raises:
            InvalidLogException
        """
        self.callsign = callsign
        self.version = version
        self.contest = contest
        self.category_assisted = category_assisted
        self.category_band = category_band
        self.category_mode = category_mode
        self.category_operator = category_operator
        self.category_power = category_power
        self.category_station = category_station
        self.category_time = category_time
        self.category_overlay = category_overlay
        self.category_transmitter = category_transmitter
        self.certificate = certificate
        self.claimed_score = claimed_score
        self.club = club
        self.created_by = created_by
        self.email = email
        self.location = location
        self.name = name
        self.address = address
        self.address_city = address_city
        self.address_state_province = address_state_province
        self.address_postalcode = address_postalcode
        self.operators = operators
        self.offtime = offtime
        self.soapbox = soapbox
        self.qso = qso
        self.x_qso = x_qso
        self.x_anything = x_anything

        if not self.qso:
            self.qso = list()

        if not self.x_qso:
            self.x_qso = list()

        if check_categories:
            for attribute, candidates in data.VALID_CATEGORIES_MAP.items():
                value = getattr(self, attribute, None)
                if value and value not in candidates:
                    raise InvalidLogException(
                        'Got {} for {} but expecting one of {}.'.format(
                            value,
                            attribute, candidates))

    def write_text(self):
        """write_text generates a Cabrillo log text.

        Arguments:
            None.

        Returns:
            str
        """
        assert self.version == '3.0'

        lines = list()
        lines.append('START-OF-LOG: {}'.format(self.version))

        for attribute, keyword in data.KEYWORD_MAP.items():
            value = getattr(self, attribute, None)
            if attribute == 'certificate' and value is not None:
                # Convert boolean to YES/NO.
                if value:
                    lines.append('{}: YES'.format(keyword))
                else:
                    lines.append('{}: NO'.format(keyword))
            elif attribute in ['address', 'soapbox', 'qso', 'x_qso'] and value:
                # Process multi-line attributes.
                output_lines = ['{}: {}'.format(keyword, str(x)) for x in
                                value]
                lines += output_lines
            elif attribute in ['operators', 'offtime'] and value:

                # Process attributes delimited by space.
                lines += ['{}: {}'.format(keyword, ' '.join(value))]
            elif value and attribute != 'version':
                lines.append('{}: {}'.format(keyword, value))

        lines.append('END-OF-LOG:')

        return os.linesep.join(lines)

    def __str__(self):
        return '<Cabrillo for {}>'.format(self.callsign)


