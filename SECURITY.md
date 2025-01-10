# Security Policy

## Supported Versions

| Version                | Supported          |
| ---------------------- | ------------------ |
| v1.0.0                 | :white_check_mark: |
| lesser than v1.0.0     | :x:                |


## How we determine installed games

First, we are checking for 2 Registry Keys. They are used to recognize the platform a game was installed with.
  - Registry Key for Steam (r"SOFTWARE\Valve\Steam")
  - Registry Key for Epic Games (r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher")

After determining your Epic & Steam Library, we check for existence of Files in any given SavePath we know. This way we avoid scanning & analyzing unrelated files and also remove a lot of overhead.

