import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


aws_region = os.environ.get("AWS_REGION", "eu-central-1")
coffee_queue_size = os.environ.get("QUEUE", 20)

coffee_config = dict(
    config_table=os.environ.get(
        "SERVERLESSPRESSO_CONFIG_TABLE",
        "serverlesspresso-config-table",
    ),
    counting_table=os.environ.get(
        "SERVERLESSPRESSO_COUNTING_TABLE",
        "serverlesspresso-counting-table",
    ),
    order_table=os.environ.get(
        "SERVERLESSPRESSO_ORDER_TABLE",
        "serverlesspresso-order-table",
    ),
    validator_table=os.environ.get(
        "SERVERLESSPRESSO_VALIDATOR_TABLE", 
        "serverlesspresso-validator-table"
    ),
    eventbridge = os.environ.get(
        "SERVERLESSPRESSO_EVENTBRIDGE", 
        "Serverlesspresso"
    ),
    eventsource = os.environ.get(
        "SERVERLESSPRESSO_EVENTSOURCE", 
        "awsserverlessda.serverlesspresso"
    )
    
)


events_payload =  {
      "EventBusName": coffee_config.get("eventbridge"),
      "Source": coffee_config.get("eventsource"),
    }

