import os
import json
import boto3

# Python way of using process.env... 
region = os.environ.get('AWS_REGION')
config_table_name = os.environ.get('configTable')
counting_table_name = os.environ.get('countingTable')

#aws_config = {'region': region}
dynamodb = boto3.client('dynamodb', region_name=region)

# load initMenuState and initCountingState JSON files
with open('./initMenuState.JSON', 'r') as menu_state_file:
    init_menu_state = json.load(menu_state_file)

with open('./initCountingState.JSON', 'r') as counting_state_file:
    init_counting_state = json.load(counting_state_file)

batch_write_params = {
    config_table_name: [],
    counting_table_name: []
}

config_item = {
    'PutRequest': {
        'Item': init_menu_state
    }
}
batch_write_params[config_table_name].append(config_item)

for counting_item in init_counting_state:
    counting_item_request = {
        'PutRequest': {
            'Item': counting_item
        }
    }
    batch_write_params[counting_table_name].append(counting_item_request)

def init_menu():
    try:
        print('params', json.dumps(batch_write_params, indent=2))
        result = dynamodb.batch_write_item(RequestItems=batch_write_params)
        print('initMenus result:', result)
    except Exception as err:
        print('initMenus error:', err)


