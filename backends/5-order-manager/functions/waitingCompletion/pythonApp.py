
import boto3
import json
import datetime

dynamodb = boto3.resource("dynamodb")
order_table = dynamodb.Table("serverlesspresso-order-table")
event_bridge = boto3.client('events')
def lambda_handler(event, context):
    params = {
        'Key': {
            'PK': 'orders',
            'SK': event['detail']['orderId'],
        },
        'UpdateExpression': "set TS = :TS, TaskToken = :TaskToken, orderNumber = :orderNumber",
        'ConditionExpression': "#userId = :userId",
        'ExpressionAttributeNames': {
            "#userId": "USERID"
        },
        'ExpressionAttributeValues': {
            ":userId": event['detail']['userId'],
            ":TaskToken": event['detail']['TaskToken'],
            ":orderNumber": event['detail']['orderNumber'],
            ":TS": int(datetime.datetime.now().timestamp()*1000)
        },
        'ReturnValues': "ALL_NEW"
    }

    print(params)

    result = order_table.update_item(**params)
    print(result)

    # Publish event to EventBridge
    response = event_bridge.put_events(
        Entries=[
            {
                'Detail': json.dumps({
                    'orderId': result['Attributes']['SK'],
                    'orderNumber': result['Attributes']['orderNumber'],
                    'state': result['Attributes']['ORDERSTATE'],
                    'drinkOrder': json.loads(result['Attributes']['drinkOrder']),
                    'userId': result['Attributes']['USERID'],
                    'robot': result['Attributes']['robot'],
                    'eventId': event['detail']['eventId'],
                    'TS': result['Attributes']['TS'],
                    'Message': "A Lambda function is invoked which stores the Step Functions Task Token in an Amazon DynamoDB table. The Task Token is later used to resume the workflow when the barista completes or cancels the order."
                }),
                'DetailType': 'OrderManager.WaitingCompletion',
                'EventBusName': os.environ['BusName'],
                'Source': os.environ['Source'],
                'Time': datetime.datetime.now().timestamp() *1000
            }
        ]
    )
    print(response)