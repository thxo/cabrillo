"""Contains utilities to parse a Cabrillo file."""
from datetime import datetime
from cabrillo import QSO, Cabrillo

from cabrillo.errors import InvalidQSOException, InvalidLogException
from cabrillo import data

import collections
import re


def parse_qso(text, valid):
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
        raise InvalidQSOException(
            "QSO components too little. Expects at "
            "least 6, got {}".format(len(components))
        )

    # Calculate the number of information exchanged.
    num_exchanged = len(components) - 4
    # Handle case where transmitter ID presents for TWO transmitter logs.
    transmitter = None
    if num_exchanged % 2 == 1:
        if components[-1] not in ["0", "1"]:
            raise InvalidQSOException(
                "{} RST/exchanges presented, which is " "uneven.".format(num_exchanged)
            )
        else:
            num_exchanged -= 1
            transmitter = int(components[-1])

    # Build QSO
    date = datetime.strptime(
        "{} {}".format(components[2], components[3]), "%Y-%m-%d %H%M"
    )
    return QSO(
        freq=components[0],
        mo=components[1],
        date=date,
        de_call=components[4],
        de_exch=components[5 : int(3 + num_exchanged / 2 + 1)],
        dx_call=components[int(3 + num_exchanged / 2 + 1)],
        dx_exch=components[int(3 + num_exchanged / 2 + 2) : int(3 + num_exchanged + 1)],
        t=transmitter,
        valid=valid,
    )


def parse_log_text(
    text, ignore_unknown_key=False, check_categories=True, ignore_order=False
):
    """Parse a Cabrillo log in text form.

    Attributes in cabrillo.data.KEYWORD_MAP will be parsed accordingly. X-
    attributes will be sorted into the x_anything attribute of the Cabrillo
    object.

    Arguments:
        text: str of log
        check_categories: Check if categories, if given, exist in the
            Cabrillo specification.
        ignore_unknown_key: Boolean denoting whether if unknown and non X-
            attributes should be ignored if found in long. Otherwise,
            an InvalidLogException will be raised. Defaults to False
            (which enforces valid keywords).

    Returns:
        cabrillo.Cabrillo

    Raises:
        InvalidQSOException, InvalidLogException
    """
    inverse_keywords = {v: k for k, v in data.KEYWORD_MAP.items()}
    results = dict()
    results["x_anything"] = collections.OrderedDict()

    key_colon_value = re.compile(r"^\s*([^:]+?)\s*:\s*(.*?)\s*$")
    for line in text.split("\n"):
        match = key_colon_value.fullmatch(line)
        if match:
            key, value = match.group(1), match.group(2)
        else:
            raise InvalidLogException(
                f"Line does not start with a colon-delimited (:) key, got '{line}'"
            )

        if key == "END-OF-LOG":
            break
        elif key == "CLAIMED-SCORE":
            try:
                results[inverse_keywords[key]] = int(value)
            except ValueError:
                raise InvalidLogException(
                    "Improperly formatted claimed "
                    'score "{}". Per specification the'
                    " score, if given, must be an "
                    "integer without any formatting, "
                    'like "12345678".'.format(value)
                )
        elif key == "CERTIFICATE":
            results[inverse_keywords[key]] = value == "YES"
        elif key in ["QSO", "X-QSO"]:
            # Do not split QSO and X-QSO case here.
            # By not splitting, we keep timewise order for QSOs that have the same timestamp.
            results.setdefault("qso", []).append(parse_qso(value, key == "QSO"))
        elif key == "OPERATORS":
            results.setdefault(inverse_keywords[key], list()).extend(
                value.replace(",", " ").split()
            )
        elif key in ["ADDRESS", "SOAPBOX"]:
            results.setdefault(inverse_keywords[key], list()).append(value)
        elif key in inverse_keywords.keys():
            results[inverse_keywords[key]] = value
        elif key.startswith("X-"):
            # We keep the order that we were given.
            results["x_anything"][key] = value
        elif not ignore_unknown_key:
            raise InvalidLogException("Unknown key {} read.".format(key))

    return Cabrillo(
        check_categories=check_categories, ignore_order=ignore_order, **results
    )


def parse_log_file(
    filename, ignore_unknown_key=False, check_categories=True, ignore_order=False
):
    """Parse a Cabrillo log file.

    Attributes in cabrillo.data.KEYWORD_MAP will be parsed accordingly. X-
    attributes will be sorted into the x_anything attribute of the Cabrillo
    object.

    Arguments:
        filename: filename of the target log file.
        check_categories: Check if categories, if given, exist in the
            Cabrillo specification.
        ignore_unknown_key: Boolean denoting whether if unknown and non X-
            attributes should be ignored if found in long. Defaults to False.
        ignore_order: Cabrillo logs need to be ordered time-wise.
            Whether to ignore violations on input and disable output.

    Returns:
        cabrillo.Cabrillo

    Raises:
        InvalidQSOException, InvalidLogException
    """
    with open(filename, "r", encoding="unicode_escape") as f:
        return parse_log_text(
            f.read(), ignore_unknown_key, check_categories, ignore_order
        )
