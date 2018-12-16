"""Contains code pertaining to parsing and holding individual Cabrillo data.
"""
# pylint: disable=E1101, E0203
from cabrillo import data
from cabrillo.errors import InvalidLogException


class Cabrillo:
    """Representation of a Cabrillo log file.

    Attributes:
          version: The only supported version is '3.0'.
          callsign: Call sign of station.
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
          x_anything: A dict of ignored/unknown attributes.

    """

    def __init__(self, check_categories=True, **d):
        """Construct a Cabrillo object.

        Use named arguments only.

        Attributes:
            check_categories: Check if categories, if given, exist in the
            Cabrillo specification.
            See class attributes for other parameters.

        Raises:
            InvalidLogException
        """
        d.setdefault('version', '3.0')
        d.setdefault('created_by', 'cabrillo (Python)')
        for key in data.KEYWORD_MAP:
            setattr(self, key, d.setdefault(key, None))

        self.x_anything = d.setdefault('x_anything', dict())

        if self.version != '3.0':
            raise InvalidLogException("Only Cabrillo v3 supported, "
                                      "got {}".format(self.version))

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
            str: Cabrillo log file text. `_` in Attribute
              names are automatically replaced to `-` upon text output.

        Raises:
            InvalidLogException when target Cabrillo version is not 3.0.
        """
        if self.version != '3.0':
            raise InvalidLogException("Only Cabrillo v3 supported.")

        lines = list()
        lines.append('START-OF-LOG: {}'.format(self.version))

        # Output known attributes.
        for attribute, keyword in data.KEYWORD_MAP.items():
            value = getattr(self, attribute, None)
            if value is not None:
                if attribute == 'certificate':
                    # Convert boolean to YES/NO.
                    if value:
                        lines.append('{}: YES'.format(keyword))
                    else:
                        lines.append('{}: NO'.format(keyword))
                elif attribute in ['address', 'soapbox', 'qso', 'x_qso']:
                    # Process multi-line attributes.
                    output_lines = ['{}: {}'.format(keyword, str(x)) for x in
                                    value]
                    lines += output_lines
                elif attribute == 'operators':
                    # Process attributes delimited by space.
                    lines.append('{}: {}'.format(keyword, ' '.join(value)))
                elif attribute == 'offtime':
                    # Process offtime dates.
                    lines.append('{}: {}'.format(keyword, ' '.join(
                        [x.strftime("%Y-%m-%d %H%M") for x in value])))
                elif value and attribute != 'version':
                    lines.append('{}: {}'.format(keyword, value))

        # Output ignored attributes.
        for attribute, keyword in self.x_anything.items():
            lines.append('{}: {}'.format(attribute.replace('_', '-'), keyword))

        lines.append('END-OF-LOG:')

        return '\n'.join(lines)

    def __str__(self):
        return '<Cabrillo for {}>'.format(self.callsign)
