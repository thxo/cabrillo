"""Contains code pertaining to parsing and holding individual Cabrillo data.
"""
# pylint: disable=E1101, E0203

import collections
import io

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
          claimed_score: Claimed score as int.
          club: Club represented.
          created_by: Software responsible for creating this log file.
            Optional, defaults to "cabrillo (Python)".
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
          soapbox: List of lines of soapbox text.
          qso: List of all QSOs, including ignored QSOs.
          valid_qso: List of all valid QSOs (excluding ignored X-QSO) (read-only).
          x_qso: List of all invalid QSOs (X-QSO only) (read-only).
          x_anything: An ordered mapping of ignored/unknown attributes.
    """

    def __init__(self, check_categories=True, ignore_order=False, **d):
        """Construct a Cabrillo object.

        Use named arguments only.

        Attributes:
            check_categories: Check if categories, if given, exist in the
            Cabrillo specification.
            See class attributes for other parameters.

        Raises:
            InvalidLogException
        """
        d.setdefault("created_by", "cabrillo (Python)")
        for key in data.OUTPUT_KEYWORD_MAP:
            setattr(self, key, d.get(key, None))

        self.x_anything = d.get("x_anything", collections.OrderedDict())

        version = d.get("version", "3.0")
        if version != "3.0":
            raise InvalidLogException(
                "Only Cabrillo v3 supported, " "got {}".format(version)
            )
        else:
            self.version = version

        self.qso = []
        for qso in d.get("qso", []):
            self.append_qso(qso, ignore_order)

        self.ignore_order = ignore_order

        if check_categories:
            for attribute, candidates in data.VALID_CATEGORIES_MAP.items():
                value = getattr(self, attribute, None)
                if value and value not in candidates:
                    raise InvalidLogException(
                        "Got {} for {} but expecting one of {}.".format(
                            value, attribute, candidates
                        )
                    )

    valid_qso = property(fget=lambda self: [qso for qso in self.qso if qso.valid])
    x_qso = property(fget=lambda self: [qso for qso in self.qso if not qso.valid])

    def append_qso(self, qso, ignore_order):
        """Add one QSO to the end of this log."""
        if 0 < len(self.qso) and qso.date < self.qso[-1].date and not ignore_order:
            # The Cabrillo spec says QSOs need to be ordered by time.
            # The timestamps from Cabrillo's point of view
            # give time only to minute precision, and
            # QSO rates above 60 / hour are by no means uncommon.
            # So we refrain from ordering QSOs by timestamps ourselves.
            raise InvalidLogException("QSOs need to be ordered time-wise.")

        self.qso.append(qso)

    def text(self):
        """Generate the Cabrillo log text.

        Arguments:
            None.

        Returns:
            str: Cabrillo log file text. `_` in Attribute
              names are automatically replaced to `-` upon text output.

        Raises:
            InvalidLogException when target Cabrillo version is not 3.0
            or ignore_ordered mode is active.
        """
        with io.StringIO() as out:
            self.write(out)
            return out.getvalue()

    def write(self, file):
        """writes a Cabrillo log text to the text-file-like object file.

        Arguments:
            file: Anything that has a write() - method accepting a string.
                  Cabrillo log file text is written here. `_` in attribute
                  names are automatically replaced by `-`.

        Raises:
            InvalidLogException when target Cabrillo version is not 3.0
            or ignore_ordered mode is active.
        """
        if self.version != "3.0":
            raise InvalidLogException("Only Cabrillo v3 supported.")

        if self.ignore_order:
            raise InvalidLogException(
                "Refuse produce output in ignore_ordered mode as Cabrillo logs need to be ordered time-wise."
            )

        print("START-OF-LOG: {}".format(self.version), file=file)

        # Output known attributes.
        for attribute, keyword in data.OUTPUT_KEYWORD_MAP.items():
            value = getattr(self, attribute, None)
            if value is not None:
                if attribute == "certificate":
                    # Convert boolean to YES/NO.
                    print("{}: {}".format(keyword, "YES" if value else "NO"), file=file)
                elif attribute in ["address", "soapbox"]:
                    # Process multi-line attributes.
                    for x in value:
                        print("{}: {}".format(keyword, x), file=file)
                elif attribute == "operators":
                    # Process attributes delimited by space.
                    print("{}: {}".format(keyword, " ".join(value)), file=file)
                elif attribute == "offtime":
                    # Process offtime dates.
                    print(
                        "{}: {}".format(
                            keyword,
                            " ".join([x.strftime("%Y-%m-%d %H%M") for x in value]),
                        ),
                        file=file,
                    )
                elif value and attribute != "version":
                    print("{}: {}".format(keyword, value), file=file)

        # Output ignored attributes.
        for attribute, keyword in self.x_anything.items():
            print("{}: {}".format(attribute.replace("_", "-"), keyword), file=file)

        # Output QSOs:
        for qso in self.qso:
            print(qso, file=file)

        print("END-OF-LOG:", file=file)

    def __str__(self):
        return "<Cabrillo for {}>".format(self.callsign)
