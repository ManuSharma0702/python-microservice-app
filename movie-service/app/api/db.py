from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
import os
from databases import Database

DATABASE_URL = 'postgresql://postgres:iamManusharma123@movie-db/movies_db'
# DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement = True),
    Column('name', String(50)),
    Column('plot', String(1000)),
    Column('genres', ARRAY(String)),
    Column('cast_id', ARRAY(Integer))
)

database = Database(DATABASE_URL)