from contextlib import contextmanager
from pathlib import Path

import uvicorn
from app.core.config import env
from app.core.security import hash_password
from app.data.crud import user
from app.data.session import get_db
from app.views import auth, funding, fundraising, lookup, social
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

# TODO use env vars for these

app = FastAPI(
    title="Jogaar",
    description="""Jogaar is a crowdfunding platform for future small business owners.""",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

staticdir = Path("static")
staticdir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=staticdir), name="static")

routers = [
    auth.router,
    funding.router,
    fundraising.router,
    lookup.router,
    social.router,
]

for router in routers:
    app.include_router(router)


@app.get("/")
async def root() -> RedirectResponse | dict[str, str]:
    return RedirectResponse(app.docs_url) if app.docs_url else {"message": "no docs"}


first_admin_data = user.UserCreate(
    name=env.ADMIN_NAME,
    email=env.ADMIN_MAIL,
    password=hash_password(env.ADMIN_PASS),
)

with contextmanager(get_db)() as db:
    existing_u = user.read_by_email(env.ADMIN_MAIL, db)
    if existing_u is None:
        user.create_with_access(first_admin_data, user.Access.ADMIN, db)
    else:
        user.update_access(existing_u.id, user.Access.ADMIN, db)


# TODO cli
if __name__ == "__main__":
    uvicorn.run("main:app", port=env.API_PORT, log_level="info")
