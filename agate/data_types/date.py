#!/usr/bin/env python

import datetime

import isodate
import parsedatetime
import six

from agate.data_types.base import DataType
from agate.exceptions import CastError

class Date(DataType):
    """
    Data type representing dates only.

    :param date_format:
        A formatting string for :meth:`datetime.datetime.strptime` to use
        instead of using regex-based parsing.
    """
    def __init__(self, date_format=None, **kwargs):
        super(Date, self).__init__(**kwargs)

        self.date_format = date_format
        self.parser = parsedatetime.Calendar()

    def test(self, d):
        """
        Test, for purposes of type inference, if a value could possibly be valid
        for this column type. This will work with values that are native types
        and values that have been stringified.
        """
        if d is None:
            return True

        if type(d) is datetime.date:
            print (d)
            return True

        if not isinstance(d, six.string_types):
            return False

        d = d.strip()

        if d.lower() in self.null_values:
            return True

        if self.date_format:
            try:
                datetime.datetime.strptime(d, self.date_format)
            except ValueError:
                return False

            return True

        value, status = self.parser.parseDT(d)

        if status == 1:
            return True

        try:
            dt = isodate.parse_date(d)

            return True
        except:
            pass

        return False

    def cast(self, d):
        """
        Cast a single value to a :class:`datetime.date`.

        :param date_format:
            An optional :func:`datetime.strptime` format string for parsing
            datetimes in this column.
        :returns:
            :class:`datetime.date` or :code:`None`.
        """
        if isinstance(d, datetime.date) or d is None:
            return d
        elif isinstance(d, six.string_types):
            d = d.strip()

            if d.lower() in self.null_values:
                return None

        if self.date_format:
            dt = datetime.datetime.strptime(d, self.date_format)

            return dt.date()

        value, status = self.parser.parseDT(d)

        if status == 1:
            return value.date()

        try:
            dt = isodate.parse_date(d)

            return dt
        except:
            pass

        raise CastError('Can not parse value "%s" as date.' % d)

    def csvify(self, d):
        if d is None:
            return None

        return d.isoformat()

    def jsonify(self, d):
        return self.csvify(d)
