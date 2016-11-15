# Data Refinement

The specification states that we should "refine initial (raw) data and save the refined data for the subsequent work". 
However, it leaves it pretty open as to how we want to do this. 

As such, we should keep a track of the fields we choose to remove and our justification for doing so.

## Field Considerations

### `time` and `created_at` 
It appears that these fields show the time that the tweet occurred in two different formats. 
As such, they should be replaced with a single, easily parsible format under the least complicated header: `time`

### `geo-coordinate` 
This field is sparsely populated. 
If we do not plan on using it, it should be removed

### `in_reply_to` fields
These fields contain a special case of the `user_mentions` list inside `entities_str` where a tweet is a reply if the first thing that occurs within it's body is a user mention.
This means that any tweet with a user mention at index 0 is in reply to that user. 

#### `in_reply_to_status_id_str` 
This field might still be necessary as the entities object does not store any information on what status we are in reply to.
This would also provide another, easier way to check if the tweet is a reply.


## Entity Duplication
Many of the fields are also contained in the `entities_str` object for each entry. This duplication of data is bad and we should try to remove this.

## Proposed Format

The main dataframe format:

| Field                       | Description                           |
|-----------------------------|---------------------------------------|
| `id_str`                    | ID of the status                      |
| `from_user`                 | Username of the status owner          |
| `text`                      | Plain text of the status              |
| `time`                      | UTC time of status                    |
| `user_lang`                 | Language identification code          |
| `from_user_id_str`          | ID of the status owner                |
| `in_reply_to_status_id_str` | ID of the status being responded to   |
| `source`                    | The twitter client being used         |
| `user_followers_count`      | Status owner's no. followers          |
| `user_friends_count`        | No. owner's followers who follow back |
| `status_url`                | URL for the status                    |
| `entities_str`              | JSON string describing tweet further  |

### entities_str

The `entities_str` field could also be simplified.
It may contain unnecessary metadata referring to media included in the tweet or to a 'symbol'.

Twitters documentation for this field can be found [here](https://dev.twitter.com/overview/api/entities-in-twitter-objects#symbols) 

Although this field varies largely, so it may be best to leave as is and focus on moving forward with analysis
