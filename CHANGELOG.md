# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
