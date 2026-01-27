from pydantic import BaseModel
from typing import List, Optional


class GenreByRegionResponse(BaseModel):
    region: str
    genre: str
    stream_count: int


class SubscriberByRegionResponse(BaseModel):
    region: str
    level: str
    user_count: int


class TopArtistResponse(BaseModel):
    artist: str
    stream_count: int
    rank: int


class RisingArtistResponse(BaseModel):
    artist: str
    growth_rate: float
    current_streams: int
    previous_streams: int
