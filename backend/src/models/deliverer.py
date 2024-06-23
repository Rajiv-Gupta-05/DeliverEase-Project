from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class DeliveryDetails(BaseModel):
    delivery_detail_id: int
    pick_up: str
    drop_off: str
    cont_name: str
    phone: constr(min_length=10, max_length=15)
    size_name: str
    fragile: bool
    temp_sensitive: bool
    delivery_type: str
    distance: float
    peak_hour: bool
    description: Optional[str]
