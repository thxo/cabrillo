# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0]
### Added
- `frequency_to_band_m()` utility for meter-band conversion.
- `check_mode` flag on `parse_log_text`, `parse_log_file`, and `parse_qso` to
  accept non-standard QSO modes (e.g. `CW/Digital`) without raising.
- Extended Maidenhead grid locator support (8 and 10 character locators).
- VHF/UHF bands (50, 70, 144, 222, 432, 902 MHz) in FREQ_RANGES for
  `match_against` band matching.
- OFFTIME header now parsed into datetime list (roundtrip works).
- Test fixtures for LAQP, IARU-HF (DXLog.net vendor keys), and multi-TX logs.

### Fixed
- `claimed_score = 0` no longer silently dropped from output.
- Empty GRID-LOCATOR stored as None (not empty string) for consistent roundtrip.
- `append_qso()` usable without explicitly passing `ignore_order`.
- `QSO.__eq__` no longer crashes when compared to non-QSO objects.
- Malformed QSO dates raise `InvalidQSOException` (not raw `ValueError`).
- Exchange comparison in `match_against` is now case-insensitive.

### Changes
- Data: remove duplicate YOUTH from CATEGORY_OVERLAY; annotate deprecated
  values (123G, OVER-50) and dead data (CONTEST list, VALID_QSO_CATEGORIES).
- CI: test on Python 3.10, 3.12, 3.13, 3.14 (drop 3.9).

## [0.2.1]
### Changes
- Allow empty lines in logs.
- Handle empty claimed score value as 0. (by report in #14)
- Generally attempt to make empty values more robust.

## [0.2.0]
### Added
- Add new CATEGORY additions to the Cabrillo spec since November 2020.

### Fixed
- Replace stale Travis CI workflow badge with GitHub action's.

## [0.1.2]
### Added
- Add GRID-LOCATOR field. (#11)
- Add more examples in README.

### Fixed
- Fix setup.py authorship information.

## [0.1.1]
### Changes
- Add new Cabrillo fields. (#9)

## [0.1.0]
### Added
- Cut first documented release.

### Changes
- Fix UnicodeDecodeError when parsing non UTF-8 log files. (#6)
