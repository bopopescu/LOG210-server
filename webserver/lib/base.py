from flask import json

def jsonify(data):
    return json.dumps(data)

def decode_datetime(data, remove_timezone=True):
    """ Extract a python datetime from a string in one of either format :
    * RFC822
    * RFC1123
    * RFC1036
    * ISO8601 (python datetime.isoformat)
    * ANSI c datetime format with or without timezone extension

    :param data: the string to convert to datetime
    :type data: str or unicode
    :return: the datetime instance representing the string
    :return_type: datetime.datetime
    :raise TypeError: if data is neither str neither unicode
    :raise ValueError: if data can't be converted from one of the supported format

    *Help for testing the json.dumps() result of a datetime field*

    The format return by Flask/Werkzeug is RFC1123. You can display the result with this command :

        import datetime
        dt = datetime.datetime.now().strftime('%a, %02d %b %Y %H:%M:%S GMT')

    or also with werkzeug

        import datetime
        from werkzeug import http_date
        dt = http_date(datetime.datetime.now())

    """
    from dateutil import parser

    if not isinstance(data, (str, unicode)):
        raise TypeError('data must be str or unicode')

    try:
        result = parser.parse(data)
    except:
        raise ValueError('can\t convert data into datetime')

    result = result.replace(tzinfo=None) if result.tzinfo and remove_timezone else result

    return result