import boto3
import json
import time

dynamodb = boto3.resource("dynamodb")
order_table = dynamodb.Table("serverlesspresso-order-table")
def lambda_handler(event):
    Item = {
        "PK": "orders",
        "SK": event["detail"]["orderId"],
        "USERID": event["detail"]["userId"],
        "ORDERSTATE": event["detail"]["eventId"] + "-CREATED",
        "TaskToken": event["detail"]["TaskToken"],
        "TS": int(time.time()),
    }
    robot = False
    if event["detail"].get("robot"):
        robot = True
    Item["robot"] = robot
    order_table.put_events(Item)
    return json.dumps(Item)
