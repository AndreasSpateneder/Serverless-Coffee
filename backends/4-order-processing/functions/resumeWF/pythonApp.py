import json
import boto3

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': "Content-Type,Authorization,authorization",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

stepfunctions = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print(json.dumps(event, indent=2))

    """
    2.**********************************************
    Make ready the data
    **********************************************
    """
    order_id = event['detail']['orderId']
    task_token = event['detail']['TaskToken']

    """
    2.**********************************************
    RESUME SFN WF (ORDER SERVICE)
    **********************************************
    """
    params = {
        'output': json.dumps({"orderId": order_id}),
        'taskToken': task_token
    }

    try:
        res = stepfunctions.send_task_success(**params)
    except Exception as err:
        print(err)

    """
    3.**********************************************
    RETURN Success
    **********************************************
    """
    return {
        'statusCode': 200,
        'body': json.dumps({'success': True}),
        'headers': headers
    }
