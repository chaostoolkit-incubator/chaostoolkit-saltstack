# Changelog

## [0.1.1][]

### Changed

- Bugfix: kill process now passes correct parameter
- Refactory: abstract core workflow into one common function to reduce duplicates

### Added

- Network experiments now accepts device name to adapt different os
- Add experiment action of kill processes by name
- Add experiment action of kill process by PID
- Add experiment probe to check process PID by name

### Changed

- Refactory: abstract core workflow into one common function to reduce duplicates

### Added

- Add experiment action of kill processes by name
- Add experiment action of kill process by PID
- Add experiment probe to check process PID by name

## [0.1.0][]

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-saltstack/tree/0.1.0

### Added

-   Initial release, experiments are only validated on Linux! Not Windows yet!
-   Add probe that check if a Salt Minion is online
-   Add probe that check if a Salt Minion is installed Linux tc for network experiments
-   Add experiment action of burn CPU to 100% usage
-   Add experiment action of burn I/O
-   Add experiment action of delay network
-   Add experiment action of network loss
-   Add experiment action of network corruption
-   Add experiment action of advanced network input
-   [Beta] Add experiment action of fill disk

