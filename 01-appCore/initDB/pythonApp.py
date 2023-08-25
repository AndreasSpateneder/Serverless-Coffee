import json
import http.client as http_client
import boto3
import pythonInitMenu

def send_response(event, context, response_status, response_data):
    response_body = json.dumps({
        "Status": response_status,
        "Reason": f"See the details in CloudWatch Log Stream: {context.log_stream_name}",
        "PhysicalResourceId": context.log_stream_name,
        "StackId": event['StackId'],
        "RequestId": event['RequestId'],
        "LogicalResourceId": event['LogicalResourceId'],
        "Data": response_data
    })

    parsed_url = http_client.urlsplit(event['ResponseURL'])
    connection = http_client.HTTPSConnection(parsed_url.netloc)
    headers = {
        'Content-Type': '',
        'Content-Length': str(len(response_body))
    }

    print('SENDING RESPONSE...\n')

    connection.request('PUT', parsed_url.path, body=response_body, headers=headers)
    response = connection.getresponse()

    print('STATUS:', response.status)
    print('HEADERS:', response.getheaders())

    connection.close()

def lambda_handler(event, context):
    print('REQUEST RECEIVED:\n', json.dumps(event))

    if event['RequestType'] == 'Create':
        print('CREATE!')
        pythonInitMenu.init_menu()
        send_response(event, context, 'SUCCESS', {'Message': 'Resource creation successful!'})
    elif event['RequestType'] == 'Update':
        print('UPDATE!')
        pythonInitMenu.init_menu()
        send_response(event, context, 'SUCCESS', {'Message': 'Resource update successful!'})
    elif event['RequestType'] == 'Delete':
        print('DELETE!')
        send_response(event, context, 'SUCCESS', {'Message': 'Resource deletion successful!'})
    else:
        print('FAILED!')
        send_response(event, context, 'FAILED', {})

    print('FINISHED')
