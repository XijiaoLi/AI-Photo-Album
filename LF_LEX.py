import json

def lambda_handler(event, context):
    # TODO implement
    print(event)
    session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}
    key1 = event['currentIntent']['slots']['keyword']
    key2 = event['currentIntent']['slots']['kkeyword']
    print(key1, key2)
    
    if key1 is None:
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': event['currentIntent']['slots'],
                'slotToElicit': "keyword",
                'message': {
                    'contentType': 'PlainText',
                    'content': 'What do you want?'
                }
            }
        }
    else:
        key1 = tokenize(key1)
        if not key2 is None:
            key2 = tokenize(key2)
    
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': key1 + " " + key2
            }
        }
    }
    
def tokenize(key):
    if key.endswith('es'):
        key = key[:-2]
    elif key.endswith('s'):
        key = key[:-1]
    return key
