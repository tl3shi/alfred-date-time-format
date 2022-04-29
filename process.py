# -*- coding: utf-8 -*-

import alfred
import calendar
from delorean import utcnow, parse, epoch
import pytz
from datetime import datetime

default_date_time_str_zone = "+8"

def process(query_str):
    """ Entry point """
    value = parse_query_value(query_str)
    if value is not None:
        results = alfred_items_for_value(value)
        xml = alfred.xml(results) # compiles the XML answer
        alfred.write(xml) # writes the XML back to Alfred

def parse_query_value(query_str):
    """ Return value for the query string """
    try:
        query_str = str(query_str).strip('"\' ')
        if query_str == 'now':
            d = utcnow()
        else:
            # Parse datetime string or timestamp
            try:
                if len(query_str) == 10: #seconds
                    d = epoch(float(query_str))
                else: # milliseconds
                    d = epoch(float(query_str)/1000)
            except ValueError:
                # default convert timezone
                if ('+' not in str(query_str)):
                    query_str += default_date_time_str_zone
                d = parse(str(query_str))
    except (TypeError, ValueError):
        d = None
    return d

def alfred_items_for_value(value):
    """
    Given a delorean datetime object, return a list of
    alfred items for each of the results
    """

    index = 0
    results = []

    # First item as timestamp
    item_value = calendar.timegm(value.datetime.utctimetuple())
    results.append(alfred.Item(
        title=str(item_value),
        subtitle=u'UTC Timestamp',
        attributes={
            'uid': alfred.uid(index), 
            'arg': item_value,
        },
        icon='icon.png',
    ))
    index += 1

    # Various formats
    formats = [
        # 1937-01-01 12:00:27
        ("%Y-%m-%d %H:%M:%S", ''),
    ]
    # for format, description in formats:
    #     item_value = value.datetime.strftime(format)
    #     results.append(alfred.Item(
    #         title=str(item_value),
    #         subtitle=description,
    #         attributes={
    #             'uid': alfred.uid(index), 
    #             'arg': item_value,
    #         },
    #     icon='icon.png',
    #     ))
    #     index += 1

    tz = pytz.timezone('Asia/Shanghai')
    dt = datetime.fromtimestamp(item_value, tz)
    temp= dt.strftime("%Y-%m-%d %H:%M:%S")

    results.append(alfred.Item(
            title=str(temp),
            subtitle="Asia/Shanghai",
            attributes={
                'uid': alfred.uid(index), 
                'arg': temp,
            },
            icon='icon.png',
        ))
    index+=1
# Asia/Shanghai

    # results.append(alfred.Item(
    #         title=str(item_value),
    #         subtitle=description,
    #         attributes={
    #             'uid': alfred.uid(index), 
    #             'arg': item_value,
    #         },
    #         icon='icon.png',
    #     ))
    return results

if __name__ == "__main__":
    try:
        query_str = alfred.args()[0]
    except IndexError:
        query_str = None
    process(query_str)
