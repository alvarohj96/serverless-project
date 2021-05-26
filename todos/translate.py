import os
import json

import boto3

dynamodb = boto3.resource('dynamodb')

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    # fetch todo from the database
    item_translate = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    
    # call to the AWS Translate Text function 
    client = boto3.client(service_name='translate')
    result = client.translate_text(Text=item_translate['Item']['text'], SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])  

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result.get('TranslatedText'))
    }
    
    return response