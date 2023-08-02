# Convert Date

## Installation

1. Clone this repository.
2. Double-click `Convert Date.alfredworkflow`.

## Query format

`VALUE|'now' [as FORMAT_NAME]`

where `VALUE` can be either an integer (seconds since the epoch) or `YYYY-mm-dd`/`YYYY-mm-dd HH:MM:SS` (ISO date/datetime).

For example,

- `now as epoch`: convert current datetime as timestamp
- `339850329 as ISO date`: convert this timestamp as ISO date
- `2023-08-02`: convert this ISO date to various formats

## Keymap

- `command + c`: copy the target value to clipboard
- `enter`: copy and paste the target value to frontmost app

## Dependencies

- (Optional) [`fzf`](https://github.com/junegunn/fzf): if present, the matching of `as FORMAT_NAME` query becomes fuzzy match

## Similar projects

- [`alfred-datetime-format-converter`](https://github.com/mwaterfall/alfred-datetime-format-converter)
- [`alfred-timestamp`](https://gitee.com/ManerFan/alfred-timestamp)
