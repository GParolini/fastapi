import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import base  # noqa: F401
from app.core.config import settings

logger = logging.getLogger(__name__)


POETRIES = [
    {
        "id": 1,
        "label": "Best Society",
        "source": "Philip Larkin",
        "url": "https://allpoetry.com/Best-Society",
    },
    {
        "id": 2,
        "label": "Map of the New World - I Archipelagoes",
        "source": "Derek Walcott",
        "url": "https://www.poetryfoundation.org/poems/47662/map-of-the-new-world",
    },
    {
        "id": 3,
        "label": "Fragen eines lesenden Arbeiters",
        "source": "Bertolt Brecht",
        "url": "https://archiv2017.die-linke.de/partei/dokumente/programm-der-partei-die-linke/bertolt-brecht-fragen-eines-lesenden-arbeiters/",  # noqa
    },
    {
        "id": 4,
        "label": "O Tell Me the Truth About Love",
        "source": "W.H. Auden",
        "url": "https://www.thereader.org.uk/wp-content/uploads/2021/02/Auden-W.H.-O-Tell-Me-the-Truth-About-Love.pdf",
    },
    {
        "id": 5,
        "label": "I limoni",
        "source": "Eugenio Montale",
        "url": "https://www.libriantichionline.com/divagazioni/eugenio_montale_limoni_1925",
    },
    
]


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                full_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                is_superuser=True,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.FIRST_SUPERUSER} already exists. "
            )
        if not user.poetries:
            for poetry in POETRIES:
                poetry_in = schemas.PoetryCreate(
                    label=poetry["label"],
                    source=poetry["source"],
                    url=poetry["url"],
                    submitter_id=user.id,
                )
                crud.poetry.create(db, obj_in=poetry_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
