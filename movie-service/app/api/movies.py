import json
from typing import List
from fastapi import Header, APIRouter, HTTPException, Depends
from app.api.redis_client import get_redis_client
from app.api.models import MovieIn, MovieOut, MovieUpdate
from app.api import db_manager
from app.api.service import is_cast_present
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
movies = APIRouter()

def cache_get(redis_client, key:str):
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

def cache_set(redis_client, key:str, value: dict, ttl: int = 360):

    redis_client.set(key,json.dumps(value), ex = ttl)
    
@movies.get('/', response_model=List[MovieOut])
async def index():
    return await db_manager.get_all_movies()

@movies.get('/{id}', response_model=MovieOut)
async def get_movie(id: int, redis_client = Depends(get_redis_client)):
    cache_key = f'movie{id}'
    cache_result = cache_get(redis_client, cache_key)   
    if cache_result:
        movie = MovieOut(**cache_result)
        return movie
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie_keys = movie.keys()  # Assuming it returns field names like 'id', 'name', etc.
    movie_values = movie.values()  # This will return a tuple or list of values
        
    movie_dict = dict(zip(movie_keys, movie_values))
    cache_set(redis_client, cache_key, movie_dict)
    return movie

@movies.post('/', response_model = MovieOut ,status_code=201)
async def add_movie(payload: MovieIn):
    payload = payload.dict(exclude_unset=True)
    if 'cast_id' in payload:
        for cast_id in payload['cast_id']:
            print(cast_id)
            if not is_cast_present(cast_id):
                raise HTTPException(status_code = 404, detail = f"Cast with id:{cast_id} not found")
        
    movie_id = await db_manager.add_movie(payload)

    response = {
        'id': movie_id,
        **payload
    }

    return response

@movies.put('/{id}', response_model=MovieOut)
async def update_movie(id: int, payload: MovieUpdate):
   
    movie = await db_manager.get_movie(id)
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)
   
    if 'cast_id' in update_data:
        for cast_id in payload['cast_id']:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")


    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)
   
    return await db_manager.update_movie(id, updated_movie)



@movies.delete('/{id}', response_model = None)
async def delete_movie(id: int, redis_client = Depends(get_redis_client)):
    movie = await db_manager.get_movie(id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    cache_key = f'movies{id}'
    redis_client.delete(cache_key)
    return await db_manager.delete_movie(id)
