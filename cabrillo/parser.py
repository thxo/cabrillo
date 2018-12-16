"""Contains utilities to parse a Cabrillo file."""
from datetime import datetime

from cabrillo import QSO
from cabrillo.errors import InvalidQSOException


def parse_qso(text):
    """Parse a single line of QSO into a QSO object.

    Arguments:
        text: str of QSO from log file (excluding the 'QSO: ' preamble)

    Returns:
        cabrillo.QSO

    Raises:
        InvalidQSOException
    """
    components = text.split()

    # Requires freq, mo, date, time, 2x calls.
    if len(components) < 8:
        raise InvalidQSOException('QSO components too little. Expects at '
                                  'least 6, got {}'.format(len(components)))

    # Calculate the number of information exchanged.
    num_exchanged = len(components) - 4
    # Handle case where transmitter ID presents for TWO transmitter logs.
    transmitter = None
    if num_exchanged % 2 == 1:
        if components[-1] not in ['0', '1']:
            raise InvalidQSOException("{} RST/exchanges presented, which is "
                                      "uneven.".format(num_exchanged))
        else:
            num_exchanged -= 1
            transmitter = int(components[-1])

    # Build QSO
    date = datetime.strptime('{} {}'.format(components[2], components[3]),
                             '%Y-%m-%d %H%M')
    return QSO(freq=components[0], mo=components[1], date=date,
               de_call=components[4],
               de_exch=components[5:int(3 + num_exchanged / 2 + 1)],
               dx_call=components[int(3 + num_exchanged / 2 + 1)],
               dx_exch=components[int(3 + num_exchanged / 2 + 2):
                                  int(3 + num_exchanged + 1)], t=transmitter)
