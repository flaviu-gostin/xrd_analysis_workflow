# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

- No item here yet

## [2.1.1] - 2022-04-07

### Fixed

- Path to PONI file not being created (due to incorrect syntax in Makefile)

## [2.1.0] - 2022-03-29

### Added

- Add Figure S2.
- Add this changelog file.

### Changed

- Add annotations to and adjust margins in Fig S1.
- Adjust gray levels in Fig S1 to improve visibility of diffraction
  rings and spots.
- Makefile: use Python module `venv` instead of with virtualenv utility.
- Recommend creating virtual environment with `python3` instead of
  `virtualenv`.
- Recommend calling `pip` as Python module.

### Fixed

- Unpacking error in check_calibration.py
- Use correct slice number for Figure S1.
- Figure S1 coming out as negative.
- Archives not being automatically extracted after download.
- Failing build on Travis CI and on local machine.

### Removed

- Support (and Travis CI testing) for Python3.6 and 3.7.

## [2.0.0] - 2020-11-21

### Added

- Automatic download of raw data from data repository on Zenodo.
