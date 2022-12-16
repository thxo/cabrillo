import pytest

from cabrillo import qso


class TestModeConvert:
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("SSB", "PH"),
            ("AM", "PH"),
            ("FT8", "DG"),
            ("USB", "PH"),
            ("FM", "FM"),
            ("RTTY", "RY"),
            ("CW", "CW"),
            ("PSK31", "DG"),
        ],
    )
    def test_modes(self, test_input, expected):
        converted_mode = qso.convert_mode(test_input)
        assert converted_mode == expected
