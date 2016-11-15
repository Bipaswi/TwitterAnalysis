import pandas
from parse import parse_data
from analyse import analyse_types
from analyse import analyse_entities
from analyse import analyse_replies
from analyse import analyse_field
from analyse import analyse_retweets
from analyse import analyse_relations
from analyse import analyse_field
from analyse import analyse_types_field
from analyse import analyse_interactions
from encode import encode_json

data = parse_data("../Data/digifest16.csv")

print("*******")

#types = analyse_types(data)
#encode_json(types.sum(), 'sum_types.json')
#print (types)
#print("*******")
#tweet_time = analyse_types_field(data, "created_at", "h")
#print(tweet_time)
#encode_json(tweet_time, "tweet_time.json")
#print(tweet_time)

print("********")

#testTime = analyse_relations(data, "created_at", "tweet")
#encode_json(testTime, "relation_tweet_time.json")
#print(testTime)

print("********")

#mentions = analyse_entities(data, 'user_mentions', 'id_str')
#encode_json(mentions, "mentions.json")
#print(mentions)

print("*******")

#hashtags = analyse_entities_str(data, 'hashtags', 'text')
#print(hashtags)

print("*******")

#apps = analyse_field(data, 'source')
#apps.to_json()
#print(apps.max())
#encode_json(apps, "Apps_count.json")
#encode_json(apps, "test.json")

#apps = analyse_applications(data)
#print(apps)

print("*******")

#retweets = analyse_entities_str(data, 'user_mentions', 'name')
#mean = calc_mean(retweets)
#std = calc_std(retweets)
#print(mean)
#print(std)

print("*******")

#replies = analyse_replies(data)
#encode_json(replies, "replies_per_user.json")
#print("standard deviation: ")
#print(replies.std())
#print("mean: ")
#print(replies.describe())
#print(replies)

#retweets = analyse_retweets(data)
#encode_json(retweets, "retweets_per_user.json")
#print(retweets)

print("*******")

#source_field = analyse_types_field(data, 'source')
#print(source_field)


#foo = analyse_field(data, 'time')
#print(foo)

