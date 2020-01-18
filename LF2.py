import json
import boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    # TODO implement
    
    print("the event is:",event)
    print("the context is:",context)
   
    sentence = get_sentence(event)
    #sentence = "show me some pictures with shirt and Table"
   
    keywords = lex_phrase(sentence)
    print("keywords:",keywords)
    
    urls = elastic_search(keywords)
    print(urls)
    res = form_json(urls,keywords)
    print(res)
    return res
    '''
    return {
        'messages':res
    }
    '''
    
    
    #return form_json(urls,keywords)
    
def get_sentence(event):
    #don't know what kind of the event yet
    #inputText = event['body-json']['messages'][0]['unstructured']['text']
    inputText = event['params']['querystring']['query']
    print("LOLOLOLOL:", inputText)
    return inputText
    
def form_json(urls,keywords):
    result = []
    for url in urls:
        single_res = {
            "url":url,
            "labels":keywords
        }
        print(single_res)
        result.append(single_res)
    
    return {
        "results":result
    }
   
def lex_phrase(sentence):
    key_words = []
    client = boto3.client('lex-runtime')
    lex_response = client.post_text(
        botName = 'PhotoSearch',
        botAlias = 'koko',
        userId = "shit",
        inputText = sentence
    )
    print("lex response:",lex_response['message'])
    key_words = lex_response['message'].split(" ")
    print(key_words)
    return key_words

def elastic_search(keywords):
   
    host = 'vpc-photos-um6blvqixup6knzqyrqiji4zoa.us-east-1.es.amazonaws.com'
    index = 'photos'
    ES_URL = 'https://' + host + '/' + index + '/_search'
    headers = {'Content-Type': 'application/json'}
    urls = []
    for k in keywords:
        data = {
            'size': 10,
            'query': {
                'match': {
                    'labels':k
                }
            }
        }
        d = json.dumps(data)
        res = requests.get(url = ES_URL, data = d, headers = headers)
        response = res.json()
        for hit in response['hits']['hits']:
            print(hit)
            key = hit['_source']['objectKey']
            bucket = hit['_source']['bucket']
            newurl = 'https://' + bucket + '.s3.amazonaws.com' + '/' + key
            if newurl not in urls:
                urls.append(newurl)
    return urls
   
