import boto3
import json
import time

dynamodb = boto3.resource("dynamodb")
order_table = dynamodb.Table("serverlesspresso-order-table")


def lambda_handler(event):
    order_table.update_item(
        Key={"PK": "orders", "SK": event["detail"]["orderId"]},
        UpdateExpression="set ORDERSTATE = :state, TS = :TS, reason = :reason",
        ExpressionAttributeValues={
            ":state": event["detail"]["eventId"] + "-CANCELLED",
            ":reason": event["detail"]["cause"],
            ":TS": int(time.time()),
        },
        ReturnValues="ALL_NEW",
    )

    return {"success": True}
