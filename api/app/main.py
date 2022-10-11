import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.config import env
from app.logic import auth, funding, fundraising, lookup, social

app = FastAPI(
    title="Jogaar",
    description="""Jogaar is a crowdfunding platform for future small business owners.""",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [
    auth.router,
    funding.router,
    fundraising.router,
    lookup.router,
    social.router,
]:
    app.include_router(router)


@app.get("/")
async def root() -> RedirectResponse | dict[str, str]:
    return RedirectResponse(app.docs_url) if app.docs_url else {"message": "no docs"}


# TODO cli
if __name__ == "__main__":
    uvicorn.run("main:api", port=env.API_PORT, log_level="info")
