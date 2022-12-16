"""Contains classes pertaining to holding individual QSOs."""

from cabrillo import data
from cabrillo.errors import InvalidQSOException


def convert_mode(mode):
    mode_sources = [
        data.PH_MODES,
        data.CW_MODES,
        data.FM_MODES,
        data.RTTY_MODES,
        data.DG_MODES,
    ]

    for source in mode_sources:
        if mode in source:
            if source == data.PH_MODES:
                return "PH"
            elif source == data.CW_MODES:
                return "CW"
            elif source == data.FM_MODES:
                return "FM"
            elif source == data.RTTY_MODES:
                return "RY"
            elif source == data.DG_MODES:
                return "DG"

    raise ValueError(f"Could not convert '{mode}' to a Cabrillo-compatible mode!")


def frequency_to_band(freq):
    """Converts numeric frequency in kHz to band designation.

    The Cabrillo specification allows the usage of exact frequency in lieu of
    band category. For example, one may use 14313 to denote the exact
    frequency, while the other operator may log simply as 14000 to denote 20m.
    This program serves to convert numeric frequencies to their respective
    Cabrillo band designations.

    Example:
        >>> frequency_to_band('14200')
        '14000'
        >>> frequency_to_band('LIGHT')
        'LIGHT

    Arguments:
        freq (str): The frequency found in the log.

    Returns:
        str: Parsed band designation. If the given frequency is not numeric or
            not a recognized amateur band, it will be returned as-is.

    """
    try:
        freq_num = int(freq)
    except ValueError:
        return freq

    for name, range in data.FREQ_RANGES.items():
        if range[0] <= freq_num <= range[1]:
            return name

    return freq


class QSO:
    """Representation of a single QSO.

    Attributes:
        freq: Frequency in str representation.
        mo: Two letter of QSO. See MODES.
        date: UTC time in datetime.datetime object.
        de_call: Sent callsign.
        de_exch: Sent exchange incl. RST. List of each component.
        dx_call: Received callsign.
        dx_exch: Received exchange incl. RST. List of each component.
        t: Transmitter ID for multi-transmitter categories in int. 0/1.
        valid: True: Valid QSO, False: X-QSO.
    """

    def __init__(
        self,
        freq,
        mo,
        date,
        de_call,
        dx_call,
        de_exch=[],
        dx_exch=[],
        t=None,
        valid=True,
    ):
        """Construct a QSO object.

        Arguments:
            See class attributes for parameters.
            de_exch and dx_exch are optional lists.
        """
        if mo not in data.MODES:
            mo = convert_mode(mo)
            if mo is None:
                raise InvalidQSOException("{} is not a valid mode.".format(mo))

        self.freq = freq
        self.mo = mo
        self.date = date
        self.de_call = de_call
        self.de_exch = de_exch
        self.dx_call = dx_call
        self.dx_exch = dx_exch
        self.t = t
        self.valid = valid

    def match_against(self, other, max_time_delta=30, check_exch=True, check_band=True):
        """Verify if another QSO is the counterpart of this QSO from the other
        station.

        The Cabrillo format does not recognize certain less common bands (with
        WARC bands being the majority). To account for this problem, for
        frequencies that we do not recognize as a ham band, we still consider
        them to be from the same band if they differ 500kHz or less. To turn
        off band checking altogether, pass False to `check_band`.

        Arguments:
            other (cabrillo.QSO): The other QSO being verified against.
            max_time_delta (int): The maximum number of minutes that two QSOs'
                recorded times can differ and still be matched. The default is
                30 minutes. If you want to ignore checking time, use the
                value `-1`.
            check_exch (bool): If this method will compare exchanges.
                Defaults to True.
            check_band (bool): If this method will determine band match.
                Defaults to True.

        Returns:
            bool

        Raises:
            ValueError: When a negative value that is not -1 is received.
        """
        # Check time delta sanity.
        if max_time_delta != -1 and max_time_delta < 0:
            raise ValueError(
                "Time delta should nonnegative. The only "
                "exception is -1, which would turn off time "
                "checking."
            )

        # Check callsign
        if self.de_call != other.dx_call or self.dx_call != other.de_call:
            return False

        # Check mode
        if self.mo != other.mo:
            return False

        # Check time
        if max_time_delta != -1:
            delta = self.date - other.date
            if abs(delta.total_seconds()) > max_time_delta * 60:
                return False

        # Check exchange
        if check_exch:
            if self.de_exch != other.dx_exch or self.dx_exch != other.de_exch:
                return False

        # Check band
        if check_band:
            # If they're the same, they must match.
            if self.freq == other.freq:
                return True
            # If they're the same band, they match.
            if frequency_to_band(self.freq) == frequency_to_band(other.freq):
                return True
            # Account for bands not in Cabrillo, we give 500kHz latitude.
            try:
                if abs(int(self.freq) - int(other.freq)) <= 500:
                    return True
            except ValueError:
                pass
            # Give up.
            return False

        # Catchall success.
        return True

    def __str__(self):
        line = "{}: {} {} {} {} {} {} {} {}"
        time_str = self.date.strftime("%Y-%m-%d %H%M")
        if self.t is None:
            t_text = ""
        else:
            t_text = self.t

        return line.format(
            "QSO" if self.valid else "X-QSO",
            self.freq,
            self.mo,
            time_str,
            self.de_call,
            " ".join(self.de_exch).strip(),
            self.dx_call,
            " ".join(self.dx_exch).strip(),
            t_text,
        ).strip()

    def __eq__(self, other):
        """Define equal QSO."""
        return (
            self.freq == other.freq
            and self.mo == other.mo
            and self.date == other.date
            and self.de_call == other.de_call
            and self.dx_call == other.dx_call
            and self.de_exch == other.de_exch
            and self.dx_exch == other.dx_exch
        )
