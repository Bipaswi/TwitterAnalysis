''' Module for the analysis of a twitter data set

Provides a collection of functions for analysing the dataset:

  - analyse_types
  - analyse_hashtags
  - analyse_field
  - analyse_entities 
  - analyse_replies
  - analyse_retweets
  - analyse_types_generic
  - analyse_time

These functions all take the dataset as an argument, perform some
analysis, and return a dataset containing the calculated values.

'''

from collections import defaultdict
from encode import encode_json
import pandas as pd
import json

######################################################################
#
#  Tweet Type Analysis
#


def _group(row):

    # Relies on NaN != NaN
    if row.in_reply_to_status_id_str == row.in_reply_to_status_id_str:
        return 'reply'

    elif row.text[0:2] == 'RT':
        return 'retweet'

    else:
        return 'tweet'


def _count_types(data):
    '''
    '''
    count = defaultdict(int)
    for tweet in data:
        count[tweet] += 1
    return count


def analyse_types(data):
    ''' Count occurrences of each type of tweet

    This function will analyse the dataset and produce a DataFrame
    counting how many tweets, retweets and replies were posted by
    each user.

    Args:
      data (pandas.DataFrame): The twitter dataset

    Returns:
       pandas.DataFrame: Hashtag counts (indexed by user id)

    DataFrame Format:

    +-----------------------+---------------------------------------------+
    | Field                 | Description                                 |
    +=======================+=============================================+
    | `tweet`               | Integer count of occurences (default: NaN)  |
    +-----------------------+---------------------------------------------+
    | `retweet`             | Integer count of occurences (default: NaN)  |
    +-----------------------+---------------------------------------------+
    | `reply`               | Integer count of occurences (default: NaN)  |
    +-----------------------+---------------------------------------------+

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> types = analyse_types(df)
    types = analyse_types(df)
    >>> types
                       tweet retweet reply
    68963                  1     NaN   NaN
    284553               NaN       2   NaN
    726453               NaN       1   NaN
    740343               NaN     NaN     1
    ...                  ...     ...   ...
    '''
    data['type_'] = data.apply(_group, axis=1)
    byuser = data.groupby('from_user_id_str')

    users = (user for user, tweets in byuser)
    result = pd.DataFrame(columns=['tweet', 'retweet', 'reply'],
                          index=users)

    for user, tweets in byuser:
        result.loc[user] = pd.Series(_count_types(tweets.type_))

    data.drop('type_', axis=1, inplace=True)
    encode_json(result.sum(), 'sum_types.json')
    return result

######################################################################
#
#  Hashtag Popularity Analysis
#

def _flatten(listgen, field_name):
    for i in listgen:
        for x in i:
            yield x[field_name]


######################################################################
#
#  Chosen field Analysis
#
#

def analyse_field(data, field, thres=50):
    """  Count occurrences of each chosen field

    This function will analyse the field and count the occurences
    of each field used

    Args:
      data (pandas.DataFrame): The twitter dataset
      field: The field in the DataFrame you want to analyse
      thres: The threshold you want your data set to adhere to 

    Returns:
       pandas.DataFrame: field counts (indexed by Application)

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> analyse_applications(df)
    Tweedle                           2
    @SmabAudio App                    1
    Application to RT                 3
    BOTlibre!                         1
    BeingExample                      2
                                      ..

    """
    counts = defaultdict(int)
    for x in data[field]:
        counts[x] += 1

    series= pd.Series(_refine_counts(counts, thres))
    result = pd.DataFrame({field:series.index, 'count':series.values})
    return result

#_
def _refine_counts(counts, thres):
    new_counts = defaultdict(int)
    for cli, occ in counts.items():
        if occ < thres:
            new_counts['others'] += occ
        else:
            new_counts[cli] = occ
    return new_counts

# TODO(jac32): Map hashtag relationships

def analyse_entities(data, entity, field):
    """ Count occurrences of each object in entity_field.

    This function will analyse the entities field of each tweet and
    produce a Pandas DataFrame containing an occurrences count for
    each entity_field you are looking for.

    Args:
      data (pandas.DataFrame): The twitter dataset
      entity (str): The entity type to be examined
      field (str): The field within the entity to be examined

    Returns:
       pandas.DataFrame: entity_field counts (indexed by the entity field)

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> analyse_entities_str(df, 'hashtags', 'text')
    14JCID                    1
    3dprinting               10
    4life                     2
    AI                        1
                             ..

    """
    entities = (tweet[entity] for tweet in data.entities_str)
    fields = _flatten(entities, field)

    counts = defaultdict(int)
    for field in fields:
        counts[field] += 1

    series = pd.Series(counts)
    result = pd.DataFrame({entity:series.index, 'count':series.values})
    return result


#######################################################
#
# analyses replies to user
#

def analyse_replies(data):
    """ Count occurrences of each reply to user

    This function will analyse the replies to each user of each tweet and
    produce a Pandas DataFrame containing an occurrences count for
    each reply to user.

    Args:
      data (pandas.DataFrame): The twitter dataset

    Returns:
       pandas.DataFrame: entity_field counts (indexed by the entity_field)

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> analyse_replies(df)
    6.897321e+17    1
    6.917383e+17    3
    6.977457e+17    1
    7.022103e+17    1
    7.024451e+17    1
    7.025329e+17    2
    7.025612e+17    1
                    ..
    """

    counts = defaultdict(int)
    for in_reply_to_status_id_str in data.in_reply_to_status_id_str:
        if in_reply_to_status_id_str == in_reply_to_status_id_str:
            counts[in_reply_to_status_id_str] += 1

    result = pd.Series(counts)
    return result

def _group_retweets(row):
    if row.text[0:2] == 'RT':
        return 'retweet'
   
def analyse_retweets(data):

    """ Count occurrences of each retweet to user

    This function will analyse the replies to each user of each tweet and
    produce a Pandas DataFrame containing an occurrences count for
    each reply to user.

    Args:
      data (pandas.DataFrame): The twitter dataset

    Returns:
       pandas.DataFrame: entity_field counts (indexed by the entity_field)

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> analyse_retweets(data)
                          retweet
    68963                  NaN
    284553                   2
    726453                   1
    740343                 NaN
    763418                 NaN
    769897                   1
    1147031                NaN
    1168961                  2
    1186911                  5
    1210901                  1
    1222151                  1
    1223671                  2
    1348691                  1
    1349941                NaN
                        ..
    """

    data['type_'] = data.apply(_group_retweets, axis=1)
    byuser = data.groupby('from_user_id_str')

    users = (user for user, tweets in byuser)
    result = pd.DataFrame(columns=['retweet'],
                          index=users)

    for user, tweets in byuser:
        result.loc[user] = pd.Series(_count_types(tweets.type_))

    data.drop('type_', axis=1, inplace=True)
    return result

###########
# changes the groupby. possible to analyse with any two fields
#
#

def analyse_relations(data, field, tweet_type, step="h"):

    """ Count occurrences of each tweet type to a chosen field

    This function will analyse the replies to each user of each tweet and
    produce a Pandas DataFrame containing an occurrences count for
    each reply to user.

    Args:
      data (pandas.DataFrame): The twitter dataset
      field (str): The field within the entity to be examined
      tweet_type: The type of tweet you want to analyse
      step: The step in time you want to group by


    Returns:
       pandas.DataFrame: entity_field counts (indexed by the entity_field)

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> analyse_replations(df, time, tweet)
                           tweet
    2016-01-03 00:43:42   NaN
    2016-01-03 00:45:00   NaN
    2016-01-03 01:12:15     1
    2016-01-03 01:15:57   NaN
    2016-01-03 01:31:46   NaN
    2016-01-03 01:35:17   NaN
    2016-01-03 03:19:02     1
    2016-01-03 03:25:42   NaN
    2016-01-03 05:23:03     1
                    ..
    """

    data['type_'] = data.apply(_group, axis=1)
    if field == "created_at":
        per = data['created_at'].dt.to_period(step)
        byuser = data.groupby(per)
    else:
        byuser = data.groupby(field)

    users = (user for user, tweets in byuser)
    if tweet_type == 'tweet' or tweet_type or 'retweets' or tweet_type == 'replies':
        result = pd.DataFrame(columns=[tweet_type],
                          index=users)

    for user, tweets in byuser:
        result.loc[user] = pd.Series(_count_types(tweets.type_))

    data.drop('type_', axis=1, inplace=True)
    return result

def analyse_types_field(data, field, step="h"):
    ''' Count occurrences of each type of tweet

    This function will analyse the dataset and produce a DataFrame
    counting how many tweets, retweets and replies were posted by
    each field.

    Args:
      data (pandas.DataFrame): The twitter dataset
      field (str): The field within the entity to be examined
      tweet_type: The type of tweet you want to analyse
      step: The step in time you want to group by

    Returns:
       pandas.DataFrame: Hashtag counts (indexed by the field chosen)

    DataFrame Format:

    +-----------------------+---------------------------------------------+
    | Field                 | Description                                 |
    +=======================+=============================================+
    | `tweet`               | Integer count of occurences (default: NaN)  |
    +-----------------------+---------------------------------------------+
    | `retweet`             | Integer count of occurences (default: NaN)  |
    +-----------------------+---------------------------------------------+
    | `reply`               | Integer count of occurences (default: NaN)  |
    +-----------------------+---------------------------------------------+

    Example:

    >>> from parse import parse_data
    from parse import parse_data
    >>> df =  parse_data('../Data/digifest16.csv')
    df =  parse_data('../Data/digifest16.csv')
    >>> types = analyse_types(df)
    types = analyse_types(df)
    >>> types
    types
                       tweet retweet reply
    68963                  1     NaN   NaN
    284553               NaN       2   NaN
    726453               NaN       1   NaN
    740343               NaN     NaN     1
    ...                  ...     ...   ...
    '''
    data['type_'] = data.apply(_group, axis=1)
    if field == "created_at":
        per = data['created_at'].dt.to_period(step)
        byfield = data.groupby(per)
    else:        
        byfield = data.groupby(field)

    field_index = (f for f, tweets in byfield)
    result = pd.DataFrame(columns=['tweet', 'retweet', 'reply'],
                          index=field_index)

    for f, tweets in byfield:
        result.loc[f] = pd.Series(_count_types(tweets.type_))

    data.drop('type_', axis=1, inplace=True)
    return result

def analyse_interactions(data, adr="Display/interactions.json"):
    data = data.groupby('from_user_id_str')
    results = {}
    for user, tweets in data:
        results[str(user)] = _concat(tweets.apply(_getMentions, axis=1))
    with open(adr, "w") as dumpfile:
        json.dump(results, dumpfile)    

def _getMentions(tweet):
    return map((lambda x: x['id_str']), tweet['entities_str']['user_mentions'])

def _concat(lists):
    l = [element for list_ in lists for element in list_]
    return l



