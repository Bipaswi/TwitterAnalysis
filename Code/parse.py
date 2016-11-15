""" Module for parsing a twitter data set

Main interaction point is the parse_data function

:example:

>>> from parse import parse_data
>>> df = parse_data('../Data/digifest16.csv')
>>> df.columns
Index(['id_str', 'from_user', 'text', 'time', 'user_lang', 'from_user_id_str',
       'in_reply_to_status_id_str', 'source', 'user_followers_count',
       'user_friends_count', 'status_url', 'entities'],
      dtype='object')

"""

import os
import json
import pandas as pd
import re

# TODO(jac32): Revisit the entities_str -> entities naming choice here
# TODO(jac32): Check all lines are shorter than PEP8/Google style suggests

def _parse_file(path, cols):
    ''' Parse twitter data from csv file to a useful format

    This function will parse twitter data stored as a csv file at the
    absolute path provided.

    Args:
       path (str):  Absolute path to the csv datafile
       col (List[str]): columns to parse

    Returns:
       pandas.DataFrame: DataFrame storing the refined twitter data

    '''
    if 'created_at' in cols:
        data = pd.read_csv(path, usecols=cols)
        data.created_at = pd.to_datetime(data['created_at'])
    else:
        data = pd.read_csv(path, usecols=cols)

    if 'entities_str' in cols:
        data['entities_str'] = data['entities_str'].apply(json.loads)
    
    if 'source' in cols:
        data['source'] = data['source'].apply(lambda x: re.search("<.+>(.*)<\/.+>", x).groups()[0])

    return data

def parse_data(relpath, cols=None):
    ''' Parse and refine twitter data

    This function will serve as the point of interaction with
    this parsing module and will parse the twitter data at a
    provided relative path.

    Args:
       relpath (str):  Relative path to the csv datafile

    Keyword Args:
       col (List[str]): columns to parse

    Returns:
       Pandas DataFrame

    DataFrame Format:

    +-----------------------------+---------------------------------------+
    | Field                       | Description                           |
    +=============================+=======================================+
    | `id_str`                    | ID of the status                      |
    +-----------------------------+---------------------------------------+
    | `from_user`                 | Username of the status owner          |
    +-----------------------------+---------------------------------------+
    | `text`                      | Plain text of the status              |
    +-----------------------------+---------------------------------------+
    | `time`                      | UTC time of status                    |
    +-----------------------------+---------------------------------------+
    | `user_lang`                 | Language identification code          |
    +-----------------------------+---------------------------------------+
    | `from_user_id_str`          | ID of the status owner                |
    +-----------------------------+---------------------------------------+
    | `in_reply_to_status_id_str` | ID of the status being responded to   |
    +-----------------------------+---------------------------------------+
    | `source`                    | The twitter client being used         |
    +-----------------------------+---------------------------------------+
    | `user_followers_count`      | Status owner's no. followers          |
    +-----------------------------+---------------------------------------+
    | `user_friends_count`        | No. owner's followers who follow back |
    +-----------------------------+---------------------------------------+
    | `status_url`                | URL for the status                    |
    +-----------------------------+---------------------------------------+
    | `entities_str`              | JSON string describing tweet further  |
    +-----------------------------+---------------------------------------+
    '''

    if cols is None:
        # If the header is not listed here, column is removed
        cols = ['id_str',
                'from_user',
                'text',
                'created_at',
                'user_lang',
                'from_user_id_str',
                'in_reply_to_status_id_str',
                'source',
                'user_followers_count',
                'user_friends_count',
                'status_url',
                'entities_str']

    # Convert relative path to absolute path
    home = os.path.dirname(os.path.realpath('__file__'))
    path = os.path.join(home, relpath)

    # Parse and refine CSV file (minus the unnecessary columns)
    data = _parse_file(path, cols)
    return data
