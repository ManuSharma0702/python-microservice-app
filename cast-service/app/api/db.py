from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine)
import os
from databases import Database

DATABASE_URL = 'postgresql://postgres:iamManusharma123@cast-db/cast_db'
#DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(50)),
    Column('nationality', String(50)),
)

database = Database(DATABASE_URL)
