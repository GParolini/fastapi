from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates

from typing import Optional, Any
from pathlib import Path
from sqlalchemy.orm import Session

from app.schemas.poetry import PoetrySearchResults, Poetry, PoetryCreate
from app import deps
from app import crud


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Poetry API", openapi_url="/openapi.json")

api_router = APIRouter()


# Updated to serve a Jinja2 template
# https://www.starlette.io/templates/
# https://jinja.palletsprojects.com/en/3.0.x/templates/#synopsis


@api_router.get("/", status_code=200)
def root(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    poetries = crud.poetry.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "poetries": poetries},
    )


@api_router.get("/poetry/{poetry_id}", status_code=200, response_model=Poetry)
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


@api_router.get("/search/", status_code=200, response_model=PoetrySearchResults)
def search_poetries(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
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


@api_router.post("/poetry/", status_code=201, response_model=Poetry)
def create_poetry(
    *, poetry_in: PoetryCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new poetry in the database.
    """
    poetry = crud.poetry.create(db=db, obj_in=poetry_in)

    return poetry


app.include_router(api_router)



if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
