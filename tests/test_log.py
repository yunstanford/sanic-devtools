import json
import logging
import re
import sys
from unittest.mock import MagicMock
import pytest
from sanic_devtools.log import AccessFormatter, DefaultFormatter


def _mk_record(msg, level=logging.INFO, **extra):
    class Record:
        levelno = level
        exc_info = None
        exc_text = None
        stack_info = None

        def __init__(self):
            if extra:
                for k, v in extra.items():
                    setattr(self, k, v)

        def getMessage(self):
            return msg
    return Record()


def test_dft_formatter():
    f = DefaultFormatter()
    assert f.format(_mk_record('testing')) == 'testing'


def test_dft_formatter_colour():
    f = DefaultFormatter()
    f.stream_is_tty = True
    assert f.format(_mk_record('testing')) == '\x1b[32mtesting\x1b[0m'


def test_dft_formatter_colour_time():
    f = DefaultFormatter()
    f.stream_is_tty = True
    assert f.format(_mk_record('[time] testing')) == '\x1b[35m[time]\x1b[0m\x1b[32m testing\x1b[0m'


def test_access_formatter():
    f = AccessFormatter()
    msg = json.dumps({'time': '_time_', 'prefix': '_p_', 'msg': '_msg_', 'dim': False})
    assert f.format(_mk_record(msg)) == '_time_ _p_ _msg_'


def test_access_formatter_no_json():
    f = AccessFormatter()
    assert f.format(_mk_record('foobar')) == 'foobar'


def test_access_formatter_colour():
    f = AccessFormatter()
    f.stream_is_tty = True
    msg = json.dumps({'time': '_time_', 'prefix': '_p_', 'msg': '_msg_', 'dim': False})
    assert f.format(_mk_record(msg)) == '\x1b[35m_time_\x1b[0m \x1b[34m_p_\x1b[0m \x1b[0m_msg_\x1b[0m'


def test_access_formatter_extra():
    f = AccessFormatter()
    msg = json.dumps({'time': '_time_', 'prefix': '_p_', 'msg': '_msg_', 'dim': False})
    assert f.format(_mk_record(msg, details={'foo': 'bar'})) == (
        'details: {\n'
        "    'foo': 'bar',\n"
        '}\n'
        '_time_ _p_ _msg_'
    )


def test_access_formatter_exc():
    f = AccessFormatter()
    try:
        raise RuntimeError('testing')
    except RuntimeError:
        stack = f.formatException(sys.exc_info())
        assert stack.startswith('Traceback (most recent call last):\n')
        assert stack.endswith('RuntimeError: testing\n')


def test_access_formatter_exc_colour():
    f = AccessFormatter()
    f.stream_is_tty = True
    try:
        raise RuntimeError('testing')
    except RuntimeError:
        stack = f.formatException(sys.exc_info())
        assert stack.startswith('\x1b[38;5;26mTraceback')
