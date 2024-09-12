#!/usr/bin/env python3
"""
Here the module description
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Filtering the data """
    for fd in fields:
        replace = '{}={}{}'.format(fd, redaction, separator)
        message = re.sub(r'{}=(.)*?{}'.format(fd, separator), replace, message)
    return message
