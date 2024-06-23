from fastapi import APIRouter, HTTPException
from src.api.dao.deliverer import get_new_delivery
from src.models.deliverer import DeliveryDetails

router = APIRouter()

@router.get("/newdeliverer", response_model=DeliveryDetails)
async def read_latest_delivery():
    delivery_details = await get_new_delivery()
    if not delivery_details:
        raise HTTPException(status_code=404, detail="No delivery details found")
    return delivery_details
