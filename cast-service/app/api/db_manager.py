from app.api.models import CastIn, CastOut, CastUpdate
from app.api.db import casts, database
from sqlalchemy import select


async def add_cast(payload: CastIn):
    query = casts.insert().values(**payload.dict())
    cast_id = await database.execute(query = query)
    return cast_id

async def get_cast(id: int):
    query = select(casts.c.id, casts.c.name, casts.c.nationality).where(casts.c.id == id)
    
    result = await database.fetch_one(query)
    return result

async def get_all_casts():
    query = casts.select()
    return await database.fetch_all(query=query)
