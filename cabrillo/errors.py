"""Contains errors used throughout the library."""


class CabrilloParserException(Exception):
    """CabrilloParserException is the catch-all exception for this library."""


class InvalidLogException(CabrilloParserException):
    """InvalidLogException occurs if there is an error reading the log
    file.
    """


class InvalidQSOException(CabrilloParserException):
    """InvalidLogException occurs if there is an error parsing an individual
    QSO.
    """
