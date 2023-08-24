import boto3
from fastapi import HTTPException
import json
import time
from order_api import constants
from order_api.api import Order

dynamodb = boto3.resource("dynamodb", region_name=constants.aws_region)
coffe_config_table = dynamodb.Table(constants.coffee_config["config_table"])
coffe_counting_table = dynamodb.Table(constants.coffee_config["counting_table"])
events_client = boto3.client("events")


# returns true if the shop is open
async def check_shop_open() -> bool:
    try:
        return coffe_config_table.get_item(
            Key={"PK": "config-ABC"},
        ).get(
            "Item"
        )["storeOpen"]
    finally:
        return False


def available_queue():
    try:
        return (
            coffe_counting_table.get_item(
                Key={"PK": "order-queue"},
            ).get(
                "Item"
            )["IDvalue"]
            < constants.coffee_queue_size
        )
    finally:
        return False


def emit_workflow_started(order: Order):
    Message = "The workflow waits for your order to be submitted. It emits an event with a unique 'task token'. The token is stored in an Amazon DynamoDB table, along with your order ID."
    event_details = {
        "Details": json.dumps(
            dict(
                Message=Message,
                TaskToken=time.time(),
                userId=order.userId,
                eventId=order.evenId,
                orderId=order.orderId,

            )
        ),
        "DetailType": "OrderProcessor.WorkflowStarted",
    }
    Entries = constants.events_payload | event_details
    events_client.put_events(Entries=[Entries])


def reserve_queue():
    queue = (
        coffe_counting_table.get_item(
            Key={"PK": "order-queue"},
        )
        .get("Item")
        .get("IDvalue")
    )
    if not queue:
        queue = 0
    coffe_counting_table.put_item(
        Item={
            "PK": "order-queue",
            "IDvalue": queue + 1,
        }
    )


def emit_cancel_order_event(order: Order):
    Message = "The shop was not ready, and so a 'not ready' event is emitted to cancel the current order."
    event_details = {
        "Details": json.dumps(
            dict(Message=Message, userId=order.userId, eventId=order.evenId)
        ),
        "DetailType": "OrderProcessor.ShopUnavailable",
    }
    Entries = constants.events_payload | event_details
    events_client.put_events(Entries=[Entries])


def init_queue():
    coffe_counting_table.put_item(Item={"PK": "order-queue", "IDvalue": 0})
