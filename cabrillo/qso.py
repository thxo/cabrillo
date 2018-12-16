"""Contains classes pertaining to holding individual QSOs."""

from cabrillo import data
from cabrillo.errors import InvalidQSOException


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
    """

    def __init__(self, freq, mo, date, de_call, dx_call, de_exch=None,
                 dx_exch=None, t=None):
        """Construct a QSO object.

        Arguments:
            See class attributes for parameters.
            de_exch and dx_exch are optional lists.
        """
        if mo not in data.MODES:
            raise InvalidQSOException('{} is not a valid mode.'.format(mo))

        self.freq = freq
        self.mo = mo
        self.date = date
        self.de_call = de_call
        self.dx_call = dx_call
        self.t = t

        if not de_exch:
            self.de_exch = list()
        else:
            self.de_exch = de_exch

        if not dx_exch:
            self.dx_exch = list()
        else:
            self.dx_exch = dx_exch

    def __str__(self):
        line = '{} {} {} {} {} {} {} {}'
        time_str = self.date.strftime("%Y-%m-%d %H%M")
        if self.t is None:
            t_text = ''
        else:
            t_text = self.t

        return line.format(self.freq, self.mo,
                           time_str,
                           self.de_call,
                           ' '.join(self.de_exch).strip(),
                           self.dx_call,
                           ' '.join(self.dx_exch).strip(),
                           t_text).strip()
