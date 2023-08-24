from fastapi import FastAPI, HTTPException
import order_api.flows as order_flows
from pydantic import BaseModel
from enum import Enum
app = FastAPI()

class Order(BaseModel):
    userId: str
    eventId: str 
    orderId: str


class OrderAction(str, Enum):
    make = "make"
    unmake = "unmake"
    cancel = "cancel"
    complete = "complete"


@app.on_event("startup")
async def startup_event():

        
        
# Create order
@app.post("/order")
async def process_order(order: Order):
    if not order_flows.check_shop_open():
        order_flows.emit_cancel_order_event(order)
        return {"success": False}
    if not order_flows.available_queue():
        order_flows.emit_cancel_order_event(order)
        return {"success": False}
    order_flows.reserve_queue()
    order_flows.emit_workflow_started(order)
    return {"success": True}
    

@app.post("/order/{action}")
async def order_actions(action: OrderAction):
    if OrderAction is OrderAction.make:
        pass
    
    


@app.post("/emit_event")
async def emit_event(detail: dict):
    # Simulate emitting event
    return {"message": "Event Emitted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)