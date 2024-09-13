#!/usr/bin/env python3
"""
Here the module description
"""
from datetime import datetime
import logging
import re
from typing import List

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Filtering the data """
    for fd in fields:
        replace = '{}={}{}'.format(fd, redaction, separator)
        message = re.sub(r'{}=(.)*?{}'.format(fd, separator), replace, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Here we define the formating of the log """
        data = filter_datum(fields=self.fields, redaction=self.REDACTION,
                            message=record.msg, separator=self.SEPARATOR)
        return self.FORMAT % {'name': record.name, 'asctime': datetime.now(),
                              'levelname': record.levelname, 'message': data}


def get_logger() -> logging.Logger:
    """ Here the get logger function defined """
    logger = logging.Logger(
        name="user_data",
        level=logging.INFO,
    )
    logger.propagate = False
    logger.addHandler(logging.StreamHandler(stream=RedactingFormatter))
    logger.addFilter(PII_FIELDS)
    return logger
