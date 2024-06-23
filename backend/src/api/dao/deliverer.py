from typing import Optional
from src.models.deliverer import DeliveryDetails
from src.models.db.database import database

async def get_new_delivery() -> Optional[DeliveryDetails]:
    query = """
        SELECT * FROM delivery_details
        ORDER BY updated_at DESC
        LIMIT 1
    """
    row = await database.connection.fetchrow(query)
    if row:
        return DeliveryDetails(**dict(row))
    return None
