# Convert Date

## Installation

1. Clone this repository.
2. Double-click `Convert Date.alfredworkflow`.

## Query format

`VALUE|'now' [as FORMAT_NAME]`

where `VALUE` can be:

- an integer: seconds since the epoch
- e.g. `June 8, 2018`
- e.g. `2013-03-04 12:04:05`
- e.g. `2013/3/4`
- etc.

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
