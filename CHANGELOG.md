# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-01

### Added
- Initial release of the calculator app
- FastAPI backend with a JSON arithmetic API at `/api/calc`
- Modern calculator UI served from the `static` folder
- Local startup script via `run.sh`
- Project documentation and GitHub issue/PR templates
- CI workflow for smoke testing
- MIT license

### Changed
- Organized project files for easier local development and GitHub publishing
- Refined the README into a formal project overview

### Fixed
- Resolved environment import issues by clarifying virtual environment setup

### Security
- Kept the app simple and dependency-based without exposing unnecessary runtime configuration

## [Unreleased]

### Planned
- Add scientific calculator functions
- Support parentheses and nested arithmetic expressions
- Add automated unit tests for more edge cases
- Add a real screenshot asset to the docs folder
- Improve UI polish and responsiveness

## Release Template

Use this structure for future release notes:

```md
## [X.Y.Z] - YYYY-MM-DD

### Added
- ...

### Changed
- ...

### Fixed
- ...

### Removed
- ...
```
