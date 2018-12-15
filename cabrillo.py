# Based on the Cabrillo specification available at
# https://wwrof.org/cabrillo/cabrillo-specification-v3/
# All values below should remain upper case.
CATEGORY_ASSISTED = ['ASSISTED', 'NON-ASSISTED']
CATEGORY_BAND = ['ALL', '160M', '80M', '40M', '20M', '15M', '10M', '6M', '4M',
                 '2M', '222', '432', '902', '1.2G', '2.3G', '3.4G', '5.7G',
                 '10G', '24G', '47G', '75G', '123G', '134G', '241G', 'LIGHT',
                 'VHF-3-BAND', 'VHF-FM-ONLY']
CATEGORY_MODE = ['SSB', 'CW', 'RTTY', 'FM', 'MIXED']
CATEGORY_OPERATOR = ['SINGLE-OP', 'MULTI-OP', 'CHECKLOG']
CATEGORY_POWER = ['HIGH', 'LOW', 'QRP']
CATEGORY_STATION = ['FIXED', 'MOBILE', 'PORTABLE', 'ROVER', 'ROVER-LIMITED',
                    'ROVER-UNLIMITED', 'EXPEDITION', 'HQ', 'SCHOOL']
CATEGORY_TIME = ['6-HOURS', '12-HOURS', '24-HOURS']
CATEGORY_TRANSMITTER = ['ONE', 'TWO', 'LIMITED', 'UNLIMITED', 'SWL']
CATEGORY_OVERLAY = ['CLASSIC', 'ROOKIE', 'TB-WIRES', 'NOVICE-TECH', 'OVER-50']
MODES = ['CW', 'PH', 'FM', 'RY', 'DG']

KEYWORD_MAP = dict(version='START-OF-LOG', callsign='CALLSIGN',
                   contest='CONTEST', category_assisted='CATEGORY-ASSISTED',
                   category_band='CATEGORY-BAND',
                   category_mode='CATEGORY-MODE',
                   category_operator='CATEGORY-OPERATOR',
                   category_power='CATEGORY-POWER',
                   category_station='CATEGORY-STATION',
                   category_time='CATEGORY-TIME',
                   category_transmitter='CATEGORY-TRANSMITTER',
                   category_overlay='CATEGORY-OVERLAY',
                   certificate='CERTIFICATE', claimed_score='CLAIMED-SCORE',
                   club='CLUB', created_by='CREATED_BY', email='EMAIL',
                   location='LOCATION', name='NAME', address='ADDRESS',
                   address_city='ADDRESS_CITY',
                   address_state_province='ADDRESS_STATE_PROVINCE',
                   address_postalcode='ADDRESS_POSTALCODE',
                   address_country='ADDRESS_COUNTRY', operators='OPERATORS',
                   offtime='OFFTIME', soapbox='SOAPBOX', qso='QSO',
                   x_qso='X-QSO')
VALID_CATEGORIES_MAP = dict(category_assisted=CATEGORY_ASSISTED,
                            category_band=CATEGORY_BAND,
                            category_mode=CATEGORY_MODE,
                            category_operator=CATEGORY_OPERATOR,
                            category_power=CATEGORY_POWER,
                            category_station=CATEGORY_STATION,
                            category_time=CATEGORY_TIME,
                            category_transmitter=CATEGORY_TRANSMITTER,
                            category_overlay=CATEGORY_OVERLAY)


class CabrilloParserException(Exception):
    pass


class InvalidLogException(CabrilloParserException):
    pass


class InvalidQSOException(CabrilloParserException):
    pass


class Cabrillo:
    """Representation of a Cabrillo log file.

    Attributes:
          version: The only supported version is '3.0'.
          callsign: Call sign of station. Required.
          contest: Contest identification.
          category_assisted: One of CATEGORY_ASSISTED.
          category_band: One of CATEGORY_BAND.
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
                 category_operator=None, category_power=None,
                 category_station=None, category_time=None,
                 category_transmitter=None, category_overlay=None,
                 certificate=None, claimed_score=None, club=None,
                 created_by="cabrillo (Python)", email=None, location=None,
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
        if check_categories:
            for key, value in VALID_CATEGORIES_MAP.items():
                attribute = getattr(self, key)
                if attribute and attribute not in value:
                    raise InvalidLogException("Got {} for {} but expecting "
                                              "one of {}.".format(attribute,
                                                                 key, value))

        self.callsign = callsign
        self.version = version
        self.contest = contest
        self.category_assisted = category_assisted
        self.category_band = category_band
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


class QSO:
    """Representation of a single QSO.

    Attributes:
        freq: Frequency in str representation.
        mo: Two letter of QSO. See MODES.
        date: UTC date in yyyy-mm-dd.
        de_call: Sent callsign.
        de_rst: Sent RST.
        de_exch: Sent exchange. List of each component.
        dx_call: Received callsign.
        dx_rst: Received RST.
        dx_exch: Received exchange. List of each component.
    """

    def __init__(self, freq, mo, date, de_call, de_rst, dx_call,
                 dx_rst, dx_exch=None, de_exch=None):
        """Construct a QSO object.

        Arguments:
            See class attributes for parameters.
            de_exch and dx_exch are optional lists.
        """
        if mo not in MODES:
            raise InvalidQSOException("{} is not a valid mode.".format(mo))

        self.freq = freq
        self.mo = mo
        self.date = date
        self.de_call = de_call
        self.de_rst = de_rst
        self.dx_call = dx_call
        self.dx_rst = dx_rst
        self.de_exch = de_exch
        self.dx_exch = dx_exch
