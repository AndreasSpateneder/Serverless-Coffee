import boto3
from pydantic import BaseModel
import json
import time
from order_api import constants

dynamodb = boto3.resource("dynamodb", region_name=constants.aws_region)
coffe_config_table = dynamodb.Table(constants.coffee_config["config_table"])
coffe_counting_table = dynamodb.Table(constants.coffee_config["counting_table"])
coffe_order_table = dynamodb.Table(constants.coffee_config["order_table"])
events_client = boto3.client("events", region_name=constants.aws_region)


class Order(BaseModel):
    userId: str
    eventId: str


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


def emit_workflow_started(order: Order, orderId: int):
    Message = "The workflow waits for your order to be submitted. It emits an event with a unique 'task token'. The token is stored in an Amazon DynamoDB table, along with your order ID."
    event_details = {
        "Details": json.dumps(
            dict(
                Message=Message,
                TaskToken=time.time(),
                userId=order.userId,
                eventId=order.evenId,
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

def release_queue():
    queue = (
        coffe_counting_table.get_item(
            Key={"PK": "order-queue"},
        )
        .get("Item")
        .get("IDvalue")
    )
    if not queue or queue == 0:
        queue = 0
        
        coffe_counting_table.put_item(
            Item={
                "PK": "order-queue",
                "IDvalue": queue  ,
            }
        )
    coffe_counting_table.put_item(
        Item={
            "PK": "order-queue",
            "IDvalue": queue -1 ,
        }
    )
def generate_order_id():
    order_id = (
        coffe_counting_table.get_item(
            Key={"PK": "orderID-ABC"},
        )
        .get("Item")
        .get("IDvalue")
    )
    if not order_id:
        order_id = 0
    coffe_counting_table.put_item(
        Item={
            "PK": "orderID-ABC",
            "IDvalue": order_id + 1,
        }
    )
    return order_id + 1


def update_make_order(
    order: Order,
    orderId: int,
    baristaId: str,
):
    coffe_order_table.update_item(
        Key={"PK": "orders", "SK": orderId},
        UpdateExpression="set #baristaUserId = :baristaUserId",
        ExpressionAttributeNames={"#baristaUserId": "baristaUserId"},
        ExpressionAttributeValues={":baristaUserId": {"S": baristaId}},
        ReturnValues="ALL_NEW",
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


def emit_making_order_event(order: Order, orderId, baristaId):
    Message = "Barista preparing order"
    event_details = {
        "Details": json.dumps(
            dict(
                Message=Message,
                TaskToken=time.time(),
                userId=order.userId,
                eventId=order.evenId,
                orderId=orderId,
                baristaId=baristaId,
            )
        ),
        "DetailType": "OrderManager.MakeOrder",
    }
    Entries = constants.events_payload | event_details
    events_client.put_events(Entries=[Entries])
