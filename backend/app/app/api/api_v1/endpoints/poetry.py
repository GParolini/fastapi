from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.api import deps
from app.schemas.poetry import Poetry, PoetryCreate, PoetrySearchResults

router = APIRouter()


@router.get("/{poetry_id}", status_code=200, response_model=Poetry)
def fetch_poetry(
    *,
    poetry_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Fetch a single poetry by ID
    """
    result = crud.poetry.get(db=db, id=poetry_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Poetry with ID {poetry_id} not found"
        )

    return result


@router.get("/search/", status_code=200, response_model=PoetrySearchResults)
def search_poetries(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="Brecht"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for poetries based on label keyword
    """
    poetries = crud.poetry.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": poetries}

    results = filter(lambda poetry: keyword.lower() in poetry.label.lower(), poetries)
    return {"results": list(results)[:max_results]}


@router.post("/", status_code=201, response_model=Poetries)
def create_poetry(
    *, poetry_in: PoetryCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new poetry in the database.
    """
    poetry = crud.poetry.create(db=db, obj_in=poetry_in)

    return poetry
