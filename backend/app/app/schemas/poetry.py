from pydantic import BaseModel, HttpUrl

from typing import Sequence


class PoetryBase(BaseModel):
    label: str
    source: str
    url: HttpUrl


class PoetryCreate(PoetryBase):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int


class PoetryUpdate(PoetryBase):
    label: str


# Properties shared by models stored in DB
class PoetryInDBBase(PoetryBase):
    id: int
    submitter_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Poetry(PoetryInDBBase):
    pass


# Properties properties stored in DB
class PoetryInDB(PoetryInDBBase):
    pass


class PoetrySearchResults(BaseModel):
    results: Sequence[Poetry]
