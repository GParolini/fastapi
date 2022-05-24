from app.crud.base import CRUDBase
from app.models.poetry import Poetry
from app.schemas.poetry import PoetryCreate, PoetryUpdate


class CRUDPoetry(CRUDBase[Poetry, PoetryCreate, PoetryUpdate]):
    ...


poetry = CRUDPoetry(Poetry)
