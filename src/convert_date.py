import os
from collections import OrderedDict
import sys
import json
import datetime as dt
import typing as ty
import re
import subprocess


def strftime(datetime: dt.datetime, fmt: str) -> str:
    """See: https://stackoverflow.com/a/71427544/7881370"""
    return datetime.strftime(
        fmt.replace('%-', '%#') if os.name == 'nt' else fmt)


def prepare_outputs(datetime: dt.datetime) -> ty.Dict[str, str]:
    """All available date formats and values given datetime object."""
    name_to_fmt = [
        ('A, B d, YYYY at II:MM:SS p', '%A, %B %-d, %Y at %I:%M:%S %p'),
        ('ISO date', '%Y-%m-%d'),
        ('ISO datetime', '%Y-%m-%d %H:%M:%S'),
        ('YYYY-mm-dd', '%Y-%m-%d'),
        ('YYYY-mm-dd HH:MM:SS', '%Y-%m-%d %H:%M:%S'),
        ('YYYY/mm/dd', '%Y/%m/%d'),
        ('YYYY/m/d', '%Y/%-m/%-d'),
        ('B d, YYYY', '%B %-d, %Y'),
    ]
    outputs = OrderedDict({'epoch': str(int(datetime.timestamp()))})
    outputs.update(
        {name: strftime(datetime, fmt)
         for name, fmt in name_to_fmt})
    return outputs


def parse_query(query: str) -> ty.Tuple[dt.datetime, str]:
    """
    Query format: [VALUE|'now'] ['as' FORMAT]
    """
    query = query.strip()
    m = re.search(r'\bas\s*(.*)$', query)
    if m:
        query = query[:m.start()].strip()
        expected_target_format = m.group(1).strip()
    else:
        expected_target_format = ''
    try:
        epoch = int(query)
        return dt.datetime.fromtimestamp(epoch), expected_target_format
    except (ValueError, TypeError):
        pass

    other_fmts_to_try = [
        '%B %d, %Y',
        '%B %d %Y',
        '%b %d, %Y',
        '%b %d %Y',
        '%Y/%m/%d',
    ]
    for fmt in other_fmts_to_try:
        try:
            return dt.datetime.strptime(query, fmt), expected_target_format
        except ValueError:
            pass

    try:
        return dt.datetime.fromisoformat(query), expected_target_format
    except ValueError:
        pass

    if query == 'now':
        return dt.datetime.now(), expected_target_format

    raise NotImplementedError('Failed to parse the input as date/datetime')


def filter_out_formats(
    expected_target_format: str,
    outputs: ty.Dict[str, str],
) -> ty.List[str]:
    """
    If ``expected_target_format`` is empty, return all keys of ``outputs``.
    If ``fzf`` is installed, use it to get the output formats. Otherwise, use
    simple containing test to decide the output formats.
    """
    if not expected_target_format:
        return list(outputs)
    try:
        resp = subprocess.run(['fzf', '--filter', expected_target_format],
                              text=True,
                              input=''.join(map('{}\n'.format, outputs)),
                              capture_output=True,
                              check=True)
        output_formats = re.findall(r'(.*)\n', resp.stdout)
    except subprocess.CalledProcessError as err:
        if err.returncode == 1:
            output_formats = []
        else:
            raise
    except FileNotFoundError:
        output_formats = [x for x in outputs if expected_target_format in x]
    return output_formats


def generate_response_err(err: Exception) -> list:
    return [{
        'title': 'Error type: {}'.format(type(err).__name__),
        'subtitle': 'Error message: {}'.format(str(err)),
        'valid': False,
        'icon': {
            'path': 'error-icon.png',
        },
    }]


def generate_response(
    output_formats: ty.List[str],
    outputs: ty.Dict[str, str],
) -> list:
    items = []
    for f in output_formats:
        items.append({
            'title': outputs[f],
            'subtitle': 'name: {}'.format(f),
            'arg': outputs[f],
            'text': {
                'copy': outputs[f],
                'largetype': outputs[f],
            },
        })
    if not items:
        items.append({
            'title': 'Error: no match format',
            'valid': False,
            'icon': {
                'path': 'error-icon.png',
            },
        })
    return items


def main():
    query = sys.argv[1]
    try:
        datetime, expected_target_format = parse_query(query)
        outputs = prepare_outputs(datetime)
        output_formats = filter_out_formats(expected_target_format, outputs)
    except Exception as err:
        items = generate_response_err(err)
    else:
        items = generate_response(output_formats, outputs)
    print(json.dumps({'items': items}), end='')


if __name__ == '__main__':
    main()
